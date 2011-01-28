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

CHList = {}
LoginInfo = {}
CONTROL = None
APPSRV = None
LOG = None

class net(object):
    def __init__(self, sock, addr):
        global LOG
        self.switch = True
        self.do = None
        self.address = addr
        self.sock = sock
        self.windage = 0
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
                LOG.debug(rdata.__repr__())
                if not rdata:
                    LOG.debug('disconnect...%s:%s'%self.address)
                    self.exit()
                pdata = self.parseHead(pdata + rdata)
        except Exception, e:
            LOG.error('error...%s:%s'%self.address)
            LOG.error(str(e))
            self.exit()
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack(self.headformat, data[:6])
            if not self.do:
                if head[1] in [0xABDE,0xABCD]:
                    self.do = virtualMessage(self.broadcast, self.net_to_parse)
                    self.sock.settimeout = 30
                    self.windage = 2
                else:
                    self.headformat = '<LH'
                    head = struct.unpack(self.headformat, data[:6])
                    self.do = testManage(self.broadcast, self.net_to_parse)
                stackless.tasklet(self.do.listen_message)()
            if head[0] + self.windage <= len(data):
                mdata = data[ : head[0] + self.windage]
                data = data[head[0] + self.windage : ]
                #TODO: 检查返回数据的格式
                self.net_to_parse.send([head[0], head[1], mdata])
                LOG.debug('%s:%s received %d, %x, %s'%(self.address[0],
                                              self.address[1], 
                                              head[0], 
                                              head[1], 
                                              mdata.__repr__())
                        )
                data = self.parseHead(data)
        return data

    def threadBroadcast(self):
        while self.switch:
            try:
                rdata = self.broadcast.receive()
                self.sock.sendall(rdata)
                LOG.debug('%s:%s send %s'%(self.address[0], self.address[1], rdata.__repr__()))
            except Exception, e:
                if e.args() == 9:
                    LOG.error('Socket has be closed! Send package failed: %s'%rdata.__repr__())
                else:
                    LOG.error(e.message())
            
    def exit(self):
        addr = '%s:%s'%self.address
        self.net_to_parse.send('exit')
        if addr in CHList.keys():
            del(CHList[addr])
        self.switch = False
        self.sock.close()

class testManage(object):
    def __init__(self, broadcast, net_to_parse):
        self.net_to_parse = net_to_parse
        self.broadcast = broadcast
        self.switch = True
        self.cltlist = []
    
    def listen_message(self):
        global CLIENT,LOG
        while self.switch:
            package = self.net_to_parse.receive()
            LOG.debug(package.__repr__())
            if package[1] == 0x0001:
                s_pack = self.getCltList(package)
                CLIENT = self.broadcast
                for ip in self.cltlist:
                    for addr in CHList.keys():
                        if ip == re.split(':', addr)[0]:
                            CHList[ip].send('%sip:%s'%(s_pack, self.myIP(ip)))
                            result += '%s send...'%ip
                        else:
                            result += '%s connecting faild...\n%s\n'%(ip, '='*20)
                s_pack = self.packResult(result)
                s_pack += self.packEnd()
                self.broadcast.send(s_pack)
            elif package[1] == 0x0002:
                for ip in self.cltlist:
                    if ip in CHList.keys():
                        CHList[ip].send(package[2])
            elif package[1] == 0x0003:
                s_pack = self.getclient(package)
                for ip in self.cltlist:
                    if ip in CHList.keys():
                        CHList[ip].send(s_pack)
            elif package[1]== 0x0004:
                CONTROL.send(package[2])
            elif package[1] == 0x0005:
                for ip in CHList.keys():
                    result += ip
                s_pack = self.packResult(result)
                s_pack += self.packEnd()
                self.broadcast.send(s_pack)
            elif head[1] == 0xffff:
                for ip in self.cltlist:
                    if ip in CHList.keys():
                        CHList[ip].send(package[2])
                self.cltlist = []
                
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
                              0xffff)
        return package

    def getCltList(self, r_pack):
        cltstring_len = strcut.unpack('<H', r_pack[2][6:8])
        cltstring = r_pack[2][8 : 8 + cltstring_len]
        m_pack = r_pack[2][8 + cltstring_len : ]
        for i in range(cltstring_len,6):
            port = ord(cltstring[i+4]) * 256 + ord(cltstring[i+5])
            self.cltlist.append('%s.%s.%s.%s:%s'%(ord(cltstring[i]),ord(cltstring[i+1]),ord(cltstring[i+2]),ord(cltstring[i+3]), port))
        spack = struct.pack('<LH', 
                            r_pack[0] - cltstring_len + 16,     #16 = 18 - 2
                            r_pack[1])
        s_pack += m_pack
        return s_pack
    
    def myIP(ip):
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
        self.user = None
    
    def listen_message(self):
        while self.switch:
            try:
                package = self.net_to_parse.receive()
                if package == 'exit':
                    if self.uid and self.uid in CHList.keys():
                        self.do_logout()
                    break
                mdata = package[2]
                cmd = struct.unpack("<H", mdata[8 : 10])[0]
                LOG.debug('%x'%cmd)
                if cmd == 0x7001:
                    msg = Msg()
                    self.broadcast.send(self.make_response_app(0))
                    receivers_len = struct.unpack("<H", mdata[14 : 16])[0]
                    receivers_string = mdata[16 : receivers_len * 4 + 16]
                    mdata = mdata[receivers_len * 4 + 16 : ]
                    LOG.debug(mdata.__repr__())
                    LOG.debug('receivers_len:%s'%receivers_len)
                    receivers_list = struct.unpack('<%sL'%receivers_len, receivers_string)
                    for receiver in receivers_list:
                        LOG.debug('receiver:%s'%receiver.__repr__())
                        if receiver in CHList.keys():
                            for ch in CHList[receiver]:
                                ch.send(self.make_transfer(mdata))
                elif cmd == 0x9001:
                    pbr = Response()
                    from protobuf.soc_login_pb2 import SocketLoginMessage
                    msg = SocketLoginMessage()
                    msg.ParseFromString(mdata[14:])
                    LOG.debug(msg)
                    if msg.code == 1:
                        if msg.userName in LoginInfo.keys():    #virtual login
                            self.user = msg.userName
                            mdata = LoginInfo[msg.userName]
                            LOG.debug(mdata)
                            pbr.ParseFromString(mdata)
                            self.uid = pbr.userTCPLogin.uid
                            self.sid = pbr.userTCPLogin.sid
                            CHList[self.uid].append(self.broadcast)
                        else:
                            url = '%s/user.tcplogin/?alt=pbbin&username=%s&password=%s&service=msg'%(APPSERVER, 
                                                                                                    msg.userName, 
                                                                                                    msg.password)
                            LOG.debug(url)
                            mdata = urllib.urlopen(url).read()
                            LOG.debug(mdata)
                            pbr.ParseFromString(mdata)
                            LOG.debug(pbr)
                            if pbr.code == 200000:
                                self.user = msg.userName
                                self.uid = pbr.userTCPLogin.uid
                                self.sid = pbr.userTCPLogin.sid
                                CHList[self.uid] = [self.broadcast]
                                LoginInfo[msg.userName] = mdata
                                LOG.debug('%s_%s Login'%(self.user,self.uid))
                            else:
                                LOG.debug('%s_%s Login error:%s'%(self.user,self.uid,pbr))
                        self.broadcast.send(self.make_response_clt(mdata))
                    elif msg.code == 3:
                        self.do_logout()
                elif cmd == 0x9006:  #return 0x9008 heart for flash
                    pass
            except Exception, e:
                LOG.error(str(e)+str(dir(e)))

    def do_logout(self):
        pbr = Response()
        url = '%s/user.tcplogout/?alt=pbbin&sid=%s'%(APPSERVER,
                                                     self.sid)
        mdata = urllib.urlopen(url).read()
        pbr.ParseFromString(mdata)
        for ch in CHList[self.uid]:
            ch.send(self.make_response_clt(mdata))
        if pbr.code == 200000:
            del(CHList[self.uid])
            del(LoginInfo[self.user])
            self.switch = False
            LOG.debug('%s_%s Logout'%(self.user,self.uid))
            self.broadcast.close()
            self.net_to_parse.close()
        else:
            LOG.debug('%s_%s Logout error:%s'%(self.user,self.uid,pbr))

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
    
    def make_transfer(self, encoded):
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
    LOG.debug('runing...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',CLT_PORT))
    sock.listen(1)
    while 1:
        sockclient,addr = sock.accept()
        LOG.debug('connecting...%s:%s'%addr)
        clt = net(sockclient, addr)
        stackless.tasklet(clt.receive)()
        
def appthread():
    global LOG
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',APP_PORT))
    sock.listen(1)
    while 1:
        sockclient,addr = sock.accept()
        LOG.debug('app service connected...%s:%s'%addr)
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