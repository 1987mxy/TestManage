#coding=gbk

from sys import path
path.append('..\\lib')

import stackless
from urllib import urlopen
from traceback import format_exc
from struct import unpack, pack


from mylib.log import LOG
import mylib.package
from mylib import settings
from mylib.other import chkPath

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

class MyStacklessChannel(stackless.channel):
    def send(self, obj):
        if not self.closing:
            super(MyStacklessChannel, self).send(obj)
            
    def receive(self):
        if not self.closing:
            recv = super(MyStacklessChannel, self).receive()
            return recv
        return ''

class net(object):
    def __init__(self, sock, addr, magicCode, heartCode):
        if self.__class__ is net:
            LOG.error('net class dose not instantiation')
            raise 'net class dose not instantiation'
        self.address = '%s:%s'%addr
        self.sock = sock
        self.switch = True
        self.death = False
        self.magicCode = magicCode
        self.heartCode = heartCode
        self.headformat = '<HLHHL'
        self.broadcast = MyStacklessChannel()
        self.net_to_parse = MyStacklessChannel()
    
    def receive(self):
        try:
            pdata = ''
            while self.switch:
                LOG.debug('%s listening...'%self.address)
                rdata = self.sock.recv(1000)
                LOG.debug('receive raw_string from %s : '%self.address, rdata)
                if not rdata:
                    LOG.info('%s disconnect...'%self.address)
                    self.exit()
                else:
                    self.death = False
                    pdata = self.parseHead('%s%s'%(pdata, rdata))
        except :
            LOG.error('type %s : %s'%(self.__class__, dir(self)))
            LOG.error('receive error : %s'%format_exc())
            LOG.error('%s receive error : %s'%(self.address, 
                                               format_exc()))
            self.exit()

    def parseHead(self, data):
        if len(data) >= 14:
            head = unpack(self.headformat, data[:14])
            if head[0] + 2 <= len(data):
                mdata = data[ : head[0] + 2]
                data = data[head[0] + 2 : ]
                if head[1] == self.magicCode:
                    if head[3] != self.heartCode:
                        self.net_to_parse.send([head[0], head[3], mdata])
                else:
                    LOG.error('receive FIFA package from %s : '%self.address, mdata)
                    self.exit()
                data = self.parseHead(data)
        return data

    def threadBroadcast(self):
        while self.switch:
            try:
                rdata = self.broadcast.receive()
                if rdata == 'exit':
                    LOG.info('%s be exited!'%self.address)
                    self.exit()
                elif self.switch:
                    if rdata.__class__ is list:
                        self.sock.sendall(rdata[0])
                        LOG.debug('uuid package %s send to %s : '%(rdata[1], self.address), rdata[0])
                    else:
                        self.sock.sendall(rdata)
                        LOG.debug('send to %s : '%self.address, rdata)
                else:
                    LOG.info('send to %s failed !'%self.address)
            except Exception:
                LOG.error('%s broadcast error : '%self.address)
                LOG.error('%s\n%s'%(format_exc(),
                                    rdata.__repr__()))
                self.exit()

    def chkHeart(self, time):
        while (not self.death) and self.switch:
            self.death = True
            SLEEP.delay_caller(time)
        if self.switch:
            LOG.error('%s heart time out !'%self.address)
            self.exit()
    
    def reHeart(self):
        pass
                
    def exit(self):
        pass

class testManage(net):
    def __init__(self, sock, addr):
        super(testManage, self).__init__(sock, 
                                         addr, 
                                         settings.TestManage.magicCode, 
                                         settings.TestManage.heartCode)
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()
        
        self.task_reHeart = stackless.tasklet(self.reHeart)(10)
        self.task_chkHeart = stackless.tasklet(self.chkHeart)(30)
        CHList[self.address] = self.broadcast
        self.task_receive = stackless.tasklet(self.receive)()
        
        self.e_pack = mylib.package.packCtrlEnd()
        self.user = None
        self.uid = None
        self.cltlist = []
        
        
        self.file = {}
        
    def chkHeart(self, time):
        while (not self.death) and self.switch:
            self.death = True
            SLEEP.delay_caller(time)
        if self.switch:
            LOG.error('%s TestManage heart time out !'%self.address)
            self.exit()
        
    def reHeart(self, time):
        h_pack = mylib.package.pack6()
        while self.switch:
            LOG.debug('send heart to TestManage %s !'%self.address)
            SLEEP.delay_caller(time)
            try:
                self.sock.sendall(h_pack)
            except:
                pass
        
    def exit(self):
        global CONTROL, CHList
        self.broadcast.close()
        self.heart.close()
        self.net_to_parse.close()
        self.switch = False
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        if self.address in CHList.keys():    #不是CONTROL
            del(CHList[self.address])
            if CONTROL:
                info = '%s heart time out or disconnect ...'%self.address
                CONTROL.send(mylib.package.pack2(info))
            self.chkEnd(self.address)
        elif self.broadcast == CONTROL:
            CONTROL = None
            self.dispense('exit')
        if self.uid in CHList.keys() and self.broadcast in CHList[self.uid]:       #client.exe退出时关闭该链接虚拟登录
            CHList[self.uid].remove(self.broadcast)
            if not CHList[self.uid]:
                del(CHList[self.uid])
        LOG.info('%s TestManage exit...'%self.address)
    
    def listen_message(self):
        global CLTLIST, CONTROL, RUN
        msg = SocketLoginMessage()
        pbr = Response()
        while self.switch:
            r_pack = self.net_to_parse.receive()
            if r_pack[1] in [0x9001,0x9003,0x9004]:   #是用SID不停登陆的,所以需要不显示LOG
                LOG.debug('received head from TestManage %s : [%d, %2x]'%(self.address, 
                                                                          r_pack[0], 
                                                                          r_pack[1]))
            else:
                LOG.info('received head from TestManage %s : [%d, %2x]'%(self.address, 
                                                                         r_pack[0], 
                                                                         r_pack[1]))
            LOG.debug('received package from TestManage %s : '%self.address, r_pack[2])
            result = ''
            if r_pack[1] == 0x0001:
                CONTROL = self.broadcast
                if self.address in CHList.keys():
                    del(CHList[self.address])
                s_pack = self.getCltList(r_pack)
                if CLTLIST:
                    for ip in CLTLIST:
                        CHList[ip].send('%sip:%s'%(s_pack, self._myIP(ip.split(':')[0])))
                        LOG.info('send to TestManage %s'%ip)
                else:
                    self.broadcast.send(self.e_pack)
            elif r_pack[1] in [0x0002, 0x0004]:
                if CONTROL:
                    CONTROL.send(r_pack[2])
            elif r_pack[1] in [0x0003, 0xffff]:
                self.dispense(r_pack[2])
            elif r_pack[1] == 0x0005:
                if self.address in CHList.keys():
                    del(CHList[self.address])
                ips = []
                for ip in CHList.keys():
                    if ':' in ip:
                        ch_len = 1
                    else:
                        ch_len = CHList[ip].__len__()
                    ips += [ip, '\t', str(ch_len), '\n']
                result = ''.join(ips)
                LOG.info(result)
                s_pack = ''.join([mylib.package.pack2(result), self.e_pack])
                self.broadcast.send(s_pack)
            elif r_pack[1] == 0xff00:
                self.chkEnd(self.address)
            elif r_pack[1] == 0xf0f0:   #关闭服务器
                pass
#            模拟登陆
            elif r_pack[1] == 0x9001:    #用来借助自动脚本关闭war3进程所必须的登录
                msg.ParseFromString(r_pack[2][14:])
                LOG.debug('receive package from TestManage %s : %s'%(self.address,
                                                                     msg))
                user = msg.userName
                if user in LoginInfo.keys():    #virtual login
                    sid = LoginInfo[user]
                    url = '%s/user.tcplogin/?alt=pbbin&sid=%s&service=msg'%(settings.APPSERVER, 
                                                                            sid)
                    r_pack[2] = urlopen(url).read()
                    LOG.info('%s_%s TestManage send http request : %s'%(user,
                                                                        self.address, 
                                                                        url))
                    pbr.ParseFromString(r_pack[2])
                    LOG.info('%s_%s TestManage receive http response : %s'%(user, 
                                                                            self.address, 
                                                                            pbr))
                    if pbr.code == 200000:
                        self.user = user
                        self.uid = str(pbr.userTCPLogin.uid)
                        CHList[self.uid].append(self.broadcast)
                        LOG.info('%s_%s_%s TestManage double logined'%(user, 
                                                                       self.uid, 
                                                                       self.address))
                        self.broadcast.send(mylib.package.make_response_clt(r_pack[2]))
                    else:
                        if self.user in LoginInfo.keys():
                            del(LoginInfo[self.user])
                        LOG.error('%s_%s TestManage double logined failed !'%(user, 
                                                                              self.address))
#===============================================================================
# 姚常鋆 C++ Client LOG收集逻辑
#===============================================================================
            elif r_pack[1] == 0x1001:
                filename_len = unpack('<H',r_pack[2][14 : 16])[0]   #log文件名长度
                filename = r_pack[2][16 : filename_len + 16]
                if filename in self.file.keys():
                    self.file[filename].write(r_pack[2][filename_len + 16 : ])   #补充文件
                else:
                    chkPath(r'.\gmlog')
                    self.file[filename] = open(r'.\gmlog\%s'%filename,'wb')
                    self.file[filename].write(r_pack[2][filename_len + 16 : ])
            elif r_pack[1] == 0x10ff:
                filename_len = unpack('<H',r_pack[2][14 : 16])[0]
                filename = r_pack[2][16 : filename_len + 16]
                if filename in self.file.keys():
                    self.file[filename].close()
                    del(self.file[filename])
                    self.broadcast.send(mylib.package.packCltEnd())
                
    def dispense(self, package):
        global CLTLIST
        for ip in CLTLIST:     #调出0x0001包中所存在的目的地址
            if ip in CHList.keys():     #与正连接的客户端列表进行比较
                CHList[ip].send(package)
                LOG.info('send to TestManage %s'%ip)
            else:
                info = '%s connecting failed ...'%ip
                LOG.info(info)
                self.broadcast.send(mylib.package.pack2(info))
                self.chkEnd(ip)

    def chkEnd(self, addr):
        global CLTLIST, CONTROL
        if addr in CLTLIST:     #当客户端列表为空时，可以发送控制端收尾指令
            CLTLIST.remove(addr)
            if not CLTLIST and CONTROL:
                CONTROL.send(self.e_pack)

    def getCltList(self, r_pack):
        global CLTLIST, CONTROL
        cltstring_len = int(unpack('<H', r_pack[2][14:16])[0])
        if cltstring_len == 0xffff:
            CLTLIST = [ip for ip in CHList.keys() if ':' in ip]   #没有':'则为virtual_message的链接,需要排除
            cltstring_len = 0
        elif cltstring_len > 0xf000:
            CLTLIST = [ip for ip in CHList.keys() if ':' in ip]
            cltstring_len = cltstring_len - 0xf000
            cltstring = r_pack[2][16 : 16 + cltstring_len]
            for i in range(0, cltstring_len, 6):
                port = ord(cltstring[i+4]) * 256 + ord(cltstring[i+5])
                if port:
                    ip = '%s.%s.%s.%s:%s'%(ord(cltstring[i]),
                                           ord(cltstring[i+1]),
                                           ord(cltstring[i+2]),
                                           ord(cltstring[i+3]), 
                                           port)
                    if ip in CLTLIST:
                        CLTLIST.remove(ip)
                else:
                    ip = '%s.%s.%s.%s:'%(ord(cltstring[i]),
                                        ord(cltstring[i+1]),
                                        ord(cltstring[i+2]),
                                        ord(cltstring[i+3]))
                    tempCLTLIST = CLTLIST[:]
                    for addr in tempCLTLIST:
                        if ip in addr:
                            CLTLIST.remove(addr)
        else:    
            cltstring = r_pack[2][16 : 16 + cltstring_len]
            for i in range(0, cltstring_len, 6):
                port = ord(cltstring[i+4]) * 256 + ord(cltstring[i+5])
                if port:
                    ip = '%s.%s.%s.%s:%s'%(ord(cltstring[i]),
                                           ord(cltstring[i+1]),
                                           ord(cltstring[i+2]),
                                           ord(cltstring[i+3]), 
                                           port)
                    tempCLTLIST = [addr for addr in CHList.keys() if ip == addr]
                else:
                    ip = '%s.%s.%s.%s:'%(ord(cltstring[i]),
                                        ord(cltstring[i+1]),
                                        ord(cltstring[i+2]),
                                        ord(cltstring[i+3]))
                    tempCLTLIST = [addr for addr in CHList.keys() if ip in addr]
                if tempCLTLIST:
                    CLTLIST += tempCLTLIST
                else:
                    result = '%s connecting failed...\n'%ip
                    s_pack = mylib.package.pack2(result)
                    CONTROL.send(s_pack)
        m_pack = r_pack[2][16 + cltstring_len : ]
        s_pack = pack('<HLHHL', 
                      r_pack[0] - cltstring_len + 16,    #16 = 18(myIP) - 2
                      0xAAAC, 
                      r_pack[0] - cltstring_len + 16, 
                      r_pack[1], 
                      0)
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
        super(VirtualMessage_to_Client, self).__init__(sock, 
                                                       addr, 
                                                       settings.VirtualMessagetoClient.magicCode, 
                                                       settings.VirtualMessagetoClient.heartCode)
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()
        
        self.task_chkHeart = stackless.tasklet(self.chkHeart)(30)
        self.task_receive = stackless.tasklet(self.receive)()
        
        self.uid = None
        self.sid = None
        self.user = None

    def chkHeart(self, time):
        while (not self.death) and self.switch:
            self.death = True
            SLEEP.delay_caller(time)
        if self.switch:
            LOG.error('%s %s_%s GMClient heart time out !'%(self.address, self.user, self.uid))
            self.exit()

    def exit(self):
        self.broadcast.close()
        self.heart.close()
        self.net_to_parse.close()
        self.switch = False
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        if self.uid in CHList.keys():
            if self.broadcast in CHList[self.uid]:
                CHList[self.uid].remove(self.broadcast)
            if len(CHList[self.uid]) <= 1:
                self.do_logout()
        LOG.info('%s GMClient exit...'%self.address)

    def listen_message(self):
        while self.switch:
            try:
                r_pack = self.net_to_parse.receive() 
                if r_pack[1] == 0x9006:
                    LOG.debug('received head from GMClient %s_%s_%s : [%d, %2x]'%(self.user, 
                                                                                  self.uid, 
                                                                                  self.address, 
                                                                                  r_pack[0], 
                                                                                  r_pack[1]))
                else:
                    LOG.info('received head from GMClient %s_%s_%s : [%d, %2x]'%(self.user, 
                                                                                 self.uid, 
                                                                                 self.address, 
                                                                                 r_pack[0], 
                                                                                 r_pack[1]))
                LOG.debug('received package from GMClient %s_%s_%s : '%(self.user, 
                                                                        self.uid, 
                                                                        self.address), 
                          r_pack[2])
                if r_pack[1] == 0x9001:
                    pbr = Response()
                    msg = SocketLoginMessage()
                    msg.ParseFromString(r_pack[2][14:])
                    user = msg.userName
                    LOG.debug('receive login_msg from GMClient %s : %s'%(self.address,
                                                                         msg))
                    if msg.code == 1:
                        if user in LoginInfo.keys():    #virtual login
                            sid = LoginInfo[user]
                            url = '%s/user.tcplogin/?alt=pbbin&sid=%s&service=msg'%(settings.APPSERVER, 
                                                                                    sid)
                            r_pack[2] = urlopen(url).read()
                            LOG.info('%s_%s GMClient send http request : %s'%(user,
                                                                              self.address, 
                                                                              url))
                            pbr.ParseFromString(r_pack[2])
                            LOG.info('%s_%s GMClient receive http response : %s'%(user, 
                                                                                  self.address, 
                                                                                  pbr))
                            if pbr.code == 200000:
                                self.user = user
                                self.uid = str(pbr.userTCPLogin.uid)
                                CHList[self.uid].append(self.broadcast)
                                LOG.info('%s_%s_%s GMClient double logined ...'%(self.user, 
                                                                                 self.uid, 
                                                                                 self.address))
                            else:
                                #此时sid已经过期用sid登出是没有意义的
                                del(LoginInfo[user])
                                LOG.error('%s_%s GMClient double logined failed !'%(user, 
                                                                                    self.address))
                        else:
                            url = '%s/user.tcplogin/?alt=pbbin&username=%s&password=%s&service=msg'%(settings.APPSERVER, 
                                                                                                     user, 
                                                                                                     msg.password)
                            r_pack[2] = urlopen(url).read()
                            LOG.info('%s_%s GMClient send http request: %s'%(user, 
                                                                             self.address, 
                                                                             url))
                            pbr.ParseFromString(r_pack[2])
                            LOG.info('%s_%s GMClient receive http response: %s'%(user, 
                                                                                 self.address, 
                                                                                 pbr))
                            if pbr.code == 200000:
                                self.user = user
                                self.uid = str(pbr.userTCPLogin.uid)
                                self.sid = pbr.userTCPLogin.sid
                                CHList[self.uid] = [self.broadcast]
                                LoginInfo[user] = self.sid
                                LOG.info('%s_%s_%s GMClient logined ...'%(self.user, 
                                                                          self.uid, 
                                                                          self.address))
                            else:
                                LOG.error('%s_%s_%s GMClient login failed : %s'%(self.user, 
                                                                                 self.uid, 
                                                                                 self.address, 
                                                                                 pbr))
                        self.broadcast.send(mylib.package.make_response_clt(r_pack[2]))
                    elif msg.code == 3:
                        self.do_logout()
                else:
                    LOG.warning('unknow package from GMClient %s_%s_%s : %x'%(self.user, 
                                                                              self.uid, 
                                                                              self.address, 
                                                                              r_pack[1]))
            except :
                LOG.error('listen message error from GMClient %s_%s_%s : %x, %s'%(self.user, 
                                                                                  self.uid, 
                                                                                  self.address, 
                                                                                  r_pack[1], 
                                                                                  r_pack.__repr__()))
                LOG.error(format_exc())

    def do_logout(self):
        if self.uid in CHList.keys() and self.user in LoginInfo.keys():
            while True:
                pbr = Response()
                url = '%s/user.tcplogout/?alt=pbbin&sid=%s&service=msg'%(settings.APPSERVER,
                                                                         self.sid)
                mdata = urlopen(url).read()
                LOG.info('%s_%s_%s GMClient send http request: %s'%(self.user, 
                                                                    self.uid, 
                                                                    self.address, 
                                                                    url))
                pbr.ParseFromString(mdata)
                LOG.info('%s_%s_%s GMClient receive http response: %s'%(self.user, 
                                                                        self.uid, 
                                                                        self.address, 
                                                                        pbr))
                if pbr.code == 200000:
                    del(LoginInfo[self.user])
                    LOG.info('%s_%s_%s GMClient logouted...'%(self.user, 
                                                              self.uid, 
                                                              self.address))
                    self.user = None
                    for ch in CHList[self.uid]:
                        ch.send(mylib.package.make_response_clt(mdata))
                        CHList[self.uid].remove(ch)
                    if len(CHList[self.uid]) <= 1:
                        del(CHList[self.uid])
                    break
                else:
                    LOG.error('%s_%s_%s GMClient logout failed : %s'%(self.user, 
                                                                      self.uid, 
                                                                      self.address, 
                                                                      pbr))
                    for ch in CHList[self.uid]:
                        ch.send(mylib.package.make_response_clt(mdata))
                    SLEEP.delay_caller(5)
                        

class VirtualMessage_to_Service(net):
    def __init__(self, sock, addr):
        super(VirtualMessage_to_Service, self).__init__(sock, 
                                                        addr, 
                                                        settings.VirtualMessagetoService.magicCode, 
                                                        settings.VirtualMessagetoService.heartCode)
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()
        self.task_receive = stackless.tasklet(self.receive)()
        self.package = None
        
    def exit(self):
        self.broadcast.close()
        self.heart.close()
        self.net_to_parse.close()
        self.switch = False
        LOG.info('%s APP Service exit...'%self.address)

    def listen_message(self):
        msg = Msg()
        while self.switch:
            try:
                r_pack = self.net_to_parse.receive()  #r_pack[0] 包长度, r_pack[1]magic_code, r_pack[2]收到的完成数据包
                LOG.debug('received package from APP Service %s : '%self.address, 
                          r_pack[2])
                LOG.info('APP Service %s code: %x'%(self.address, 
                                                    r_pack[1]))
                if r_pack[1] == 0x7001:
                    receivers_list = self.getReceivers(r_pack[2])
                    self.broadcast.send(mylib.package.make_response_app(0))
                    msg.ParseFromString(self.package)
                    for receiver in receivers_list:
                        if str(receiver) in CHList.keys():
                            LOG.info('APP Service %s transmit to receiver %s : '%(self.address,
                                                                                  receiver), 
                                     self.package)
                            s_string = mylib.package.make_transmit(self.package)
                            for ch in CHList[str(receiver)]:
                                ch.send([s_string,msg.uuid])
                            
                else:
                    LOG.warning('unknow code from APP Service %s : %x'%(self.address, 
                                                                        r_pack[1]))
            except :
                LOG.error('listen message error from APP Service %s : %x, %s'%(self.address,
                                                                               r_pack[1], 
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
    sock.bind(('', settings.TestManage.port))
    sock.listen(5)
    while RUN:
        sockclient,addr = sock.accept()
        LOG.info('%s:%s TestManage connected...'%addr)
        test = testManage(sockclient, addr)
        TASK_TEST.append(stackless.tasklet(test.listen_message)())
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

def CltThread():
    global RUN, TASK_CLT 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', settings.VirtualMessagetoClient.port))
    sock.listen(5)
    while RUN:
        sockclient, addr = sock.accept()
        LOG.info('%s:%s Clt connected...'%addr)
        clt = VirtualMessage_to_Client(sockclient, addr)
        TASK_CLT.append(stackless.tasklet(clt.listen_message)())
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
        
def APPThread():
    global RUN, TASK_APP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', settings.VirtualMessagetoService.port))
    sock.listen(1)
    while RUN:
        sockclient, addr = sock.accept()
        LOG.info('%s:%s APP service connected...'%addr)
        srv = VirtualMessage_to_Service(sockclient, addr)
        TASK_APP.append(stackless.tasklet(srv.listen_message)())
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

if __name__ == '__main__':
    from os import system
    system('title VirtualMessage Service')
    roachlib.stacklesssocket.install()
    import socket
    if settings.VirtualMessage:
        LOG.info('virtualmessage runing...')
        TASK_APP.append(stackless.tasklet(APPThread)())
        TASK_CLT.append(stackless.tasklet(CltThread)())
    TASK_TEST.append(stackless.tasklet(TestThread)())
    while RUN:
        stackless.run()