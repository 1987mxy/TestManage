#coding=gbk
import sys
sys.path.append('..\\lib')
import urllib
import stackless
import re
import time
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

class net(object):
    def __init__(self, sock, addr):
        self.switch = True
        self.do = None
        self.address = addr
        self.sock = sock
        self.windage = 0
        self.broadcast = stackless.channel()
        self.net_to_parse = stackless.channel()
        CHList['%s:%s'%self.address]=self.broadcast
        stackless.tasklet(self.threadBroadcast)()
    
    def receive(self):
        pdata = ''
        while self.switch:
            rdata = self.sock.recv(4096)
            if not rdata:
                addr = '%s:%s'%self.address
                self.broadcast.close()
                self.net_to_parse.close()
                if addr in CHList.keys():
                    del(CHList[addr])
                if self.do.uid in CHList.keys():
                    del(CHList[self.do.uid])
                    del(LoginInfo[self.do.uid])
                    urllib.urlopen('http://gamemate.cn/campus/api/user.tcplogin/?alt=pbbin&sid=%s'%self.do.sid)
                print 'disconnect...', self.address
                self.switch = False
                self.do.switch = False
                self.sock.close()
            pdata = self.parseHead(pdata + rdata)
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack('<HL', data[:6])
            if not self.do:
                if head[1] == 0xABDE:
                    self.do = virtualMessage(self.net_to_parse, self.broadcast)
                    self.sock.settimeout = 30
                    self.windage = 2
                else:
                    head = struct.unpack('<LH', data[:6])
                    self.do = testManage(self.net_to_parse, self.broadcast)
                stackless.tasklet(self.do.listen_message)()
            if head[0] + self.windage <= len(data):
                mdata = data[ : head[0] + self.windage]
                data = data[head[0] + self.windage : ]
                #TODO: 检查返回数据的格式
                self.net_to_parse.send([head[0], head[1], mdata])
                data = self.parseHead(data)
        return data

    def threadBroadcast(self):
        while self.switch:
            rdata = self.broadcast.receive()
            self.sock.sendall(rdata)
            

class testManage(object):
    def __init__(self, broadcast, net_to_parse):
        self.net_to_parse = net_to_parse
        self.broadcast = broadcast
        self.switch = True
        self.cltlist = []
    
    def listen_message(self):
        global CONTROL
        while self.switch:
            package = self.net_to_parse.receive()
            #for len, type, data in self.rpack:
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
        self.net_to_parse = net_to_parse
        self.broadcast = broadcast
        self.switch = True
        self.uid = None
        self.sid = None
    
    def listen_message(self):
        while self.switch:
            package = self.net_to_parse()
            cmd = struct.unpack("<H", mdata[8 : 10])[0]
            if cmd == 0x7001:
                CHList[receiver].send(make_response_app(0))
                receivers_len = struct.unpack("<H", mdata[14 : 16])[0]
                receivers_list = mdata[16 : receivers_len + 16]
                mdata = mdata[receivers_len + 16 : ]
                i = 0
                for i in range(0, int(receivers_len)-4, 4):
                    receiver = receivers_list[i:i+4]
                    if receiver in CHList.keys():
                        for ch in CHList[receiver]:
                            ch.send(self.make_transfer(mdata))
            elif cmd == 0x9001:
                pbr = Response()
                msg = Msg()
                msg.ParseFromString(mdata[12:])
                if msg.code == 1:
                    if msg.userName in LoginInfo.keys():    #virtual login
                        self.user = msg.userName
                        CHList[self.uid].append(self.broadcast)
                        mdata = LoginInfo[msg.userName]
                    else:
                        mdata = urllib.urlopen('http://gamemate.cn/campus/api/user.tcplogin/?alt=pbbin&name=%s&password=%s&service=msg'%(msg.userName,msg.password)).read()
                        pbr.ParseFromString(mdata)
                        if pbr.code == 200000:
                            self.user = msg.userName
                            self.uid = pbr.userTCPLogin.uid
                            self.sid = pbr.userTCPLogin.uid
                            CHList[self.uid] = [self.broadcast]
                            LoginInfo[msg.userName] = mdata
                    self.broadcast.send(make_response_clt(mdata))

    def make_response_app(response_code):   
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
    
    def make_response_clt(encoded):  #logined
       content = encoded
    
       #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4)
       message_pack_header_def='<HLHHL'
    
       pack = '%s%s'%(struct.pack(message_pack_header_def,
                                  struct.calcsize(message_pack_header_def) -2 +len(content),
                                  0xABCD,
                                  struct.calcsize(message_pack_header_def) -2 +len(content),
                                  0x9002,
                                  0),
                      content)
       return pack
    
    def make_transfer(encoded):
       content = encoded
       #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4)
       message_pack_header_def='<HLHHL%ss' % len(receivers)
    
       pack = "%s%s" %(struct.pack(message_pack_header_def,
                                   struct.calcsize(message_pack_header_def) -2 +len(content),
                                   0xABCD,
                                   struct.calcsize(message_pack_header_def) -2 +len(content),
                                   0x9003,
                                   0),
                       content,
                       )
       return pack

def cltthread():
    print 'runing...'
    sock = socket.socket()
    sock.bind(('',CLT_PORT))
    sock.listen(1)
    while 1:
        sockclient,addr = sock.accept()
        print 'connecting...', addr
        stackless.tasklet(net)(sockclient, addr)
        
def appthread():
    sock = socket.socket()
    sock.bind(('',APP_PORT))
    sock.listen(1)
    while 1:
        sockclient,addr = sock.accept()
        print 'app service connected...', addr
        stackless.tasklet(net)(sockclient, addr)

if __name__ == '__main__':
    log.run_log()
    log.error_log()
    
    stacklesssocket.install()
    import socket
    stackless.tasklet(cltthread)()
    stackless.tasklet(appthread)()
    while 1:
        time.sleep(0.1)
        stackless.run()