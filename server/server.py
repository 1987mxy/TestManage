#coding=gbk
import sys
sys.path.append('..\\lib')
import urllib
import stackless
import re
import struct
import log
import stacklesssocket
from settings import *

from protobuf.msg_base_pb2 import Msg
from protobuf.res_base_pb2 import Response

from protobuf.soc_login_pb2 import SocketLoginMessage

import scheduler

CHList = {}
LoginInfo = {}
CONTROL = None
APPSRV = None
LOG = None

SLEEP = scheduler.DelayScheduler()

class net(object):
    def __init__(self, sock, addr):
        global LOG
        self.switch = True
        self.do = None
        self.address = addr
        self.sock = sock
        self.windage = 0   #virtual message包长度字段长度与testmanage包长度字段长度不同，用来修正
        self.death = False
        self.headformat = '<HL'
        self.broadcast = stackless.channel()
        self.net_to_parse = stackless.channel()
        CHList['%s:%s'%self.address]=self.broadcast
        stackless.tasklet(self.threadBroadcast)()
    
    def receive(self):
        try:
            pdata = ''
            while self.switch:
                rdata = self.sock.recv(4096)
                self.death = False
                LOG.debug('receive raw_string from %s:%s : %s'%(self.address[0], 
                                                           self.address[1], 
                                                           rdata.__repr__()))
                if not rdata:
                    LOG.info('%s:%s disconnect...'%self.address)
                    self.exit()
                else:
                    pdata = self.parseHead('%s%s'%(pdata, rdata))
        except Exception, e:
            LOG.error('%s:%s net error...'%self.address)
            LOG.error(e.message)
            self.exit()
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack(self.headformat, data[:6])
            if not self.do:
                if head[1] in [0xABDE,0xABCD]:
                    self.do = virtualMessage(self.broadcast, self.net_to_parse)
                    self.sock.settimeout = 30
                    self.windage = 2
                    del(CHList['%s:%s'%self.address])
                    if head[1] == 0xABCD:
                        stackless.tasklet(self.heart)()
                else:
                    self.headformat = '<LH'
                    head = struct.unpack(self.headformat, data[:6])
                    self.do = testManage(self.broadcast, self.net_to_parse, self.address)
                stackless.tasklet(self.do.listen_message)()
            if head[0] + self.windage <= len(data):
                mdata = data[ : head[0] + self.windage]
                data = data[head[0] + self.windage : ]
                #TODO: 检查返回数据的格式
                self.net_to_parse.send([head[0], head[1], mdata])
                LOG.info('received handler from %s:%s : [%d, %2x]'%(self.address[0],
                                                                    self.address[1],
                                                                    head[0], 
                                                                    head[1]))
                LOG.debug('received package from %s:%s : %s'%(self.address[0],
                                                              self.address[1],
                                                              mdata.__repr__()))
                data = self.parseHead(data)
        return data

    def threadBroadcast(self):
        while self.switch:
            try:
                rdata = self.broadcast.receive()
                self.sock.sendall(rdata)
                LOG.debug('send to %s:%s : %s'%(self.address[0], 
                                                self.address[1], 
                                                rdata.__repr__()))
            except Exception, e:
                LOG.error('%s:%s broadcast error...'%self.address)
                if e.args == 9:
                    LOG.error('%s:%s Socket has be closed! Send package failed: %s'%(self.address[0], 
                                                                                     self.address[1], 
                                                                                     rdata.__repr__()))
                else:
                    LOG.error(e.message)
    
    def heart(self):
        while not self.death:
            self.death = True
            SLEEP.delay_caller(30)
        self.exit()
       
    def exit(self):
        addr = '%s:%s'%self.address
        self.net_to_parse.send('exit')
        if addr in CHList.keys():
            del(CHList[addr])
        self.switch = False
        self.sock.close()

class testManage(object):
    def __init__(self, broadcast, net_to_parse, address):
        self.net_to_parse = net_to_parse
        self.broadcast = broadcast
        self.address = address
        self.client_len = 0
        self.switch = True
        self.cltlist = []
    
    def listen_message(self):
        global CONTROL, LOG
        while self.switch:
            package = self.net_to_parse.receive()
            if package == 'exit':
                self.switch = False
                self.broadcast.close()
                self.net_to_parse.close()
                break
            result = ''
            if package[1] == 0x0001:
                CONTROL = self.broadcast
                s_pack = self.getCltList(package)
                del(CHList['%s:%s'%self.address])
                for ip in self.cltlist:
                    fail = True
                    for addr in CHList.keys():
                        if ':' in ip and ip == addr:
                            CHList[ip].send('%sip:%s'%(s_pack, self.myIP(re.split(':', ip)[0])))
                            self.client_len += 1
                            fail = False
                            break
                        elif (not ':' in ip) and ip in addr:
                            CHList[addr].send('%sip:%s'%(s_pack, self.myIP(ip)))
                            self.client_len += 1
                            fail = False
                    if fail:
                        self.cltlist.remove(ip)
                        result += '%s connecting faild...\n'%ip
                        s_pack = self.packResult(result)
                        s_pack += self.packEnd()
                        self.broadcast.send(s_pack)
            elif package[1] in [0x0002, 0x0004]:
                CONTROL.send(package[2])
            elif package[1] in [0x0003, 0xffff]:
                self.dispense(package[2])
            elif package[1] == 0x0005:
                del(CHList['%s:%s'%self.address])
                for ip in CHList.keys():
                    result += '%s\n'%ip
                s_pack = self.packResult(result)
                s_pack += self.packEnd()
                self.broadcast.send(s_pack)
            elif package[1] == 0xff00:
                self.client_len -= 1
                if self.client_len <= 0:
                    CONTROL.send(package[2])
                    self.client_len = 0
                
    def dispense(self, package):
        for ip in self.cltlist:
            fail = True
            for addr in CHList.keys():
                if ':' in ip and ip == addr:
                    CHList[ip].send(package)
                    fail = False
                elif (not ':' in ip) and ip in addr:
                    CHList[addr].send(package)
                    fail = False
            if fail:
                self.cltlist.remove(ip)
                result += '%s connecting faild...\n'%ip
                s_pack = self.packResult(result)
                s_pack += self.packEnd()
                self.broadcast.send(s_pack)
                    
    
    def packResult(self, result):
        result += '='*30
        package = struct.pack('<LH', 
                              result.__len__() + 6, 
                              0x0002)
        package += result
        return package
    
    def packEnd(self):
        package = struct.pack('<LH', 
                              6, 
                              0xff00)
        return package

    def getCltList(self, r_pack):
        cltstring_len = int(struct.unpack('<H', r_pack[2][6:8])[0])
        cltstring = r_pack[2][8 : 8 + cltstring_len]
        m_pack = r_pack[2][8 + cltstring_len : ]
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
        s_pack = struct.pack('<LH', 
                            r_pack[0] - cltstring_len + 16,     #16 = 18 - 2
                            r_pack[1])
        s_pack += m_pack
        return s_pack
    
    def myIP(self, ip):
        ips = ip.split('.')
        tempip = ''
        for i in ips:
            i = '*'*(3-i.__len__()) + i
            tempip += i + '.'
        return tempip[:tempip.__len__()-1]
    
class virtualMessage(object):
    def __init__(self, broadcast, net_to_parse):
        global LOG
        self.net_to_parse = net_to_parse
        self.broadcast = broadcast
        self.switch = True
        self.uid = None
        self.user = ''
        self.sid = None
    
    def listen_message(self):
        while self.switch:
            try:
                package = self.net_to_parse.receive()
                LOG.debug('received package from %s: %s'%(self.user, str(package.__repr__())))
                if package == 'exit':
                    if self.uid and self.uid in CHList.keys():
                        self.do_logout()
                    break
                mdata = package[2]
                cmd = struct.unpack("<H", mdata[8 : 10])[0]
                LOG.info('%s code: %x'%(self.user, cmd))
                if cmd == 0x7001:
                    self.broadcast.send(self.make_response_app(0))
                    receivers_len = struct.unpack("<H", mdata[14 : 16])[0]
                    receivers_string = mdata[16 : receivers_len * 4 + 16]
                    mdata = mdata[receivers_len * 4 + 16 : ]
                    receivers_list = struct.unpack('<%sL'%receivers_len, receivers_string)
                    for receiver in receivers_list:
                        LOG.info('%s transmit to receiver: %s'%(self.user, receiver.__repr__()))
                        if receiver in CHList.keys():
                            for ch in CHList[receiver]:
                                ch.send(self.make_transmit(mdata))
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
                            self.uid = pbr.userTCPLogin.uid
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
                                self.uid = pbr.userTCPLogin.uid
                                self.sid = pbr.userTCPLogin.sid
                                CHList[self.uid] = [self.broadcast]
                                LoginInfo[msg.userName] = mdata
                                LOG.info('%s_%s Logined...'%(self.user,self.uid))
                            else:
                                LOG.error('%s_%s Login error: %s'%(self.user,self.uid,pbr))
                        self.broadcast.send(self.make_response_clt(mdata))
                    elif msg.code == 3:
                        self.do_logout()
                elif cmd == 0x9006:  #return 0x9008 heart for flash
                    LOG.debug('heart package from %s ...'%self.user)
                else:
                    LOG.warning('unknow code from %s : %s'%(self.user, cmd))
            except Exception, e:
                LOG.error('listen message error from %s : %s'%(self.user, str(package)))
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
            ch.send(self.make_response_clt(mdata))
        if pbr.code == 200000:
            del(CHList[self.uid])
            del(LoginInfo[self.user])
            self.switch = False
            LOG.info('%s_%s Logouted...'%(self.user,self.uid))
            self.broadcast.close()
            self.net_to_parse.close()
        else:
            LOG.error('%s_%s Logout error:%s'%(self.user,self.uid,pbr))

    def make_response_app(self, response_code):   
        #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4), response_code(2)
        message_pack_header_def='<HLHHLH'
        pack = struct.pack(message_pack_header_def,
                           struct.calcsize(message_pack_header_def) -2,
                           0xABCD,
                           struct.calcsize(message_pack_header_def) -2,
                           0x7002,
                           0,
                           response_code)
        return pack
    
    def make_response_clt(self, encoded):  #logined
        #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4)
        message_pack_header_def='<HLHHL'
        pack = '%s%s'%(struct.pack(message_pack_header_def,
                                   struct.calcsize(message_pack_header_def) -2 +len(encoded),
                                   0xABDE,
                                   struct.calcsize(message_pack_header_def) -2 +len(encoded),
                                   0x9002,
                                   0),
                       content)
        return pack
    
    def make_transmit(self, encoded):
        #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4)
        message_pack_header_def='<HLHHL'
        pack = "%s%s" %(struct.pack(message_pack_header_def,
                                    struct.calcsize(message_pack_header_def) -2 +len(encoded),
                                    0xABDE,
                                    struct.calcsize(message_pack_header_def) -2 +len(encoded),
                                    0x9003,
                                    0),
                        content)
        return pack

def cltthread():
    global LOG
    LOG.info('runing...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',CLT_PORT))
    sock.listen(1)
    while 1:
        sockclient,addr = sock.accept()
        LOG.info('%s:%s connecting...'%addr)
        clt = net(sockclient, addr)
        stackless.tasklet(clt.receive)()
        
def appthread():
    global LOG
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',APP_PORT))
    sock.listen(1)
    while 1:
        sockclient,addr = sock.accept()
        LOG.info('%s:%s service connected...'%addr)
        srv = net(sockclient, addr)
        stackless.tasklet(srv.receive)()

if __name__ == '__main__':
    log.run_log()
    LOG = log.error_log()
    stacklesssocket.install()
    import socket
    stackless.tasklet(cltthread)()
    stackless.tasklet(appthread)()
    while 1:
        stackless.run()