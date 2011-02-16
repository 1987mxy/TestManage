#coding=gbk

import sys
sys.path.append('..\\lib')

import socket,os,re,win32file,time
from struct import unpack
from _winreg import *

from config import CONF
from log import LOG
from other import runCMD
import rar
import package

#===============================================================================自定义库中所调用的类
# import logging    
# import ConfigParser
#===============================================================================

IP = None
PATH = {}

def _getIP():
    inf = os.popen('ipconfig')
    ipcfg = inf.readlines()
    for i in xrange(len(ipcfg)):
        lineinf = re.findall('^\s+IP[^:]+: ([^\r]+)\s$', ipcfg[i])   
        if lineinf and re.findall('^\s+[^:]+: ([^\r]+)\s$', ipcfg[i+2]):
            return lineinf[0]

def _findPath(flag):
    global PATH,CONF
    LOG.info('sreach file ...')
    r = win32file.GetLogicalDrives()
    for d in range(2,27):
        if(r>>d&1):
            import string
            drive = '%s:\\'%string.ascii_letters[d]
            for localpath,fields,files in os.walk(drive):
                if flag in files:
                    if open(r'%s\%s'%(localpath, flag), 'r').read() == '95279527':
                        CONF.save(flag, localpath)
                        PATH[flag] = localpath
                        LOG.info('localpath: %s\\'%localpath)
                        return '%s\\'%localpath
    LOG.info('localpath: path is none!')
    return ''

def _manageChar(path, char):   #根据通配符得到相应文件列表,uplog时+ip用
    filename = []
    if '\\' in char:
        spath = re.split(r'\\', char)[0]
    else:
        spath = ''
    result = os.popen(r'dir "%s%s"'%(path, char)).read()
    result = re.split(r'\n', result)
    for line in result[5:len(result)-3]:
        filename.append('%s\\%s'%(spath,re.split(' +', line, 3)[3]))
    return filename

class ManageClient(object):
    def __init__(self, sock):
        global PATH
        self.socket = sock
        self.e_pack = package.packCtrlEnd()
        self.reset()
        self.receive()
        
        
    def send(self):
        self.socket.sendall(self.s_pack)
        LOG.debug('send to Service : %s'%self.s_pack.__repr__().__len__())
    
    def close(self):
        self.switch = False
        self.socket.close()
    
    def reset(self):
        self.file = None
        self.search = ''
        self.s_pack = ''
        self.r_pack = []
        self.localpath = ''
        self.result = ''
        self.switch = True
    
    def receive(self):
        pdata = ''
        while self.switch:
            rdata = self.socket.recv(4096)
            LOG.debug('receive raw_string from Service : %s'%rdata.__repr__().__len__())
            if not rdata:
                LOG.error('disconnect...')
                self.close()
            else:
                pdata = self.parseHead(pdata + rdata)
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = unpack('<LH', data[:6])
            if head[1] == 0xffff:
                LOG.info('received handler from Service : [%d, %2x]'%(head[0], 
                                                                      head[1]))
                LOG.debug('received package from Service : %s'%data[:head[0]].__repr__().__len__())
                self.do()
                self.send()
                if self.search:
                    PATH[self.search]=findPath(self.search)
                LOG.info('='*30)
                self.reset()
                data = ''
            if head[0] <= len(data):
                mdata = data[:head[0]]
                data = data[head[0]:]
                if head[1] == 0x0006:
                    self.socket.send(mdata)
                    LOG.debug('send to Service : %s'%mdata.__repr__())
                elif head[1] != 0xffff:
                    self.r_pack.append([head[0], head[1], mdata])
                    LOG.info('received handler from Service : [%d, %2x]'%(head[0], 
                                                             head[1]))
                    LOG.debug('received package from Service : %s'%mdata.__repr__().__len__())
                data = self.parseHead(data)
        return data
    
    def do(self):
        filesize = 0
        global IP, PATH
        for len, type, data in self.r_pack:
            if type == 0x0003:
                if self.file:
                    self.file.write(data[6:])
                else:
                    self.file = open(r'.\temp\down.rar','wb')
                    self.file.write(data[6:])
                filesize += data.__len__()
        if self.file:
            LOG.info('receive filesize is %s'%filesize)
            self.file.close()
        for len, type, data in self.r_pack:
            if type == 0x0001:
                data = self.readString(data[6:])
                self.localpath = PATH[data['localpath']]
                if data['ip'] == IP:
                    self.fip = IP
                else:
                    t = re.split('\.',IP)
                    t = t[t.__len__()-1]
                    self.fip = '%s_%s'%(data['ip'], t)
                if 'open' in data.keys() or 'down' in data.keys() or 'up' in data.keys() or 'delete' in data.keys(): 
                    if data['localpath'] in PATH.keys() and os.path.exists(PATH[data['localpath']] + data['localpath']):
                        self.operation(data)
                    else:
                        self.result = '%s: path is none!\n'%self.fip
                        self.search = data['localpath']
                        break
                else:
                    if not data['localpath'] in PATH.keys():
                        PATH[data['localpath']]=''
                    self.operation(data)
        self.s_pack = '%s%s'%(self.s_pack, package.pack2(self.result))
        self.s_pack = '%s%s'%(self.s_pack, self.e_pack)

    #================解析数据报=================
    def readString(self,data):
        data = re.findall("(?:^|\<)([^:]*):([^<]*)",data)
        data = dict(data)
        data['ip'] = re.sub('\*', '', data['ip'])
        return data
    #================解析数据报=================

    def operation(self,data):
        global IP
        rule = data['step']                 #动作步骤和顺序
        try:
            for step in re.split('\|', rule):
                #================上传Log=================
                if step == 'up':
                    fs = []
                    for f in re.split('\|', data['up']):
                        if f:
                            fs += _manageChar(self.localpath, f)
                    if fs:
                        self.socket.settimeout(0)
                        r = package.pack4(self.fip, self.localpath, fs)
                        self.socket.settimeout(60)
                        self.result = '%s%s'%(self.result, r[0])
                        self.s_pack = '%s%s'%(self.s_pack, r[1])
                    continue
                #================上传Log=================
                for flag in re.split('\|', data[step]):
                    #================杀进程=================
                    if step == 'kill':
                        self.result = '%s%s'%(self.result, runCMD(r'taskkill /f /im %s'%flag))
                    #================杀进程=================
                    #================开进程=================
                    elif step == 'open':
                        runCMD('start "" /d "%s" "%s"'%(self.localpath, flag))
                    #================开进程=================
                    #================下载文件=================
                    elif step == 'down':
                        if not os.path.exists('%shistory'%self.localpath):
                            runCMD('mkdir "%shistory"'%self.localpath)
                            time.sleep(3)
                        tcmd = '%shistory\\%s'%(self.localpath, flag)
                        runCMD('del /q /f "%s(5)"'%tcmd)
                        runCMD('ren "%s(4)" "%s(5)"'%(tcmd,tcmd))
                        runCMD('ren "%s(3)" "%s(4)"'%(tcmd,tcmd))
                        runCMD('ren "%s(2)" "%s(3)"'%(tcmd,tcmd))
                        runCMD('ren "%s(1)" "%s(2)"'%(tcmd,tcmd))
                        runCMD('copy /y "%s" "%s(1)"'%(self.localpath + flag,tcmd))
                        LOG.info('成功下载文件%s'%flag)
                        self.result = '%s成功下载文件%s\n'%(self.result, flag)
                        self.socket.settimeout(0)
                        LOG.debug(rar.decompression('down', self.localpath)) #解压文件
                        self.socket.settimeout(60)
                        LOG.info('成功解压到%s'%self.localpath)
                        self.result = '%s成功解压到%s\n'%(self.result, self.localpath)
                    #================下载文件=================
                    #================CMD命令=================
                    elif step == 'cmd':
                        runCMD('start %s'%flag)
                    #================CMD命令=================
                    #================自我更新=================
                    elif step == 'update':
                        os.popen(r'del /q /f .\update\*.*')
                        LOG.debug(rar.decompression('down', '.\\update\\')) #解压update文件
                        os.system('update.bat')
                    #================自我更新=================
                    #================删除文件=================
                    elif step == 'delete':
                        r = runCMD('del /q /f "%s%s"'%(self.localpath, flag))
                        if r:
                            self.result = '%s%s'%(self.result, r)
                        else:
                            self.result = '%s成功删除%s\n'%(self.result, flag)
                    #================删除文件=================
            self.result = '%s : done\n%s\n%s'%(self.fip, self.localpath, self.result)
        except Exception, e:
            LOG.error(str(e))
            self.result = '%s error : %s\n%s\n%s'%(self.fip, str(e), self.localpath, self.result)

if __name__ == '__main__':
    os.system('title test_manage')
    PORT = CONF.getPort()
    SERVER = CONF.getServer()
    PATH = CONF.getCltPath()
    IP = _getIP()
    LOG.info('connecting ...')
    while 1:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER, PORT))
            sock.settimeout(60)
            ManageClient(sock)
        except Exception, e:
            LOG.error(str(e))
            time.sleep(10)
            LOG.info('reconnecting ...')