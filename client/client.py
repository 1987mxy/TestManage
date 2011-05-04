#coding=gbk

import sys
sys.path.append('..\\lib')

import socket, os, re
from traceback import format_exc
from win32file import GetLogicalDrives
from time import sleep
from struct import unpack, pack
from _winreg import *

from mylib.log import LOG, get_screen
from mylib.other import runCMD, chkPath
from mylib.msg_base_pb2 import Msg
import mylib.rar
import mylib.package
from mylib.config import CONF

IP = None
PATH = {}
SERVER = None
PORT = None
GMPORT = None
USER = None
PASSWD = None

def _getIP():
    inf = os.popen('ipconfig')
    ipcfg = inf.readlines()
    for i in xrange(len(ipcfg)):
        lineinf = re.findall('^\s+IP[^:]+: ([^\r]+)\s$', ipcfg[i])   
        if lineinf and re.findall('^\s+[^:]+: ([^\r]+)\s$', ipcfg[i + 2]):
            return lineinf[0]

def _findPath(flag):
    global PATH, CONF
    LOG.info('sreach file ...')
    r = GetLogicalDrives()
    for d in range(2, 27):
        if(r >> d & 1):
            import string
            drive = '%s:\\' % string.ascii_letters[d]
            for localpath, fields, files in os.walk(drive):
                if flag in files:
                    if open(r'%s\%s' % (localpath, flag), 'r').read() == '95279527':
                        CONF.save('localpath', flag, '%s\\' % localpath)
                        PATH[flag] = localpath
                        LOG.info('localpath : %s\\' % localpath)
                        return '%s\\' % localpath
    LOG.info('localpath: path is none!')
    return ''

def _manageChar(path, char):   #根据通配符得到相应文件列表,如果直接用通配符无法在文件名中+上IP
    filename = []
    if '\\' in char:
        spath = re.split(r'\\', char)[0]
    else:
        spath = ''
    result = os.popen(r'dir "%s%s"' % (path, char)).read()
    result = re.split(r'\n', result)
    for line in result[5:len(result) - 3]:
        filename.append('%s\\%s' % (spath, re.split(' +', line, 3)[3]))
    return filename

class ManageClient(object):
    def __init__(self, sock):
        global PATH
        self.socket = sock
        
        self.login = False
        self.e_pack = mylib.package.packCtrlEnd()
        self.msg = Msg()
        self.reset()
        self.socket.sendall(mylib.package.pack6())
        self.receive()

    def send(self):
        self.socket.sendall(self.s_pack)
        LOG.debug('send to Service : ', self.s_pack)
    
    def close(self):
        self.switch = False
        self.socket.shutdown()
    
    def reset(self):
        self.file = None
        self.search = ''
        self.s_pack = []
        self.r_pack = []
        self.localpath = ''
        self.result = []
        self.switch = True
        
    def reconnect(self):
        
        pass
    
    def receive(self):
        pdata = ''
        while self.switch:
            rdata = self.socket.recv(4096)
            LOG.debug('receive raw_string from Service : ', rdata)
            if not rdata:
                LOG.error('disconnect...')
                self.close()
            else:
                pdata = self.parseHead(pdata + rdata)
                
    def parseHead(self, data):
        global GMPORT
        if len(data) >= 14:
            head = unpack('<HLHHL', data[:14])
            if head[0] + 2 <= len(data):
                mdata = data[ : head[0] + 2]
                data = data[head[0] + 2 : ]
                if head[1] == 0xABDE:
                    if head[3] == 0x9003:
                        self.msg.ParseFromString(mdata[14:])
                        if self.msg.code == 0x230d and (not self.msg.arenaEnded.error):
                            GameStatus = os.getenv('GAMESTATUS')    #获取环境变量 
                            if GameStatus != None and int(GameStatus) < 4:
                                get_screen()
                            LOG.info('Arena End info : ', mdata[14:])
                            runCMD('taskkill /f /im war3.exe')
                            runCMD('taskkill /f /im startcraft.exe')
                            LOG.info('Process Killed !')
                            #os.system('start "" /d "%s" "GMClient.exe"'%os.getenv('TEMPPATH'))
    #                       os.system('close_war3.exe')
                    elif head[3] == 0x9002:
                        self.login = not self.login
                        if self.login:
                            #os.system('gmclient_watcher.vbs %s'%GMPORT)
                            LOG.info('Virtual User logined !')
                        else:
                            os.system('taskkill /f /im gmclient_watcher.exe')
                            LOG.info('Virtual User logouted !')
                elif head[1] == 0xAAAC:
                    if head[3] == 0xffff:
                        LOG.info('received head from Service : [%d, %2x]' % (head[0],
                                                                           head[3]))
                        LOG.debug('received package from Service : ', mdata)
                        self.listen_message()
                        self.send()
                        if self.search:
                            PATH[self.search] = _findPath(self.search)
                        LOG.info('='*30)
                        self.reset()
                        data = ''
                    elif head[3] == 0x0006:
                        self.socket.send(mdata)
                        if not self.login:
                            self.chkGMClient()
                        LOG.debug('received heart!')
                    else:
                        self.r_pack.append([head[0], head[3], mdata])
                        LOG.info('received handler from Service : [%d, %2x]' % (head[0],
                                                                              head[3]))
                        LOG.debug('received package from Service : ', mdata)
                else:
                    LOG.error('receive FIFA package from %s : %s' % (self.address, mdata.__repr__()))
                    self.close()
                data = self.parseHead(data)
        return data
    
    def listen_message(self):
        filesize = 0
        global IP, PATH
        for len, cmd, data in self.r_pack:
            if cmd == 0x0003:
                if self.file:
                    self.file.write(data[14:])
                else:
                    chkPath(r'.\temp')
                    self.file = open(r'.\temp\down.rar', 'wb')
                    self.file.write(data[14:])
                filesize += data.__len__()
        if self.file:
            self.file.close()
            LOG.info('receive filesize is %s' % filesize)
        for len, cmd, data in self.r_pack:
            if cmd == 0x0001:
                data = self.readString(data[14:]) 
                if data['ip'] == IP:
                    self.fip = IP
                else:
                    t = re.split('\.', IP)
                    t = t[t.__len__() - 1]
                    self.fip = '%s_%s' % (data['ip'], t)
                if 'open' in data.keys() or 'down' in data.keys() or 'up' in data.keys() or 'delete' in data.keys(): 
                    if data['localpath'] in PATH.keys() and os.path.exists(PATH[data['localpath']] + data['localpath']):
                        self.localpath = PATH[data['localpath']]
                        os.environ['TEMPPATH'] = self.localpath
                        self.operation(data)
                    else:
                        self.result += [self.fip, ' : path is none!\n']
                        self.search = data['localpath']
                        break
                else:
                    if not data['localpath'] in PATH.keys():
                        PATH[data['localpath']] = ''
                    self.operation(data)
        self.s_pack = ''.join(self.s_pack + [mylib.package.pack2(''.join(self.result)), self.e_pack])

    #================解析数据报=================
    def readString(self, data):
        data = re.findall("(?:^|\<)([^:]*):([^<]*)", data)
        data = dict(data)
        data['ip'] = re.sub('\*', '', data['ip'])
        return data
    #================解析数据报=================

    def operation(self, data):
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
                        r = mylib.package.pack4(self.fip, self.localpath, fs)
                        self.socket.settimeout(60)
                        self.result.append(r[0])
                        self.s_pack.append(r[1])
                    continue
                #================上传Log=================
                #================下载文件=================
                elif step == 'down':
                    chkPath('%shistory' % self.localpath)
                    for flag in re.split('\|', data['down']):
                        tcmd = '%shistory\\%s' % (self.localpath, flag)
                        runCMD('del /q /f "%s(5)"' % tcmd)
                        runCMD('ren "%s(4)" "%s(5)"' % (tcmd, flag))
                        runCMD('ren "%s(3)" "%s(4)"' % (tcmd, flag))
                        runCMD('ren "%s(2)" "%s(3)"' % (tcmd, flag))
                        runCMD('ren "%s(1)" "%s(2)"' % (tcmd, flag))
                        runCMD('copy /y "%s" "%s(1)"' % (self.localpath + flag, tcmd))
                        LOG.info('成功下载文件%s' % flag)
                        self.result += ['成功下载文件', flag, '\n']
                    self.socket.settimeout(0)
                    LOG.debug(mylib.rar.decompression('down', self.localpath)) #解压文件
                    self.socket.settimeout(60)
                    LOG.info('成功解压到%s' % self.localpath)
                    self.result += ['成功解压到', self.localpath, '\n']
                #================下载文件================= 
                for flag in re.split('\|', data[step]):
                    #================杀进程=================
                    if step == 'kill':
                        self.result.append(runCMD(r'taskkill /f /im %s' % flag))
                    #================杀进程=================
                    #================开进程=================
                    elif step == 'open':
                        self.result.append(runCMD('start "" /d "%s" "%s"' % (self.localpath, flag)))
                    #================开进程=================
                    #================CMD命令=================
                    elif step == 'cmd':
                        self.result += [runCMD(flag), '\n']
                    #================CMD命令=================
                    #================修改config文件=================
                    elif step == 'conf':
                        para = re.split('-', data[step])
                        CONF.save(para[0], para[1], para[2])
                        fileRestart = open('restart.bat', 'w')
                        cmds = r'''
                                taskkill /f /im client.exe
                                taskkill /f /im gmclient_watcher.exe
                                start.vbs
                                del /q /f restart.bat
                                '''
                        fileRestart.write(cmds)
                        fileRestart.close()
                        os.system('restart.bat')
                    #================修改config文件=================
                    #================自我更新=================
                    elif step == 'update':
                        chkPath(r'.\update')
                        os.popen(r'del /q /f .\update\*.*')
                        LOG.debug(mylib.rar.decompression('down', '.\\update\\')) #解压update文件
                        fileUpdate = open('update.bat', 'w')
                        cmds = r'''
                                taskkill /f /im client.exe
                                taskkill /f /im gmclient_watcher.exe
                                ping -n 2 127.0.0.1
                                copy /y ".\update\*.*" ".\"
                                start.vbs
                                del /q /f update.bat
                                '''
                        fileUpdate.write(cmds)
                        fileUpdate.close()
                        os.system('update.bat')
                    #================自我更新=================
                    #================删除文件=================
                    elif step == 'delete':
                        r = runCMD('del /q /f "%s%s"' % (self.localpath, flag))
                        if r:
                            self.result.append(r)
                        else:
                            self.result += ['成功删除', flag, '\n']
                    #================删除文件=================
            self.result = ''.join([self.fip, ' : done\n', self.localpath, '\n'] + self.result)
        except :
            self.result = ''.join([self.fip, ' error : ', format_exc(), '\n', self.localpath, '\n'] + self.result)
            LOG.error(self.result)
            

    def chkGMClient(self):
        global GMPORT
        netcmd = os.popen('netstat -na')
        port_info = netcmd.read()
        gmport_info = re.findall('\s0\.0\.0\.0:%s\s' % GMPORT, port_info)
        if gmport_info:
            self.GMlogin()

    def GMlogin(self):
        global USER, PASSWD
        """登陆msg服务器"""
        msg_data = ''.join(['\x08\x01\x12',
                            chr(USER.__len__()),
                            USER,
                            '\x1a',
                            chr(PASSWD.__len__()),
                            PASSWD])
        len_msg_data = len(msg_data)
        string = pack("<HLHHL%ss" % len_msg_data, #第一和第二字段宽度对换
                      len_msg_data + 12, #12 = 4+2+2+2+4-2
                      0xAAAC, # magic code
                      len_msg_data + 12,
                      0x9001,
                      0,
                      msg_data)
        self.socket.sendall(string)

if __name__ == '__main__':
    os.system('title test_manage')
    PORT = CONF.getPort()
    GMPORT = CONF.getGMPort()
    SERVER = CONF.getServer()
    PATH = CONF.getCltPath()
    USER = CONF.getUser()
    PASSWD = CONF.getPasswd()
    IP = _getIP()
    while 1:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((SERVER, PORT))
            LOG.info('connecting ...')
            sock.settimeout(60)
            ManageClient(sock)
        except:
            os.system('taskkill /f /im gmclient_watcher.exe')
            LOG.error(format_exc())
        sleep(30)
