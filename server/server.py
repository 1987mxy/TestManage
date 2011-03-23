#coding=gbk

from sys import path
path.append('..\\lib')

import stackless
from urllib import urlopen
from traceback import format_exc
from struct import unpack, pack


from mylib.log import LOG
import mylib.package
from mylib.settings import *

from protobuf.msg_base_pb2 import Msg
from protobuf.res_base_pb2 import Response
from protobuf.soc_login_pb2 import SocketLoginMessage

import roachlib.stacklesssocket
import roachlib.scheduler

RUN = True

CHList = {}   #链接上此服务器的client的广播channel列表
CLTLIST = []   #一次case的client列表由0x0001包中获得
CONTROL = None  #一次case的控制端的广播channel
LoginInfo = {}  #虚拟登录时返回的登录信息

TASK_APP = []
TASK_CLT = []
TASK_TEST = []

SLEEP = roachlib.scheduler.DelayScheduler()  #stackless的sleep
SLEEP.start()

class net(object):
    def __init__(self, sock, addr, magic = None):
        if self.__class__ is net:
            LOG.error('net class dose not instantiation')
            raise 'net class dose not instantiation'
        self.address = '%s:%s'%addr
        self.sock = sock
        self.switch = True
        self.death = False
        self.MagicCode = magic
        self.windage = 0   #virtual message包长度字段长度与testmanage包长度字段长度不同，用来修正
        self.headformat = '<LH'
        self.heart = stackless.channel()
        self.broadcast = stackless.channel()
        self.net_to_parse = stackless.channel()
        
    
    def receive(self):
        try:
            pdata = ''
            while self.switch:
                LOG.debug('%s listening...'%self.address)
                rdata = self.sock.recv(1000)
                LOG.debug('receive raw_string from %s : %s'%(self.address, 
                                                             rdata.__len__()))
                if not rdata:
                    LOG.info('%s disconnect...'%self.address)
                    self.exit()
                else:
                    self.death = False
                    pdata = self.parseHead('%s%s'%(pdata, rdata))
        except :
            LOG.error('type %s : %s'%(self.__class__, dir(self)))
            LOG.error('%s net error : %s'%(self.address,
                                           format_exc()))
            self.exit()

    def parseHead(self, data):
        authentic = False
        if len(data) >= 6:
            head = unpack(self.headformat, data[:6])
            if not self.MagicCode:
                if (head[1] <= 6 and head[1] > 0) or (head[1] in [0xABDE,0xffff,0xff00,0xf0f0]):
                    authentic = True
            elif self.MagicCode == head[1]:
                authentic = True
            if head[0] + self.windage <= len(data):
                mdata = data[ : head[0] + self.windage]
                data = data[head[0] + self.windage : ]
                #TODO: 检查返回数据的格式
                if head[1] == 0x0006:
                    self.heart.send(mdata)
                elif authentic:
                    self.net_to_parse.send([head[0], head[1], mdata])
                data = self.parseHead(data)
        return data

    def threadBroadcast(self):
        while self.switch:
            try:
                rdata = self.broadcast.receive()
                if rdata == 'exit':
                    LOG.info('%s be exited!'%self.address)
                    self.exit()
                else:
                    self.sock.sendall(rdata)
                    LOG.debug('send to %s : %s'%(self.address, 
                                                 rdata.__len__()))
            except Exception, e:
                LOG.error('%s broadcast error...'%self.address)
                if e.args == 9:
                    LOG.error('%s Socket has be closed! Send package failed : %s'%(self.address, 
                                                                                   rdata.__len__()))
                else:
                    LOG.error('%s : %s'%(format_exc(),
                                         rdata.__repr__()))
                self.exit()

    def chkHeart(self, time):
        while (not self.death) and self.switch:
            self.death = True
            SLEEP.delay_caller(time)
        if self.switch:
            LOG.error('%s heart time out !'%self.address)
            self.exit()
    
    def reHeart(self, time):
        while self.switch:
            package = self.heart.receive()
            LOG.debug('received heart from %s !'%self.address)
            SLEEP.delay_caller(time)
            if self.switch:
                self.broadcast.send(package)
                
    def exit(self):
        pass

class testManage(net):
    def __init__(self, sock, addr):
        super(testManage, self).__init__(sock, addr)
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()
        
        self.task_reHeart = stackless.tasklet(self.reHeart)(10)
        self.task_chkHeart = stackless.tasklet(self.chkHeart)(60)
        CHList[self.address] = self.broadcast
        self.task_receive = stackless.tasklet(self.receive)()
        
        self.e_pack = mylib.package.packCtrlEnd()
        self.user = None
        self.uid = None
        self.cltlist = []
        
    def exit(self):
        global CONTROL, CHList
        self.switch = False
        if self.address in CHList.keys():    #不是CONTROL
            del(CHList[self.address])
            if CONTROL:
                info = '%s heart time out or disconnect ...'%self.address
                CONTROL.send(mylib.package.pack2(info))
            self.chkEnd(self.address)
            if self.uid in CHList.keys() and self.broadcast in CHList[self.uid]:       #client.exe退出时关闭该链接虚拟登录
                CHList[self.uid].remove(self.broadcast)
        else:
            CONTROL = None
            self.dispense('exit')
        LOG.info('%s testManage exit...'%self.address)
    
    def listen_message(self):
        global CLTLIST, CONTROL, RUN
        msg = SocketLoginMessage()
        pbr = Response()
        while self.switch:
            r_pack = self.net_to_parse.receive()
            if r_pack[1] != 0xABDE:
                LOG.info('received head from %s : [%d, %2x]'%(self.address, 
                                                              r_pack[0], 
                                                              r_pack[1]))
            else:
                LOG.debug('received head from %s : [%d, %2x]'%(self.address, 
                                                               r_pack[0], 
                                                               r_pack[1]))
            LOG.debug('received package from %s : %s'%(self.address,
                                                       r_pack[2].__len__()))
            result = ''
            if r_pack[1] == 0x0001:
                CONTROL = self.broadcast
                del(CHList[self.address])
                s_pack = self.getCltList(r_pack)
                for ip in self.cltlist:
                    fail = True
                    for addr in CHList.keys():
                        if ':' in ip and ip == addr:
                            CLTLIST.append(ip)
                            CHList[ip].send('%sip:%s'%(s_pack, self._myIP(ip.split(':')[0])))
                            LOG.info('send to %s'%ip)
                            fail = False
                            break
                        elif (not ':' in ip) and ip in addr:
                            CLTLIST.append(addr)
                            CHList[addr].send('%sip:%s'%(s_pack, self._myIP(ip)))
                            LOG.info('send to %s'%addr)
                            fail = False
                    if fail:
                        result = '%s connecting failed...\n'%ip
                        s_pack = mylib.package.pack2(result)
                        self.broadcast.send(s_pack)
                if not CLTLIST:
                    self.broadcast.send(self.e_pack)
            elif r_pack[1] in [0x0002, 0x0004]:
                if CONTROL:
                    CONTROL.send(r_pack[2])
            elif r_pack[1] in [0x0003, 0xffff]:
                self.dispense(r_pack[2])
            elif r_pack[1] == 0x0005:
                del(CHList[self.address])
                ips = ''
                for ip in CHList.keys():
                    if ':' in ip:
                        ch_len = 1
                    else:
                        ch_len = CHList[ip].__len__()
                    ips = '%s%s %s\n'%(ips, ip, ch_len)
                LOG.info(ips)
                result = '%s%s'%(result, ips)
                s_pack = mylib.package.pack2(result)
                s_pack = '%s%s'%(s_pack, self.e_pack)
                self.broadcast.send(s_pack)
            elif r_pack[1] == 0xff00:
                self.chkEnd(self.address)
            elif r_pack[1] == 0xf0f0:   #关闭服务器
                global TASK_APP, TASK_CLT
                LOG.info('The End ...')
                s_pack = mylib.package.pack2('The End ...')
                s_pack = '%s%s'%(s_pack, self.e_pack)
                self.broadcast.send(s_pack)
                for t in TASK_APP:
                    t.kill()
                for t in TASK_CLT:
                    t.kill()
                RUN = False
                try:
                    for ch_key in CHList.keys():
                        if ':' in ch_key:
                            CHList[ch_key].send('exit')
                        else:
                            for uid_ch in CHList[ch_key]:
                                uid_ch.send('exit')
                except :
                    pass
#            模拟登陆
            elif r_pack[1] == 0xABDE:    #用来借助自动脚本关闭war3进程所必须的登录
                msg.ParseFromString(r_pack[2][14:])
                LOG.debug('receive package from %s : %s'%(self.address,
                                                          msg))
                user = msg.userName
                if user in LoginInfo.keys():    #virtual login
                    sid = LoginInfo[user]
                    url = '%s/user.tcplogin/?alt=pbbin&sid=%s&service=msg'%(APPSERVER, 
                                                                            sid)
                    LOG.info('%s_%s send http request : %s'%(user,
                                                             self.address, 
                                                             url))
                    mdata = urlopen(url).read()
                    pbr.ParseFromString(mdata)
                    LOG.info('%s_%s receive http response : %s'%(user, 
                                                                 self.address, 
                                                                 pbr))
                    if pbr.code == 200000:
                        self.user = user
                        self.uid = str(pbr.userTCPLogin.uid)
                        CHList[self.uid].append(self.broadcast)
                        LOG.info('%s_%s_%s double logined'%(user, 
                                                            self.uid, 
                                                            self.address))
                        self.broadcast.send(mylib.package.make_response_clt(mdata))
                    else:
                        if self.user in LoginInfo.keys():
                            del(LoginInfo[self.user])
                        LOG.error('%s_%s double logined failed !'%(user, 
                                                                   self.address))
                
    def dispense(self, package):
        global CLTLIST
        result = ''
        for ip in CLTLIST:     #调出0x0001包中所存在的目的地址
            if ip in CHList.keys():     #与正连接的客户端列表进行比较
                CHList[ip].send(package)
                LOG.info('send to %s'%ip)
            else:
                info = '%s connecting failed ...'%ip
                LOG.info(info)
                self.broadcast.send(mylib.package.pack2(info))
                self.chkEnd(ip)

    def chkEnd(self, addr):
        global CLTLIST, CONTROL
        if addr in CLTLIST:     #当客户端列表为空时，可以发送控制端收尾指令
            CLTLIST.remove(addr)
            if not CLTLIST:
                CONTROL.send(self.e_pack)

    def getCltList(self, r_pack):
        cltstring_len = int(unpack('<H', r_pack[2][6:8])[0])
        if cltstring_len == 0xffff:
            self.cltlist = [ip for ip in CHList.keys() if ':' in ip]   #没有':'则为virtual_message的链接,需要排除
            cltstring_len = 0
        else:
            cltstring = r_pack[2][8 : 8 + cltstring_len]
            for i in range(0, cltstring_len, 6):
                port = ord(cltstring[i+4]) * 256 + ord(cltstring[i+5])
                if port:
                    port = ':%s'%port
                else:
                    port = ''
                self.cltlist.append('%s.%s.%s.%s%s'%(ord(cltstring[i]),
                                                     ord(cltstring[i+1]),
                                                     ord(cltstring[i+2]),
                                                     ord(cltstring[i+3]),
                                                     port))
        m_pack = r_pack[2][8 + cltstring_len : ]
        s_pack = pack('<LH', 
                      r_pack[0] - cltstring_len + 16,     #16 = 18 - 2
                      r_pack[1])
        s_pack += m_pack
        return s_pack

    def _myIP(self, ip):
        ips = ip.split('.')
        tempip = ''
        for i in ips:
            i = '*'*(3-i.__len__()) + i
            tempip += i + '.'
        return tempip[:tempip.__len__()-1]

class VirtualMessage_to_Client(net):
    def __init__(self, sock, addr):
        super(VirtualMessage_to_Client, self).__init__(sock, addr, MAGIC_CLT)
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()
        self.headformat = '<HL'
        self.windage = 2
        self.task_receive = stackless.tasklet(self.receive)()
        
        self.uid = None
        self.sid = None
        self.user = None
        
    def exit(self):
        self.switch = False
        if self.uid in CHList.keys():
            if self.broadcast in CHList[self.uid]:
                CHList[self.uid].remove(self.broadcast)
            if len(CHList[self.uid]) <= 1:
                self.do_logout()
        LOG.info('%s Client exit...'%self.address)

    def listen_message(self):
        while self.switch:
            try:
                r_pack = self.net_to_parse.receive()
                mdata = r_pack[2]
                cmd = unpack("<H", mdata[8 : 10])[0]
                if cmd != 0x9006:
                    LOG.info('received head from %s_%s_%s : [%d, %2x]'%(self.user, 
                                                                        self.uid, 
                                                                        self.address, 
                                                                        r_pack[0], 
                                                                        cmd))
                else:
                    LOG.debug('received head from %s_%s_%s : [%d, %2x]'%(self.user, 
                                                                         self.uid, 
                                                                         self.address, 
                                                                         r_pack[0], 
                                                                         cmd))
                LOG.debug('received package from %s_%s_%s : %s'%(self.user, 
                                                                 self.uid, 
                                                                 self.address, 
                                                                 mdata.__len__()))
                if cmd == 0x9001:
                    pbr = Response()
                    msg = SocketLoginMessage()
                    msg.ParseFromString(mdata[14:])
                    user = msg.userName
                    LOG.debug('receive login_msg from %s : %s'%(self.address,
                                                                msg))
                    if msg.code == 1:
                        if user in LoginInfo.keys():    #virtual login
                            sid = LoginInfo[user]
                            url = '%s/user.tcplogin/?alt=pbbin&sid=%s&service=msg'%(APPSERVER, 
                                                                                    sid)
                            LOG.info('%s_%s send http request : %s'%(user,
                                                                     self.address, 
                                                                     url))
                            mdata = urlopen(url).read()
                            pbr.ParseFromString(mdata)
                            LOG.info('%s_%s receive http response : %s'%(user, 
                                                                         self.address, 
                                                                         pbr))
                            if pbr.code == 200000:
                                self.user = user
                                self.uid = str(pbr.userTCPLogin.uid)
                                CHList[self.uid].append(self.broadcast)
                                LOG.info('%s_%s_%s double logined ...'%(self.user, 
                                                                        self.uid, 
                                                                        self.address))
                            else:
                                #此时sid已经过期用sid登出是没有意义的
                                del(LoginInfo[user])
                                LOG.error('%s_%s double logined failed !'%(user, 
                                                                           self.address))
                        else:
                            url = '%s/user.tcplogin/?alt=pbbin&username=%s&password=%s&service=msg'%(APPSERVER, 
                                                                                                     user, 
                                                                                                     msg.password)
                            LOG.info('%s_%s send http request: %s'%(user, 
                                                                    self.address, 
                                                                    url))
                            mdata = urlopen(url).read()
                            pbr.ParseFromString(mdata)
                            LOG.info('%s_%s receive http response: %s'%(user, 
                                                                        self.address, 
                                                                        pbr))
                            if pbr.code == 200000:
                                self.user = user
                                self.uid = str(pbr.userTCPLogin.uid)
                                self.sid = pbr.userTCPLogin.sid
                                CHList[self.uid] = [self.broadcast]
                                LoginInfo[user] = self.sid
                                LOG.info('%s_%s_%s logined ...'%(self.user, 
                                                                 self.uid, 
                                                                 self.address))
                            else:
                                LOG.error('%s_%s_%s login failed : %s'%(self.user, 
                                                                        self.uid, 
                                                                        self.address, 
                                                                        pbr))
                        self.broadcast.send(mylib.package.make_response_clt(mdata))
                    elif msg.code == 3:
                        self.do_logout()
                elif cmd == 0x9006:  #return 0x9008 heart for flash
                    LOG.debug('receive heart from %s_%s_%s ...'%(self.user, 
                                                                 self.uid, 
                                                                 self.address))
                else:
                    LOG.warning('unknow package from %s_%s_%s : %x'%(self.user, 
                                                                     self.uid, 
                                                                     self.address, 
                                                                     cmd))
            except :
                LOG.error('listen message error from %s_%s_%s : %x, %s'%(self.user, 
                                                                         self.uid, 
                                                                         self.address, 
                                                                         cmd, 
                                                                         r_pack.__repr__()))
                LOG.error(format_exc())

    def do_logout(self):
        if self.uid in CHList.keys() and self.user in LoginInfo.keys():
            pbr = Response()
            url = '%s/user.tcplogout/?alt=pbbin&sid=%s&service=msg'%(APPSERVER,
                                                                     self.sid)
            mdata = urlopen(url).read()
            LOG.info('%s_%s_%s send http request: %s'%(self.user, 
                                                       self.uid, 
                                                       self.address, 
                                                       url))
            pbr.ParseFromString(mdata)
            LOG.info('%s_%s_%s receive http response: %s'%(self.user, 
                                                           self.uid, 
                                                           self.address, 
                                                           pbr))
            for ch in CHList[self.uid]:
                ch.send(mylib.package.make_response_clt(mdata))
            if pbr.code == 200000:
                del(LoginInfo[self.user])
                del(CHList[self.uid])
                self.switch = False
                LOG.info('%s_%s_%s logouted...'%(self.user, 
                                                 self.uid, 
                                                 self.address))
            else:
                LOG.error('%s_%s_%s logout failed : %s'%(self.user, 
                                                         self.uid, 
                                                         self.address, 
                                                         pbr))

class VirtualMessage_to_Service(net):
    def __init__(self, sock, addr):
        super(VirtualMessage_to_Service, self).__init__(sock, addr, MAGIC_SRV)
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()
        self.headformat = '<HL'
        self.windage = 2
        self.task_receive = stackless.tasklet(self.receive)()
        self.package = None
        
    def exit(self):
        self.switch = False
        LOG.info('%s APP Service exit...'%self.address)

    def listen_message(self):
        while self.switch:
            try:
                r_pack = self.net_to_parse.receive()  #r_pack[0] 包长度, r_pack[1]magic_code, r_pack[2]收到的完成数据包
                LOG.debug('received package from APP Service %s : %s'%(self.address, 
                                                                       r_pack[2].__len__()))
                mdata = r_pack[2]
                cmd = unpack("<H", mdata[8 : 10])[0]
                LOG.info('APP Service %s code: %x'%(self.address, 
                                                    cmd))
                if cmd == 0x7001:
                    receivers_list = self.getReceivers(mdata)
                    for receiver in receivers_list:
                        if str(receiver) in CHList.keys():
                            s_string = mylib.package.make_transmit(self.package)
                            for ch in CHList[str(receiver)]:
                                LOG.info('APP Service %s transmit to receiver %s : %s'%(self.address,
                                                                                        receiver, 
                                                                                        self.package.__len__()))
                                ch.send(s_string)
                    self.broadcast.send(mylib.package.make_response_app(0))
                else:
                    LOG.warning('unknow code from APP Service %s : %x'%(self.address, 
                                                                        cmd))
            except :
                LOG.error('listen message error from APP Service %s : %x, %s'%(self.address,
                                                                               cmd, 
                                                                               r_pack.__repr__()))
                LOG.error(format_exc())

    def getReceivers(self, package):
        receivers_len = unpack("<H", package[14 : 16])[0]
        receivers_string = package[16 : receivers_len * 4 + 16]
        self.package = package[receivers_len * 4 + 16 : ]
        receivers_list = unpack('<%sL'%receivers_len, receivers_string)
        return receivers_list

def TestThread():
    global RUN, TASK_TEST
    LOG.info('testmanage runing...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',TEST_PORT))
    sock.listen(1)
    while RUN:
        sockclient,addr = sock.accept()
        LOG.info('%s:%s TestManage connected...'%addr)
        test = testManage(sockclient, addr)
        TASK_TEST.append(stackless.tasklet(test.listen_message)())
    sock.close()

def CltThread():
    global RUN, TASK_CLT 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',CLT_PORT))
    sock.listen(1)
    while RUN:
        sockclient, addr = sock.accept()
        LOG.info('%s:%s Clt connected...'%addr)
        clt = VirtualMessage_to_Client(sockclient, addr)
        TASK_CLT.append(stackless.tasklet(clt.listen_message)())
    sock.close()
        
def APPThread():
    global RUN, TASK_APP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',APP_PORT))
    sock.listen(1)
    while RUN:
        sockclient, addr = sock.accept()
        LOG.info('%s:%s APP service connected...'%addr)
        srv = VirtualMessage_to_Service(sockclient, addr)
        TASK_APP.append(stackless.tasklet(srv.listen_message)())
    sock.close()

if __name__ == '__main__':
    from os import system
    system('title VirtualMessage Service')
    roachlib.stacklesssocket.install()
    import socket
    if VirtualMessage:
        LOG.info('virtualmessage runing...')
        TASK_APP.append(stackless.tasklet(APPThread)())
        TASK_CLT.append(stackless.tasklet(CltThread)())
    TASK_TEST.append(stackless.tasklet(TestThread)())
    while RUN:
        stackless.run()