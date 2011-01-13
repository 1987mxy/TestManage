#coding=gbk
import os
from ConfigParser import ConfigParser
from datetime import datetime
import socket
import struct

PATH = {}
SRVS = {}
CONF = None
TIME = ''
OTHER = ''

def setTime():
    from re import sub
    global TIME
    TIME = str(datetime.now())
    TIME = sub(':', '_', TIME)

def myIP(ip):
    ips = ip.split('.')
    tempip = ''
    for i in ips:
        i = '*'*(3-i.__len__()) + i
        tempip += i + '.'
    return tempip[:tempip.__len__()-1]

class Config(object):
    def __init__(self):
        self.cfg = ConfigParser()
        self.switch = True
        self.cfg.read('config.ini')

    def command(self):
        cmds = self.cfg.get('run','command')
        cmds = cmds.split('|')
        return cmds
        
    def server(self):
        global SRVS
        SRVS=dict(self.cfg.items('service'))
        
    def path(self):
        global PATH
        PATH = dict(self.cfg.items('path'))

    def detail(self, cmd):
        global PATH
        data = PATH
        data.update(dict(self.cfg.items(cmd)))
        return data
        
class NetOperation(object):
    def __init__(self, ip, port, packages):
        self.ip = ip
        self.timeout = 0
        self.port = port
        self.pdata = ''
        self.rpack = []
        self.spack = list(packages)
        self.spack[self.spack.__len__()-1] += myIP(ip)
        self.other = None
        self.switch = True
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))
        self.socket.settimeout(120)
        
    def close(self):
        self.socket.close()
        
    def send(self):
        for pack in self.spack:
            self.socket.sendall(pack)
        self.socket.sendall(struct.pack('<IH',6,0xffff))
        print self.ip + ':send\n'
        
    def receive(self):
        if self.switch:
            rdata = self.socket.recv(4096)
            self.timeout = 0
            if rdata == '':
                print '%s_%s socket is closed!\n'%(self.ip, self.port)
                self.socket.close()
                self.switch = False
            else:
                self.pdata = self.parseHead(self.pdata + rdata)
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack('<IH', data[:6])
            if head[1] == 0xffff:
                self.socket.close()
                self.switch = False
                print '%s receive data done!\n'%self.ip
            elif head[0] <= len(data):
                mdata = data[6:head[0]]
                data = data[head[0]:]
                self.rpack.append([head[0], head[1], mdata])
                data = self.parseHead(data)
        return data
    
    def runCommand(self):
        for len, type, data in self.rpack:
            if type == 0x0002:  #对指令的结果反馈
#                datalen = len - 6
#                mdata = struct.unpack('<%ss'%datalen, data)[0]     
#                print mdata
                print data
            elif type == 0x0003:
                global PATH
                if not os.path.exists(PATH['logpath']):  #log目录是否存在
                    os.popen('mkdir "%s"'%PATH['logpath'])
                namelen = struct.unpack('<H',data[:2])[0]   #log文件名长度
#                filelen = len - 8 - namelen #log文件大小
#                mdata = struct.unpack('<%ss%ss'%(namelen, filelen), data[2:]) #log内容
                mdata = [data[2:namelen + 2],data[namelen + 2:]]
                file = open(r'.\temp\%s'%mdata[0],'wb')
                file.write(mdata[1])
                file.close()
                import rar
                rar.decompression(mdata[0], PATH['logpath']) #解压log
                print '解压%s到%s\n'%(mdata[0], PATH['logpath'])
            
class MainOperation(object):
    def __init__(self):
        self.packages = []
        
    def operation(self, cmdline):
        global SRVS, OTHER
        cmds = cmdline.split(' ')
        dtldata = CONF.detail(cmds[0])
        step = dtldata['step'].split('|')
        if 'up' in step:
            dtldata['logpath'] += TIME + '_' + cmds[1] + '\\'
            OTHER = 'up'
        if 'down' in step:   #step中没有down就不会产生文件包
            files = dtldata['down'].split('|')
            self.packFile(PATH['filepath'], files)
        if 'update' in step:
            self.packFile(PATH['filepath'] + 'update\\', ['*.*'])
            OTHER = 'update'
        cmdpack = self.makePocket(dtldata)
        self.packCmd(cmdpack)
        terms = []
        for ip in SRVS['list'].split('|'):
            if ':' in ip:
                ip, port = ip.split(':')
                port = int(port)
            else:
                port = int(SRVS['port'])
            try:
                t = NetOperation(ip, port, self.packages)
                terms.append(t)
                t.connect()
                t.send()
                t.socket.settimeout(1)
            except Exception, e:
                t.switch = False
                print '%s:%s\n'%(ip, str(e))
        cont = True;
        while cont:
            cont = False
            for t in terms:
                try:
                    if OTHER == 'update':
                        t.close()
                        break
                    else:
                        t.receive()
                except Exception, e:
                    if not e.message == 'timed out':
                        t.switch = False
                        print '%s:%s\n'%(t.ip, str(e))
                    else:
                        t.timeout += 1
                        if t.timeout > 30:
                            t.switch = False
                            print '%s: time out!'%t.ip
                if t.switch:
                    cont = t.switch
        for t in terms:
            try:
                t.runCommand()
            except Exception, e:
                print '%s:%s\n'%(t.ip, str(e))
        if OTHER == 'up':
            os.system('explorer "' + PATH['logpath'] + '"')

    def makePocket(self, dtldata):
        global TIME
        pocket = ''
        for key in dtldata.keys():
            pocket += key + ':' + dtldata[key] + '<'
        pocket += 'ip:'
        return pocket

    def packCmd(self, pocket):  #发送指令包
        package = struct.pack('<IH',
                              pocket.__len__() + 21,
                              0x0001)
        package += pocket
        self.packages.append(package)
        
    def packFile(self, path, names):  #down操作包
        import rar
        rar.compression(path, names)
        print '压缩文件%s'%names
        data = open(r'.\temp\down.rar','rb').read()
#        package = struct.pack('<IHH8s%ss'%data.__len__(), 
#                              16 + data.__len__(), 
#                              0x0003, 
#                              8, 
#                              'down.rar', 
#                              data)
        package = struct.pack('<IHH', 
                              16 + data.__len__(), 
                              0x0003, 
                              8)
        package += 'down.rar%s'%data
        self.packages.append(package)

if __name__ == '__main__':
    CONF = Config()
    cmds = CONF.command()
    CONF.server()
    CONF.path()
    setTime()
    for cmd in cmds:
        MainOperation().operation(cmd)
    os.system('pause')