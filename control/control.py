#coding=gbk
import sys
sys.path.append('..\\lib')

import os
import config
from datetime import datetime
import socket
import struct

from settings import *

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


        
class NetOperation(object):
    def __init__(self, packages):
        global SERVER
        self.outtime = 0
        self.pdata = ''
        self.rpack = []
        self.spack = packages
        self.other = None
        self.switch = True
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((SERVER, PORT))
        self.socket.settimeout(120)
        
    def close(self):
        self.socket.close()
        
    def send(self):
        for pack in self.spack:
            self.socket.sendall(pack)
        
    def receive(self):
        if self.switch:
            rdata = self.socket.recv(4096)
            print rdata.__repr__()
            self.outtime = 0
            if rdata == '':
                print '%s_%s socket is closed!\n'%(SERVER, self.port)
                self.socket.close()
                self.switch = False
            else:
                self.pdata = self.parseHead(self.pdata + rdata)
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack('<LH', data[:6])
            if head[1] == 0xffff:
                self.socket.close()
                self.switch = False
                print '%s receive data done!\n'%SERVER
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
                rar.decompression('up',mdata[0], PATH['logpath']) #解压log
                print '解压%s到%s\n'%(mdata[0], PATH['logpath'])
            
class MainOperation(object):
    def __init__(self):
        global SERVER
        self.packages = []
        self.cltlist_string = ''
        
    def operation(self, cmdline):
        global OTHER
        cmds = cmdline.split(' ')
        dtldata = CONF.getList(cmds[0])
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
        if 'who' in step:
            self.packWho()
        cmdpack = self.makePocket(dtldata)
        self.packCmd(cmdpack)
        self.packEnd()
        terms = []
        try:
            t = NetOperation(self.packages)
            terms.append(t)
            t.connect()
            t.send()
            t.socket.settimeout(1)
        except Exception, e:
            t.switch = False
            print 'Service:%s\n'%str(e)
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
                        print '%s:%s\n'%(SERVER, str(e))
                    else:
                        t.outtime += 1
                        if t.outtime > 30:
                            t.switch = False
                            print '%s: time out!'%SERVER
                if t.switch:
                    cont = t.switch
        for t in terms:
            try:
                t.runCommand()
            except Exception, e:
                print '%s:%s\n'%(SERVER, str(e))
        if OTHER == 'up':
            os.system('explorer "' + PATH['logpath'] + '"')

    def makePocket(self, dtldata):
        global TIME
        pocket = ''
        for key in dtldata.keys():
            pocket += key + ':' + dtldata[key] + '<'
#        pocket += 'ip:' + SRVS['list']
        return pocket

    def packCmd(self, pocket):  #发送指令包
        self.getCltString()
        package = struct.pack('<LHH', 
                              8 + self.cltlist_string.__len__() + pocket.__len__(), 
                              0x0001, 
                              self.cltlist_string.__len__())
        package += (self.cltlist_string + pocket)
        self.packages.append(package)
        
    def getCltString(self):
        global CTRLS
        cltlist = re.split('[|:.]', CTRLS['list'])
        self.cltlist_string = ''
        for i in range(cltlist):
            if (i+1)%5 == 0:
                if cltlist[i]:
                    self.cltlist_string += chr(int(cltlist[i])/256) + chr(int(cltlist[i])%256)
                else:
                    self.cltlist_string += '\x00\x00'
            else:
                self.cltlist_string += chr(int(cltlist[i]))
        
    def packWho(self):  #发送指令包
        package = struct.pack('<LH',
                              6,
                              0x0005)
        self.packages.append(package)
        
    def packEnd(self):
        package = struct.pack('<LH', 
                              6, 
                              0xffff)
        self.packages.append(package)
        
    def packFile(self, path, names):  #down操作包
        import rar
        rar.compression('down', path, names)
        print '压缩文件%s'%names
        data = open(r'.\temp\down.rar','rb').read()
        package = struct.pack('<LHH%ssH', 
                              16 + data.__len__(), 
                              0x0003, 
                              self.cltlist_string.__len__(), 
                              self.cltlist_string, 
                              8)
        package += 'down.rar%s'%data
        self.packages.append(package)

if __name__ == '__main__':
    CONF = config.myConfig()
    cmds = CONF.getCMD
    CONF.getServer()
    CONF.getCtrlPath()
    setTime()
    for cmd in cmds:
        MainOperation().operation(cmd)
    os.system('pause')
