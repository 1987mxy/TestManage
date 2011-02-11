#coding=gbk
#import sys
#sys.path.append('..\\lib')

import os
import config
from datetime import datetime
import socket
import struct
import log
import rar
import re

import logging
import ConfigParser

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
        self.file = []

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((SERVER, PORT))
        self.socket.settimeout(30)
        
    def close(self):
        self.switch = False
        self.socket.close()
        
    def send(self):
        for pack in self.spack:
            self.socket.sendall(pack)
            LOG.debug('send to Serivce : %s'%pack.__repr__().__len__())
        
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
                mdata = data[ : head[0]]
                data = data[head[0] : ]
                if head[1] == 0x0006:
                    self.socket.sendall(mdata)
                    LOG.debug('send to Serivce : %s'%mdata.__repr__())
                elif head[1] != 0xff00:
                    self.rpack.append([head[0], head[1], mdata])
                    LOG.debug('received handler : [%d, %2x]'%(head[0], 
                                                             head[1]))
                    LOG.debug('received package : %s'%mdata.__repr__())
                data = self.parseHead(data)
        return data
    
    def runCommand(self):
        for len, type, data in self.rpack:
            if type == 0x0002:  #对指令的结果反馈
                LOG.info(data[6:])
            elif type == 0x0004:
                global PATH
                if self.file:   #是否第一个0x0004的包
                    self.file[1] += data[filename_len + 8 : ]   #补充文件
                else:
                    if not os.path.exists(PATH['logpath']):  #log目录是否存在
                        os.popen('mkdir "%s"'%PATH['logpath'])
                    filename_len = struct.unpack('<H',data[6 : 8])[0]   #log文件名长度
                    self.file.append(data[8 : filename_len + 8])
                    self.file.append(data[filename_len + 8 : ])
        if self.file:
            file = open(r'.\temp\%s.rar'%self.file[0],'wb')
            file.write(self.file[1])
            file.close()
            import rar
            LOG.debug(rar.decompression(self.file[0], PATH['logpath'])) #解压log
            LOG.info('解压%s到%s\n'%(self.file[0], PATH['logpath']))
            
class MainOperation(object):
    def __init__(self):
        global SERVER,PATH
        self.packages = []
        self.cltlist_string = ''
        self.e_pack = self.packEnd()
        self.w_pack = self.packWho()

    def operation(self, cmdline):
        global OTHER
        cmds = cmdline.split(' ')   #分割参数
        dtldata = CONF.getList(PATH, cmds[0])
        step = dtldata['step'].split('|')
        if 'who' in step:
            self.packages.append(self.w_pack)
        else:
            cmdpack = self.makePocket(dtldata)
            self.packCmd(cmdpack)    #先发0x0001包是让server知道该转发给那些玩家
        if 'up' in step:
            dtldata['logpath'] += TIME + '_' + cmds[1] + '\\'
            OTHER = 'up'
        if 'down' in step:   #step中没有down就不会产生文件包
            files = dtldata['down'].split('|')
            for f in files:
                if os.path.exists('%s%s'%(PATH['filepath'], f)):
                    os.popen('copy /y "%s%s" ".\\temp\\%s"'%(PATH['filepath'], f, f))
                else:
                    raise Exception('%s%s not exists!'%(PATH['filepath'], f))
            self.packFile('.\\temp\\', files)
        if 'update' in step:
            self.packFile(PATH['filepath'] + 'update\\', ['*.*'])
            OTHER = 'update'
        self.packages.append(self.e_pack)
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

    def packCmd(self, mdata):  #发送指令包
        self.getCltString()
        package = struct.pack('<LH', 
                              6 + self.cltlist_string.__len__() + mdata.__len__(), 
                              0x0001)
        package = '%s%s%s'%(package, 
                            self.cltlist_string, 
                            mdata)
        self.packages.append(package)
        
    def getCltString(self):
        from re import split
        self.cltlist_string = ''
        if PATH['list'] == 'all':
            self.cltlist_string = '\xff\xff'
        else:
            cltlist = split('[|:.]', PATH['list'])
            for i in range(0, cltlist.__len__(), 5):
                self.cltlist_string = '%s%s%s%s%s'%(self.cltlist_string,
                                                    chr(int(cltlist[i])),
                                                    chr(int(cltlist[i+1])),
                                                    chr(int(cltlist[i+2])),
                                                    chr(int(cltlist[i+3])))
                if cltlist[i+4]:            #添加端口号，2字节
                    self.cltlist_string = '%s%s%s'%(self.cltlist_string,
                                                    chr(int(cltlist[i])/256),
                                                    chr(int(cltlist[i])%256))
                else:
                    self.cltlist_string = '%s\x00\x00'%self.cltlist_string
            self.cltlist_string = '%s%s'%(struct.pack('<H', 
                                                      self.cltlist_string.__len__()),
                                          self.cltlist_string)
                    
        
    def packFile(self, path, names):  #down操作包
        len = 0
        PACKAGE_SIZE = 600
        LOG.debug(rar.compression('down', path, names))
        LOG.info('压缩文件%s'%names)
        data = open(r'.\temp\down.rar','rb').read()
        filepack_len = data.__len__()/PACKAGE_SIZE
        LOG.info(filepack_len)
        filepack_handler = struct.pack('<LH', 
                                       6 + PACKAGE_SIZE, 
                                       0x0003)
        for i in range(filepack_len):
            package = '%s%s'%(filepack_handler, data[i*PACKAGE_SIZE:(i+1)*PACKAGE_SIZE])
            self.packages.append(package)
            len += package.__len__()
        package = struct.pack('<LH', 
                              6 + data.__len__() - filepack_len * PACKAGE_SIZE, 
                              0x0003)
        package += data[filepack_len * PACKAGE_SIZE:]
        self.packages.append(package)
        len += package.__len__()
        LOG.info('send filesize is %s'%len)
        
        
    def packWho(self):  #发送指令包
        return '\x06\x00\x00\x00\x05\x00'

    def packEnd(self):
        return '\x06\x00\x00\x00\xff\xff'

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
