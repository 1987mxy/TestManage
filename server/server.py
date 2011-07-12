#coding=gbk

from sys import path
path.append('..\\lib')

import stackless
from urllib import urlopen
from traceback import format_exc
from struct import unpack, pack
import time


from mylib import log
import mylib.package
from mylib import settings
#from mylib.other import chkPath

from protobuf.msg_base_pb2 import Msg
from protobuf.res_base_pb2 import Response
from protobuf.soc_login_pb2 import SocketLoginMessage

import roachlib.stacklesssocket
import roachlib.scheduler

RUN = True

connectClient = {}   #链接上此服务器的client的列表
beControlClient = []   #一次case的client列表由0x0001包中获得
control = None  #一次case的控制端的广播channel
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
    def __init__(self, sock, addr, options):
        if self.__class__ is net:   #抽象类检测
            log.LOG.error('net class dose not instantiation')
            raise 'net class dose not instantiation'
        self.address = '%s:%s'%addr
        self.sock = sock
        self.switch = True
        self.death = False
        self.magicCode = options.magicCode
        self.heartCode = options.heartCode
        #self.responseCode = options.responseCode
        self.headformat = '<HLHHL'
        self.broadcast = MyStacklessChannel()
        self.net_to_parse = MyStacklessChannel()
    
    def receive(self):
        try:
            pdata = ''
            while self.switch:
                log.LOG.debug('%s listening...'%self.address)
                rdata = self.sock.recv(1000)
                log.LOG.debug('receive raw_string from %s : '%self.address, rdata)
                if rdata:
                    self.death = False
                    pdata = self.parseHead('%s%s'%(pdata, rdata))
                else:
                    log.LOG.info('%s disconnect...'%self.address)
                    self.exit()
        except:
            log.LOG.error('receive error : %s'%format_exc())
            log.LOG.error('%s receive error : %s'%(self.address, 
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
                        stackless.schedule()
                else:
                    log.LOG.error('receive FIFA package from %s : '%self.address, mdata)
                    self.exit()
                data = self.parseHead(data)
        return data

    def threadBroadcast(self):
        while self.switch:
            try:
                rdata = self.broadcast.receive()
                if self.switch:
                    if rdata.__class__ is list:
                        self.sock.sendall(rdata[0])
                        log.uuidLog.debug('%s\t%s : '%(rdata[1], self.address), rdata[0])
                    else:
                        self.sock.sendall(rdata)
                        log.LOG.debug('send to %s : '%self.address, rdata)
                else:
                    log.LOG.info('send to %s failed !'%self.address)
            except Exception:
                log.LOG.error('%s broadcast error : '%self.address)
                log.LOG.error('%s\n%s'%(format_exc(),
                                    rdata.__repr__()))
                self.exit()

    def chkHeart(self, gapTime):
        while (not self.death) and self.switch:
            self.death = True
            SLEEP.delay_caller(gapTime)
        if self.switch:
            log.LOG.error('%s heart time out !'%self.address)
            self.exit()
    
    def reHeart(self):
        pass
                
    def exit(self):
        pass

class testManage(net):
    def __init__(self, sock, addr):
        super(testManage, self).__init__(sock, 
                                         addr, 
                                         settings.TestManage)
        self.heartID = 0
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()
        
        self.task_reHeart = stackless.tasklet(self.reHeart)(10)
        self.task_chkHeart = stackless.tasklet(self.chkHeart)(30)
        connectClient[self.address] = self
        self.task_receive = stackless.tasklet(self.receive)()
        
        self.e_pack = mylib.package.packCtrlEnd()
        self.user = ''
        self.uid = ''
        self.cltlist = []
        
        self.file = {}
        
    def chkHeart(self, gapTime):
        while (not self.death) and self.switch:
            self.death = True
            SLEEP.delay_caller(gapTime)
        if self.switch:
            log.LOG.error('%s TestManage heart time out !'%self.address)
            self.exit()
        
    def reHeart(self, time):
        while self.switch:
            try:
                h_pack = mylib.package.pack6(self.heartID)
                self.sock.sendall(h_pack)
                log.LOG.debug('send heart %s to TestManage %s !'%(self.heartID, self.address))
                if self.heartID >= 0xffffffff:
                    self.heartID = 0
                else:
                    self.heartID += 1
            except:
                log.LOG.debug(format_exc())
            SLEEP.delay_caller(time)
        
    def exit(self):
        global control, connectClient
        self.broadcast.close()
        self.net_to_parse.close()
        self.switch = False
        self.sock.close()
        if self.address in connectClient.keys():
            if control and self.address in beControlClient:
                info = '%s heart time out or disconnect ...'%self.address
                control.broadcast.send(mylib.package.pack2(info))
            self.quitBeControl(self.address)
            del(connectClient[self.address])
            if self.uid and self.uid in connectClient.keys() and self in connectClient[self.uid]:       #client.exe退出时关闭该链接虚拟登录
                connectClient[self.uid].remove(self)
            log.LOG.info('%s TestManage exit...'%self.address)
        elif self == control:      #不是CONTROL
            control = None
            self.dispense('exit')
            for ip in beControlClient:
                if ip in connectClient.keys():
                    connectClient[ip].exit()
            log.LOG.info('%s Control exit...'%self.address)
        
    
    def listen_message(self):
        global control, RUN
        msg = SocketLoginMessage()
        pbr = Response()
        while self.switch:
            r_pack = self.net_to_parse.receive()
            if r_pack[1] in [0x9001,0x0003,0x0004]:   #是用SID不停登陆的,所以需要不显示LOG
                log.LOG.debug('received head from TestManage %s : [%d, %2x]'%(self.address, 
                                                                          r_pack[0], 
                                                                          r_pack[1]))
            else:
                log.LOG.info('received head from TestManage %s : [%d, %2x]'%(self.address, 
                                                                         r_pack[0], 
                                                                         r_pack[1]))
            log.LOG.debug('received package from TestManage %s : '%self.address, r_pack[2])
            result = ''
            if r_pack[1] == 0x0001:
                control = self
                if self.address in connectClient.keys():
                    del(connectClient[self.address])
                s_pack = self.getBeControl(r_pack)
                self.dispense(s_pack, addip = True)
            elif r_pack[1] in [0x0002, 0x0004]:
                if control:
                    control.broadcast.send(r_pack[2])
            elif r_pack[1] in [0x0003, 0xffff]:
                if r_pack[1] == 0xffff and control:
                    control.broadcast.send(r_pack[2])
                self.dispense(r_pack[2])
            elif r_pack[1] == 0x0005:
                control = self
                if self.address in connectClient.keys():
                    del(connectClient[self.address])
                ipList = []
                uidList = []
                userSubConnect = 0
                for flag in connectClient.keys():
                    if ':' in flag:
                        ipList += [str(connectClient[flag].user), '\t', flag, '\n']
                    else:
                        clients = []
                        for client in connectClient[flag]:
                            userSubConnect += 1
                            clients += ['\t', client.address, '\n']
                        clientString = ''.join(clients)
                        uidList += [flag, '\t', str(len(connectClient[flag])), '\n', clientString]
                summarizeIP = 'have connected client count : %s\n'%str(len(ipList)/4)
                summarizeUID = 'have logined client count : %s\n'%str(userSubConnect)
                result = ''.join(ipList + uidList + [summarizeIP, summarizeUID])
                log.LOG.info(result)
                s_pack = ''.join([mylib.package.pack2(result), self.e_pack])
                self.broadcast.send(s_pack)
            elif r_pack[1] == 0xff00:
                self.quitBeControl(self.address)
            elif r_pack[1] == 0xf0f0:   #关闭服务器
                raise(KeyboardInterrupt)
#            模拟登陆
            elif r_pack[1] == 0x9001:    #用来借助自动脚本关闭war3进程所必须的登录
                msg.ParseFromString(r_pack[2][14:])
                log.LOG.debug('receive package from TestManage %s : %s'%(self.address,
                                                                     msg))
                user = msg.userName
                if user in LoginInfo.keys():    #virtual login
                    sid = LoginInfo[user]
                    url = '%s/user.tcplogin/?alt=pbbin&sid=%s&service=msg'%(settings.APPSERVER, 
                                                                            sid)
                    i=0
                    while i<10:
                        try:
                            r_pack[2] = urlopen(url).read()
                            break
                        except:
                            i+=1
                            log.LOG.error('TestManage http request failed : %s'%url)
                            if i >= 10:
                                self.exit()
                                return
                    log.LOG.info('%s_%s TestManage send http request : %s'%(user,
                                                                        self.address, 
                                                                        url))
                    pbr.ParseFromString(r_pack[2])
                    log.LOG.debug('%s_%s TestManage receive http response : %s'%(user, 
                                                                            self.address, 
                                                                            pbr))
                    if pbr.code == 200000:
                        self.user = user
                        self.uid = str(pbr.userTCPLogin.uid)
                        if self.uid in connectClient.keys():
                            connectClient[self.uid].append(self)
                        log.LOG.info('%s_%s_%s TestManage double logined'%(user, 
                                                                       self.uid, 
                                                                       self.address))
                        self.broadcast.send(mylib.package.make_response_clt(r_pack[2]))
                    else:
                        if self.user in LoginInfo.keys():
                            del(LoginInfo[self.user])
                        log.LOG.error('%s_%s TestManage double logined failed !'%(user, 
                                                                              self.address))
                else:
                    self.uid=''
                    self.user=''
#===============================================================================
# #===============================================================================
# # 姚常鋆 C++ Client LOG收集逻辑
# #===============================================================================
#            elif r_pack[1] == 0x1001:
#                filename_len = unpack('<H',r_pack[2][14 : 16])[0]   #log文件名长度
#                filename = r_pack[2][16 : filename_len + 16]
#                if filename in self.file.keys():
#                    self.file[filename].write(r_pack[2][filename_len + 16 : ])   #补充文件
#                else:
#                    chkPath(r'.\gmlog')
#                    self.file[filename] = open(r'.\gmlog\%s'%filename,'wb')
#                    self.file[filename].write(r_pack[2][filename_len + 16 : ])
#            elif r_pack[1] == 0x10ff:
#                filename_len = unpack('<H',r_pack[2][14 : 16])[0]
#                filename = r_pack[2][16 : filename_len + 16]
#                if filename in self.file.keys():
#                    self.file[filename].close()
#                    del(self.file[filename])
#                    self.broadcast.send(mylib.package.packCltEnd())
#===============================================================================
                
    def dispense(self, package, addip = False):
        global beControlClient
        for ip in beControlClient:     #调出0x0001包中所存在的目的地址
            if ip in connectClient.keys():     #与正连接的客户端列表进行比较
                if addip:
                    tempPackage = '%sip:%s'%(package, self.encodeIP(ip.split(':')[0]))
                else:
                    tempPackage = package
                connectClient[ip].broadcast.send(tempPackage)
                log.LOG.debug('send to TestManage %s : '%ip, tempPackage)
            else:
                info = '%s connecting failed ...'%ip
                log.LOG.info(info)
                self.broadcast.send(mylib.package.pack2(info))
                self.quitBeControl(ip)

    def quitBeControl(self, addr):
        global beControlClient
        if addr in beControlClient:     #当客户端列表为空时，可以发送控制端收尾指令
            beControlClient.remove(addr)
            if not beControlClient and control:
                control.broadcast.send(self.e_pack)

    def getBeControl(self, r_pack):
        global beControlClient
        cltstring_len = int(unpack('<H', r_pack[2][14:16])[0])
        if cltstring_len == 0xffff:
            beControlClient = [ip for ip in connectClient.keys() if ':' in ip]   #没有':'则为virtual_message的链接,需要排除
            cltstring_len = 0
        elif cltstring_len > 0xf000:
            beControlClient = [ip for ip in connectClient.keys() if ':' in ip]
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
                    if ip in beControlClient:
                        beControlClient.remove(ip)
                else:
                    ip = '%s.%s.%s.%s:'%(ord(cltstring[i]),
                                        ord(cltstring[i+1]),
                                        ord(cltstring[i+2]),
                                        ord(cltstring[i+3]))
                    tempCLTLIST = beControlClient[:]
                    for addr in tempCLTLIST:
                        if ip in addr:
                            beControlClient.remove(addr)
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
                    tempCLTLIST = [addr for addr in connectClient.keys() if ip == addr]
                else:
                    ip = '%s.%s.%s.%s:'%(ord(cltstring[i]),
                                        ord(cltstring[i+1]),
                                        ord(cltstring[i+2]),
                                        ord(cltstring[i+3]))
                    tempCLTLIST = [addr for addr in connectClient.keys() if ip in addr]
                if tempCLTLIST:
                    beControlClient += tempCLTLIST
                else:
                    result = '%s connecting failed...\n'%ip
                    s_pack = mylib.package.pack2(result)
                    control.broadcast.send(s_pack)
        if not beControlClient:
            control.broadcast.send(self.e_pack)
        m_pack = r_pack[2][16 + cltstring_len : ]
        s_pack = '%s%s'%(pack('<HLHHL', 
                              r_pack[0] - cltstring_len + 16,    #16 = 18(myIP) - 2(client_len)
                              0xAAAC, 
                              r_pack[0] - cltstring_len + 16, 
                              r_pack[1], 
                              0),
                         m_pack)
        return s_pack

    def encodeIP(self, ip):
        ips = ip.split('.')
        tempip = ''
        for i in ips:
            i = '*'*(3-i.__len__()) + i
            tempip += i + '.'
        return tempip[:tempip.__len__()-1]

class VirtualMessage_to_Flash(net):
    def __init__(self, sock, addr):
        super(VirtualMessage_to_Flash, self).__init__(sock, 
                                                      addr, 
                                                      settings.VirtualMessagetoClient)
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()

        self.task_reHeart = None
        self.task_chkHeart = stackless.tasklet(self.chkHeart)(30)
        self.task_receive = stackless.tasklet(self.receive)()
        self.frontSendTime = 0
        self.uid = ''
        self.sid = ''
        self.user = ''
        self.responseHeart = ''

    def chkHeart(self, gapTime):
        while (not self.death) and self.switch:
            self.death = True
            SLEEP.delay_caller(gapTime)
        if self.switch:
            log.LOG.error('%s_%s_%s Flash heart time out !'%(self.user, self.uid, self.address))
            self.exit()

    def reHeart(self, gapTime):
        while self.switch:
            try:
                self.frontSendTime = time.time()
                self.sock.sendall(self.responseHeart)
                log.LOG.debug('send heart to Flash %s_%s_%s !'%(self.user, self.uid, self.address))
            except:
                log.LOG.debug(format_exc())
            SLEEP.delay_caller(gapTime)
            
    def exit(self):
        if self.uid in connectClient.keys():
            if self in connectClient[self.uid]:
                connectClient[self.uid].remove(self)
            if not [client for client in connectClient[self.uid] if client.__class__ == VirtualMessage_to_Flash]:
                self.do_logout()
        self.broadcast.close()
        self.net_to_parse.close()
        self.switch = False
        self.sock.close()
        log.LOG.info('%s_%s_%s Flash exit...'%(self.user, self.uid, self.address))

    def listen_message(self):
        while self.switch:
            try:
                r_pack = self.net_to_parse.receive()
                if r_pack[1] != 0x9007:
                    log.LOG.info('received package from Flash %s_%s_%s : [%d, %2x]'%(self.user, 
                                                                                 self.uid, 
                                                                                 self.address, 
                                                                                 r_pack[0], 
                                                                                 r_pack[1]))
                    log.LOG.debug('received package from Flash %s_%s_%s : '%(self.user, 
                                                                         self.uid, 
                                                                         self.address), 
                              r_pack[2])
                if r_pack[1] == 0x9001:
                    pbr = Response()
                    msg = SocketLoginMessage()
                    msg.ParseFromString(r_pack[2][14:])
                    user = msg.userName
                    log.LOG.debug('receive login_msg from Flash %s_%s : %s'%(user,
                                                                            self.address,
                                                                            msg))
                    if msg.code == 1:
                        if user in LoginInfo.keys():    #virtual login
                            sid = LoginInfo[user]
                            url = '%s/user.tcplogin/?alt=pbbin&sid=%s&service=msg'%(settings.APPSERVER, 
                                                                                    sid)
                            i=0
                            while i<10:
                                try:
                                    r_pack[2] = urlopen(url).read()
                                    break
                                except:
                                    i+=1
                                    log.LOG.error('Flash http request failed : %s'%url)
                                    if i >= 10:
                                        self.exit()
                                        return
                            log.LOG.info('%s_%s Flash send http request : %s'%(user,
                                                                                 self.address, 
                                                                                 url))
                            pbr.ParseFromString(r_pack[2])
                            log.LOG.debug('%s_%s Flash receive http response : %s'%(user, 
                                                                                   self.address, 
                                                                                   pbr))
                            if pbr.code == 200000:
                                self.user = user
                                self.uid = str(pbr.userTCPLogin.uid)
                                self.responseHeart = mylib.package.make_response_heart(int(self.uid))
                                self.task_reHeart = stackless.tasklet(self.reHeart)(10)
                                if self.uid in connectClient.keys():
                                    connectClient[self.uid].append(self)
                                log.LOG.info('%s_%s_%s Flash double logined ...'%(self.user, 
                                                                                 self.uid, 
                                                                                 self.address))
                            else:
                                #此时sid已经过期用sid登出是没有意义的
                                del(LoginInfo[user])
                                log.LOG.error('%s_%s_%s Flash double logined failed !'%(self.user, 
                                                                                       self.uid, 
                                                                                       self.address))
                        else:
                            url = '%s/user.tcplogin/?alt=pbbin&username=%s&password=%s&service=msg'%(settings.APPSERVER, 
                                                                                                     user, 
                                                                                                     msg.password)
                            i=0
                            while i<10:
                                try:
                                    r_pack[2] = urlopen(url).read()
                                    break
                                except:
                                    i+=1
                                    log.LOG.error('Flash http request failed : %s'%url)
                                    if i >= 10:
                                        self.exit()
                                        return
                            log.LOG.info('%s_%s Flash send http request: %s'%(user, 
                                                                             self.address, 
                                                                             url))
                            pbr.ParseFromString(r_pack[2])
                            log.LOG.debug('%s_%s Flash receive http response: %s'%(user, 
                                                                                  self.address, 
                                                                                  pbr))
                            if pbr.code == 200000:
                                self.user = user
                                self.uid = str(pbr.userTCPLogin.uid)
                                self.sid = pbr.userTCPLogin.sid
                                self.responseHeart = mylib.package.make_response_heart(int(self.uid))
                                self.task_reHeart = stackless.tasklet(self.reHeart)(10)
                                connectClient[self.uid] = [self]
                                LoginInfo[user] = self.sid
                                log.LOG.info('%s_%s_%s Flash logined ...'%(self.user, 
                                                                          self.uid, 
                                                                          self.address))
                            else:
                                log.LOG.error('%s_%s_%s Flash login failed : %s'%(self.user, 
                                                                                 self.uid, 
                                                                                 self.address, 
                                                                                 pbr))
                        self.broadcast.send(mylib.package.make_response_clt(r_pack[2]))
                    elif msg.code == 3:
                        self.do_logout()
                elif r_pack[1] == 0x9007:
                    ping = int((time.time()-self.frontSendTime)*500)
                    log.LOG.debug('%s_%s_%s Ping is %s'%(self.user, 
                                                        self.uid, 
                                                        self.address,
                                                        ping))
                    if self.uid:
                        package = mylib.package.make_response_ping(int(self.uid), ping)
                    else:
                        package = mylib.package.make_response_ping(0, ping)
                    self.sock.sendall(package)
                else:
                    log.LOG.warning('unknow package from Flash %s_%s_%s : %x'%(self.user, 
                                                                              self.uid, 
                                                                              self.address, 
                                                                              r_pack[1]))
            except :
                log.LOG.error('listen message error from Flash %s_%s_%s : %x, %s'%(self.user, 
                                                                                  self.uid, 
                                                                                  self.address, 
                                                                                  r_pack[1], 
                                                                                  r_pack.__repr__()))
                log.LOG.error(format_exc())

    def do_logout(self):
        if self.uid in connectClient.keys() and self.user in LoginInfo.keys():
            while True:
                pbr = Response()
                url = '%s/user.tcplogout/?alt=pbbin&sid=%s&service=msg'%(settings.APPSERVER,
                                                                         self.sid)
                i=0
                while i<10:
                    try:
                        mdata = urlopen(url).read()
                        break
                    except:
                        i+=1
                        log.LOG.error('Flash http request failed : %s'%url)
                        if i >= 10:
                            self.exit()
                            return
                log.LOG.debug('%s_%s_%s Flash send http request: %s'%(self.user, 
                                                                    self.uid, 
                                                                    self.address, 
                                                                    url))
                pbr.ParseFromString(mdata)
                log.LOG.info('%s_%s_%s Flash receive http response: %s'%(self.user, 
                                                                        self.uid, 
                                                                        self.address, 
                                                                        pbr))
                if pbr.code == 200000:
                    if self.user in LoginInfo.keys():
                        del(LoginInfo[self.user])
                    if self.uid in connectClient.keys():
                        uid = self.uid
                        for client in connectClient[self.uid]:
                            client.broadcast.send(mylib.package.make_response_clt(mdata))
                            client.uid = ''
                            client.user = ''
                        del(connectClient[uid])
                    log.LOG.info('%s_%s_%s Flash logouted ...'%(self.user, 
                                                               self.uid, 
                                                               self.address))
                    break
                else:
                    log.LOG.error('%s_%s_%s Flash logout failed : %s'%(self.user, 
                                                                      self.uid, 
                                                                      self.address, 
                                                                      pbr))
                    for client in connectClient[self.uid]:
                        client.broadcast.send(mylib.package.make_response_clt(mdata))
                    SLEEP.delay_caller(5)
                        

class VirtualMessage_to_Service(net):
    def __init__(self, sock, addr):
        super(VirtualMessage_to_Service, self).__init__(sock, 
                                                        addr, 
                                                        settings.VirtualMessagetoService)
        self.task_broadcast = stackless.tasklet(self.threadBroadcast)()
        self.task_receive = stackless.tasklet(self.receive)()
        self.package = None
        
    def exit(self):
        self.broadcast.close()
        self.net_to_parse.close()
        self.sock.close()
        self.switch = False
        log.LOG.info('%s APP Service exit...'%self.address)

    def listen_message(self):
        msg = Msg()
        while self.switch:
            try:
                r_pack = self.net_to_parse.receive()  #r_pack[0] 包长度, r_pack[1]magic_code, r_pack[2]收到的完成数据包
                log.LOG.debug('received package from APP Service %s : '%self.address, 
                          r_pack[2])
                log.LOG.info('APP Service %s code: %x'%(self.address, 
                                                    r_pack[1]))
                if r_pack[1] == 0x7001:
                    self.broadcast.send(mylib.package.make_response_app(0))
                    receivers_list = self.getReceivers(r_pack[2])
                    msg.ParseFromString(self.package)   ###################
                    log.LOG.debug('APP Service transmit package : %s'%msg)    ###############
                    for receiver in receivers_list:
                        if str(receiver) in connectClient.keys():
                            log.LOG.debug('APP Service %s transmit to receiver %s : '%(self.address,
                                                                                   receiver), 
                                     self.package)
                            s_string = mylib.package.make_transmit(self.package)
                            for virtualMessageClient in connectClient[str(receiver)]:
                                virtualMessageClient.broadcast.send([s_string,msg.uuid])
                elif r_pack[1] == 0x7003:
                    self.broadcast.send(mylib.package.make_response_app(0))
                    self.package = r_pack[2][14:]
                    msg.ParseFromString(self.package)   ###################
                    log.LOG.debug('APP Service transmit package : %s'%msg)    ###############
                    for receiver in connectClient.keys(): 
                        if not ':' in receiver:
                            log.LOG.debug('APP Service %s transmit to receiver %s : '%(self.address,
                                                                                   receiver), 
                                      self.package)
                            s_string = mylib.package.make_transmit(self.package)
                            for virtualMessageClient in connectClient[receiver]:
                                virtualMessageClient.broadcast.send([s_string,msg.uuid])
                else:
                    log.LOG.warning('unknow code from APP Service %s : %x'%(self.address, 
                                                                        r_pack[1]))
            except :
                log.LOG.error('listen message error from APP Service %s : %x, %s'%(self.address,
                                                                               r_pack[1], 
                                                                               r_pack.__repr__()))
                log.LOG.error(format_exc())

    def getReceivers(self, package):
        receivers_len = unpack("<H", package[14 : 16])[0]
        receivers_string = package[16 : receivers_len * 4 + 16]
        self.package = package[receivers_len * 4 + 16 : ]
        receivers_list = unpack('<%sL'%receivers_len, receivers_string)
        return receivers_list

def TestThread():
    global RUN, TASK_TEST
    log.LOG.info('testmanage runing...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', settings.TestManage.port))
    sock.listen(100)
    while RUN:
        sockclient,addr = sock.accept()
        log.LOG.info('%s:%s TestManage connected...'%addr)
        test = testManage(sockclient, addr)
        TASK_TEST.append(stackless.tasklet(test.listen_message)())
    sock.close()

def CltThread():
    global RUN, TASK_CLT 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', settings.VirtualMessagetoClient.port))
    sock.listen(100)
    while RUN:
        sockclient, addr = sock.accept()
        log.LOG.info('%s:%s Flash connected...'%addr)
        clt = VirtualMessage_to_Flash(sockclient, addr)
        TASK_CLT.append(stackless.tasklet(clt.listen_message)())
    sock.close()
        
def APPThread():
    global RUN, TASK_APP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', settings.VirtualMessagetoService.port))
    sock.listen(100)
    while RUN:
        sockclient, addr = sock.accept()
        log.LOG.info('%s:%s APP service connected...'%addr)
        srv = VirtualMessage_to_Service(sockclient, addr)
        TASK_APP.append(stackless.tasklet(srv.listen_message)())
    sock.close()

if __name__ == '__main__':
    from os import popen
    popen('title VirtualMessage Service')
    roachlib.stacklesssocket.install()
    import socket
    log.run_log()
    log.uuid_log()
    if settings.VirtualMessage:
        log.LOG.info('virtualmessage runing...')
        TASK_APP.append(stackless.tasklet(APPThread)())
        TASK_CLT.append(stackless.tasklet(CltThread)())
    TASK_TEST.append(stackless.tasklet(TestThread)())
    try:
        while RUN:
            stackless.run()
            time.sleep(0.05)
    except KeyboardInterrupt:
        for key in connectClient.keys():
            if key in connectClient.keys():
                if connectClient[key].__class__ is list:
                    for connecter in connectClient[key]:
                        connecter.exit()
                else:
                    connectClient[key].exit()
        log.LOG.info('The End ...')
        