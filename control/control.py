#coding=gbk
import sys
sys.path.append('..\\lib')

import os
import config
from datetime import datetime
import socket
import struct
import log
import rar
import re

from settings import *


PATH = {}
LOG = None
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
        global SERVER, PORT
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
        self.switch = False
        self.socket.close()
        
    def send(self):
        for pack in self.spack:
            self.socket.sendall(pack)
            LOG.debug('send to Serivce : %s'%pack.__repr__())
        
    def receive(self):
        while self.switch:
            rdata = self.socket.recv(4096)
            if not rdata:
                LOG.error('%s_%s socket is closed!\n'%(SERVER, PORT))
                self.close()
            else:
                LOG.debug('receive raw_string : %s'%rdata.__repr__())
                self.pdata = self.parseHead(self.pdata + rdata)
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack('<LH', data[:6])
            if head[1] == 0xff00:
                self.close()
                LOG.info('%s receive data done!\n'%SERVER)
            if head[0] <= len(data):
                mdata = data[6:head[0]]
                data = data[head[0]:]
                if head[1] != 0xff00:
                    self.rpack.append([head[0], head[1], mdata])
                    LOG.info('received handler : [%d, %2x]'%(head[0], 
                                                             head[1]))
                    LOG.debug('received package : %s'%mdata.__repr__())
                data = self.parseHead(data)
        return data
    
    def runCommand(self):
        for len, type, data in self.rpack:
            if type == 0x0002:  #对指令的结果反馈
                LOG.info(data)
            elif type == 0x0004:
                global PATH
                if not os.path.exists(PATH['logpath']):  #log目录是否存在
                    os.popen('mkdir "%s"'%PATH['logpath'])
                namelen = struct.unpack('<H',data[:2])[0]   #log文件名长度
                mdata = [data[2:namelen + 2],data[namelen + 2:]]
                file = open(r'.\temp\%s.rar'%mdata[0],'wb')
                file.write(mdata[1])
                file.close()
                import rar
                rar.decompression(mdata[0], PATH['logpath']) #解压log
                LOG.info('解压%s到%s\n'%(mdata[0], PATH['logpath']))
            
class MainOperation(object):
    def __init__(self):
        global SERVER,PATH
        self.packages = []
        self.cltlist_string = ''

    def operation(self, cmdline):
        global OTHER
        cmds = cmdline.split(' ')   #分割参数
        dtldata = CONF.getList(PATH, cmds[0])
        step = dtldata['step'].split('|')
        if 'who' in step:
            self.packWho()
        else:
            cmdpack = self.makePocket(dtldata)
            self.packCmd(cmdpack)
        if 'up' in step:
            dtldata['logpath'] += TIME + '_' + cmds[1] + '\\'
            OTHER = 'up'
        if 'down' in step:   #step中没有down就不会产生文件包
            files = dtldata['down'].split('|')
            self.packFile(PATH['filepath'], files)
        if 'update' in step:
            self.packFile(PATH['filepath'] + 'update\\', ['*.*'])
            OTHER = 'update'
        self.packEnd()
        try:
            t = NetOperation(self.packages)
            t.connect()
            t.send()
            t.socket.settimeout(300)
            if OTHER == 'update':
                t.close()
            else:
                t.receive()
            t.runCommand()
        except Exception, e:
            if e.message != 'timed out':
                LOG.error('%s:%s\n'%(SERVER, str(e)))
            else:
                LOG.error('%s: time out!'%SERVER)
            t.close()
        if OTHER == 'up':
            os.system('explorer "' + PATH['logpath'] + '"')

    def makePocket(self, dtldata):
        global TIME
        pocket = ''
        for key in dtldata.keys():
            pocket += key + ':' + dtldata[key] + '<'
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
        from re import split
        cltlist = split('[|:.]', PATH['list'])
        self.cltlist_string = ''
        for i in range(0, cltlist.__len__(), 5):
            self.cltlist_string = '%s%s%s%s%s'%(self.cltlist_string,
                                                chr(int(cltlist[i])),
                                                chr(int(cltlist[i+1])),
                                                chr(int(cltlist[i+2])),
                                                chr(int(cltlist[i+3])))
            if cltlist[i+4]:
                self.cltlist_string = '%s%s%s'%(self.cltlist_string,
                                                chr(int(cltlist[i])/256),
                                                chr(int(cltlist[i])%256))
            else:
                self.cltlist_string = '%s\x00\x00'%self.cltlist_string
        
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
        rar.compression('down', path, names)
        LOG.debug('压缩文件%s'%names)
        data = open(r'.\temp\down.rar','rb').read()
        package = struct.pack('<LH', 
                              6 + data.__len__(), 
                              0x0003)
        package += data
        self.packages.append(package)

if __name__ == '__main__':
    log.run_log()
    LOG = log.error_log()
    CONF = config.myConfig()
    cmds = CONF.getCMD()
    SERVER = CONF.getServer()
    PORT = CONF.getPort()
    PATH = CONF.getCtrlPath()
    setTime()
    for cmd in cmds:
        MainOperation().operation(cmd)
    os.system('pause')
