#coding=gbk

import sys
sys.path.append('..\\lib')

import urllib, stackless, re, struct

from log import LOG
import package
from settings import *

from protobuf.msg_base_pb2 import Msg
from protobuf.res_base_pb2 import Response
from protobuf.soc_login_pb2 import SocketLoginMessage
import stacklesssocket
import scheduler

RUN = True

CHList = {}   #链接上此服务器的client的广播channel列表
CLTLIST = []   #一次case的client列表由0x0001包中获得
CONTROL = None  #一次case的控制端的广播channel
LoginInfo = {}  #虚拟登录时返回的登录信息

SLEEP = scheduler.DelayScheduler()  #stackless的sleep
SLEEP.start()



class net(object):
    def __init__(self, sock, addr):
        global LOG
        self.switch = True
        self.do = None
        self.address = addr
        self.sock = sock
        self.death = False
        self.windage = 0   #virtual message包长度字段长度与testmanage包长度字段长度不同，用来修正
        self.headformat = '<HL'
        self.heart = stackless.channel()
        self.broadcast = stackless.channel()
        self.net_to_parse = stackless.channel()
    
    def receive(self):
        stackless.tasklet(self.threadBroadcast)()
        try:
            pdata = ''
            while self.switch:
                LOG.info('%s : %s listening...'%self.address)
                rdata = self.sock.recv(1000)
                LOG.debug('receive raw_string from %s : %s : %s'%(self.address[0], 
                                                                  self.address[1], 
                                                                  rdata.__len__()))
                if not rdata:
                    LOG.info('%s : %s disconnect...'%self.address)
                    self.exit()
                    break
                else:
                    self.death = False
                    pdata = self.parseHead('%s%s'%(pdata, rdata))
        except Exception, e:
            LOG.error('%s : %s net error : %s'%(self.address[0],
                                                self.address[1],
                                                str(e)))
            self.exit()
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack(self.headformat, data[:6])
            if not self.do:
                if head[1] in [0xABDE,0xABCD]:
                    #stackless.tasklet(self.chkHeart)()
                    self.do = virtualMessage(self.broadcast, self.net_to_parse, self.address)
                    self.windage = 2
                    stackless.tasklet(self.do.listen_message)()
                else:
                    self.headformat = '<LH'
                    head = struct.unpack(self.headformat, data[:6])
                    if head[1] <= 6 and head[1] > 0 :  #确保在0x0001~0x0006之间
                        stackless.tasklet(self.reHeart)()
                        stackless.tasklet(self.chkHeart)()
                        self.do = testManage(self.broadcast, self.net_to_parse, self.address)
                        CHList['%s:%s'%self.address] = self.broadcast
                        stackless.tasklet(self.do.listen_message)()
            if head[0] + self.windage <= len(data):
                mdata = data[ : head[0] + self.windage]
                data = data[head[0] + self.windage : ]
                #TODO: 检查返回数据的格式
                if head[1] == 0x0006:
                    self.heart.send(mdata)
                else:
                    self.net_to_parse.send([head[0], head[1], mdata])
                LOG.info('received handler from %s : %s : [%d, %2x]'%(self.address[0],
                                                                      self.address[1],
                                                                      head[0], 
                                                                      head[1]))
                LOG.debug('received package from %s : %s : %s'%(self.address[0],
                                                                self.address[1],
                                                                mdata.__len__()))
                data = self.parseHead(data)
        return data

    def threadBroadcast(self):
        while self.switch:
            try:
                rdata = self.broadcast.receive()
                if rdata == 'exit':
                    self.exit()
                    LOG.info('%s : %s be exit!'%self.address)
                    self.broadcast.close()
                    self.sock.close()
                    break
                else:
                    self.sock.sendall(rdata)
                    LOG.debug('send to %s : %s : %s'%(self.address[0], 
                                                      self.address[1], 
                                                      rdata.__len__()))
            except Exception, e:
                LOG.error('%s : %s broadcast error...'%self.address)
                if e.args == 9:
                    LOG.error('%s : %s Socket has be closed! Send package failed : %s'%(self.address[0], 
                                                                                        self.address[1], 
                                                                                        rdata.__len__()))
                else:
                    LOG.error('%s : %s'%(str(e),
                                         rdata.__len__()))
                self.exit()
    
    def chkHeart(self):
        while not (self.death and self.switch):
            self.death = True
            SLEEP.delay_caller(30)
        if self.switch:
            LOG.error('%s : %s heart time out!'%self.address)
            self.exit()
    
    def reHeart(self):
#        self.sock.sendall(self.h_pack)
#        LOG.debug('send to %s : %s : %s'%(self.address[0], 
#                                          self.address[1], 
#                                          self.h_pack.__len__()))
        while self.switch:
            package = self.heart.receive()
            SLEEP.delay_caller(15)
            if self.switch:
                self.broadcast.send(package)
       
    def exit(self):
        if self.switch:
            self.switch = False
            LOG.info('%s : %s net exit...'%self.address)
            if self.do:
                self.net_to_parse.send('exit')

class testManage(object):
    def __init__(self, broadcast, net_to_parse, address):
        self.e_pack = package.packCtrlEnd()
        self.net_to_parse = net_to_parse
        self.broadcast = broadcast
        self.address = address
        self.switch = True
        self.cltlist = []
    
    def listen_message(self):
        global CLTLIST, CONTROL, LOG, RUN
        while self.switch:
            r_pack = self.net_to_parse.receive()
            if r_pack == 'exit':
                self.switch = False
                if '%s:%s'%self.address in CHList.keys():
                    del(CHList['%s:%s'%self.address])
                    self.chkEnd('%s:%s'%self.address)
                else:
                    self.dispense('exit')
                self.net_to_parse.close()
                LOG.info('%s : %s test_manage exit...'%self.address)
                break
            result = ''
            if r_pack[1] == 0x0001:
                CONTROL = self.broadcast
                del(CHList['%s:%s'%self.address])
                s_pack = self.getCltList(r_pack)
                for ip in self.cltlist:
                    fail = True
                    for addr in CHList.keys():
                        print self.cltlist
                        print ip
                        print addr
                        if ':' in ip and ip == addr:
                            CLTLIST.append(ip)
                            CHList[ip].send('%sip:%s'%(s_pack, self._myIP(re.split(':', ip)[0])))
                            LOG.info('send to %s'%ip)
                            fail = False
                            break
                        elif (not ':' in ip) and ip in addr:
                            CLTLIST.append(addr)
                            CHList[addr].send('%sip:%s'%(s_pack, self._myIP(ip)))
                            LOG.info('send to %s'%addr)
                            fail = False
                    if fail:
                        result = '%s%s connecting faild...\n'%(result, ip)
                        s_pack = package.pack2(result)
                        self.broadcast.send(s_pack)
                if not CLTLIST:
                    CONTROL.send(self.e_pack)
            elif r_pack[1] in [0x0002, 0x0004]:
                CONTROL.send(r_pack[2])
            elif r_pack[1] in [0x0003, 0xffff]:
                self.dispense(r_pack[2])
            elif r_pack[1] == 0x0005:
                del(CHList['%s:%s'%self.address])
                ips = ''
                for ip in CHList.keys():
                    if ':' in ip:
                        ch_len = 1
                    else:
                        ch_len = CHList[ip].__len__()
                    ips = '%s%s %s\n'%(ips, ip, ch_len)
                LOG.info(ips)
                result = '%s%s'%(result, ips)
                s_pack = package.pack2(result)
                s_pack = '%s%s'%(s_pack, self.e_pack)
                self.broadcast.send(s_pack)
            elif r_pack[1] == 0xff00:
                self.chkEnd('%s:%s'%self.address)
            elif r_pack[1] == 0xf0f0:   #关闭服务器
                package.pack2('The End ...')
                s_pack = '%s%s'%(s_pack, self.e_pack)
                self.broadcast.send(s_pack)
                try:
                    for ch_key in CHList.keys():
                        if ':' in ch_key:
                            CHList[ch_key].send('exit')
                        else:
                            for uid_ch in CHList[ch_key]:
                                uid_ch.send('exit')
                except Exception, e:
                    pass
                RUN = False
#            模拟登陆
            elif r_pack[1] == 0xABDE:    #用来借助自动脚本关闭war3进程所必须的登录
                msg = SocketLoginMessage()
                msg.ParseFromString(r_pack[2][14:])
                LOG.debug(msg)
                if msg.userName in LoginInfo.keys():    #virtual login
                    mdata = LoginInfo[msg.userName]
                    pbr = Response()
                    pbr.ParseFromString(mdata)
                    user = msg.userName
                    uid = str(pbr.userTCPLogin.uid)
                    CHList[uid].append(self.broadcast)
                    LOG.info('%s_%s double Logined'%(user,uid))
                    self.broadcast.send(package.make_response_clt(mdata))
                
    def dispense(self, package):
        global CLTLIST
        for ip in CLTLIST:     #调出0x0001包中所存在的目的地址
            if ip in CHList.keys():     #与正连接的客户端列表进行比较
                CHList[ip].send(package)
                LOG.info('send to %s'%ip)
            else:
                info = '%s connecting faild ...'%ip
                LOG.info(info)
                result = '%s%s\n'%(result, info)
                s_pack = package.pack2(result)
                self.broadcast.send(s_pack)
                self.chkEnd(ip)

    def chkEnd(self, addr):
        global CLTLIST, CONTROL
        if addr in CLTLIST:     #当客户端列表为空时，可以发送控制端收尾指令
            CLTLIST.remove(addr)
            if not CLTLIST:
                CONTROL.send(package.pack2('%s connecting faild ...'%addr))
                CONTROL.send(self.e_pack)

    def getCltList(self, r_pack):
        global CLTLIST
        cltstring_len = int(struct.unpack('<H', r_pack[2][6:8])[0])
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
        s_pack = struct.pack('<LH', 
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

class virtualMessage(object):
    def __init__(self, broadcast, net_to_parse, address):
        global LOG
        self.net_to_parse = net_to_parse
        self.broadcast = broadcast
        self.address = address
        self.switch = True
        self.uid = None
        self.user = ''
        self.sid = None
    
    def listen_message(self):
        while self.switch:
            try:
                r_pack = self.net_to_parse.receive()
                LOG.debug('received package from %s : %s'%(self.user, str(r_pack.__len__())))
                if r_pack == 'exit':
                    self.net_to_parse.close()
                    if self.uid and self.uid in CHList.keys():
                        self.do_logout()
                    break
                mdata = r_pack[2]
                cmd = struct.unpack("<H", mdata[8 : 10])[0]
                LOG.info('%s code: %x'%(self.user, cmd))
                if cmd == 0x7001:
                    self.broadcast.send(package.make_response_app(0))
                    receivers_len = struct.unpack("<H", mdata[14 : 16])[0]
                    receivers_string = mdata[16 : receivers_len * 4 + 16]
                    mdata = mdata[receivers_len * 4 + 16 : ]
                    receivers_list = struct.unpack('<%sL'%receivers_len, receivers_string)
                    for receiver in receivers_list:
                        LOG.info('%s transmit to receiver: %s'%(self.user, str(receiver)))
                        if str(receiver) in CHList.keys():
                            for ch in CHList[str(receiver)]:
                                ch.send(package.make_transmit(mdata))
                elif cmd == 0x9001:
                    pbr = Response()
                    msg = SocketLoginMessage()
                    msg.ParseFromString(mdata[14:])
                    LOG.debug(msg)
                    if msg.code == 1:
                        if msg.userName in LoginInfo.keys():    #virtual login
                            mdata = LoginInfo[msg.userName]
                            pbr.ParseFromString(mdata)
                            self.user = msg.userName
                            self.uid = str(pbr.userTCPLogin.uid)
                            self.sid = pbr.userTCPLogin.sid
                            CHList[self.uid].append(self.broadcast)
                            LOG.info('%s_%s double Logined'%(self.user,self.uid))
                        else:
                            url = '%s/user.tcplogin/?alt=pbbin&username=%s&password=%s&service=msg'%(APPSERVER, 
                                                                                                    msg.userName, 
                                                                                                    msg.password)
                            LOG.info('%s send http request: %s'%(self.user, url))
                            mdata = urllib.urlopen(url).read()
                            pbr.ParseFromString(mdata)
                            LOG.info('%s receive http response: %s'%(self.user, pbr))
                            if pbr.code == 200000:
                                self.user = msg.userName
                                self.uid = str(pbr.userTCPLogin.uid)
                                self.sid = pbr.userTCPLogin.sid
                                CHList[self.uid] = [self.broadcast]
                                LoginInfo[msg.userName] = mdata
                                LOG.info('%s_%s Logined...'%(self.user,self.uid))
                            else:
                                LOG.error('%s_%s Login error: %s'%(self.user,self.uid,pbr))
                        self.broadcast.send(package.make_response_clt(mdata))
                    elif msg.code == 3:
                        self.do_logout()
                elif cmd == 0x9006:  #return 0x9008 heart for flash
                    LOG.debug('heart package from %s ...'%self.user)
                else:
                    LOG.warning('unknow code from %s : %s'%(self.user, cmd))
            except Exception, e:
                LOG.error('listen message error from %s : %s'%(self.user, str(r_pack)))
                LOG.error(str(e))

    def do_logout(self):
        pbr = Response()
        url = '%s/user.tcplogout/?alt=pbbin&sid=%s'%(APPSERVER,
                                                     self.sid)
        mdata = urllib.urlopen(url).read()
        LOG.info('%s send http request: %s'%(self.user, url))
        pbr.ParseFromString(mdata)
        LOG.info('%s receive http response: %s'%(self.user, pbr))
        for ch in CHList[self.uid]:
            if not ch == self.broadcast:
                ch.send(package.make_response_clt(mdata))
        if pbr.code == 200000:
            del(LoginInfo[self.user])
            del(CHList[self.uid])
            self.switch = False
            LOG.info('%s_%s Logouted...'%(self.user,self.uid))
            self.broadcast.close()
        else:
            LOG.error('%s_%s Logout error:%s'%(self.user,self.uid,pbr))

def cltthread():
    global RUN
    LOG.info('runing...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',CLT_PORT))
    sock.listen(1)
    while RUN:
        sockclient,addr = sock.accept()
        LOG.info('%s : %s connected...'%addr)
        clt = net(sockclient, addr)
        stackless.tasklet(clt.receive)()
    sock.close()
        
def appthread():
    global LOG, RUN
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',APP_PORT))
    sock.listen(1)
    while RUN:
        sockclient,addr = sock.accept()
        LOG.info('%s : %s APP service connected...'%addr)
        srv = net(sockclient, addr)
        stackless.tasklet(srv.receive)()
    sock.close()

if __name__ == '__main__':
    stacklesssocket.install()
    import socket
    stackless.tasklet(appthread)()
    stackless.tasklet(cltthread)()
    while RUN:
        stackless.run()
    