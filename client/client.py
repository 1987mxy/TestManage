#coding=gbk

import sys
sys.path.append('..\\lib')

import socket, os, re
from traceback import format_exc
from win32file import GetLogicalDrives
from time import sleep
from struct import unpack, pack

from mylib.log import LOG, uuidLog, get_screen
from mylib.other import runCMD, chkPath, killProcess
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
HEARTTIMEOUT = 60

def _getIP():
    inf = os.popen('ipconfig')
    ipcfg = inf.readlines()
    for i in xrange(len(ipcfg)):
        lineinf = re.findall('^\s+IP[^:]+: ([^\r]+)\s$', ipcfg[i])   
        if lineinf and re.findall('^\s+[^:]+: ([^\r]+)\s$', ipcfg[i + 2]):
            return lineinf[0]

def _findPath(flag):
    global PATH
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

class ManageClient(object):
    def __init__(self, sock):
        global PATH
        self.socket = sock
        self.login = False
        self.e_pack = mylib.package.packCtrlEnd()
        self.msg = Msg()
        self.reset()
        self.receive()
        
    def send(self):
        self.result = ''.join([self.returnIP, ' : done\n', self.localpath, '\n'] + self.result)
        self.s_pack.extend([mylib.package.pack2(''.join(self.result)), self.e_pack])
        self.s_pack = ''.join(self.s_pack)
        self.socket.settimeout(0)
        self.socket.sendall(self.s_pack)
        self.socket.settimeout(HEARTTIMEOUT)
        LOG.debug('send to Service : ', self.s_pack)
        LOG.info('='*30)
        if self.search:
            PATH[self.search] = _findPath(self.search)
        self.reset()
    
    def close(self):
        self.switch = False
        self.socket.close()
    
    def reset(self):
        self.copyLogNames = []  #已复制的LOG需要给compression使用
        self.stepList = []
        self.search = ''
        self.s_pack = []
        self.r_pack = []
        self.localpath = ''
        self.result = []
        self.switch = True
        self.data = {}
    
    def receive(self):
        pdata = ''
        while self.switch:
            rdata = self.socket.recv(4096)
            LOG.debug('receive raw_string from Service : ', rdata)
            if not rdata:
                LOG.error('disconnect...')
                self.close()
            else:
                pdata = self.parseHead('%s%s'%(pdata, rdata))
                
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
                        uuidLog.debug('%s\t%s'%(self.msg.uuid, '%s:%s'%self.socket.getsockname()))
                        if self.msg.code == 0x230d and (not self.msg.arenaEnded.error):
                            GameStatus = os.getenv('GAMESTATUS')    #获取环境变量 
                            if GameStatus != None and int(GameStatus) < 4:
                                get_screen()
                            LOG.info('Arena End info : ', mdata[14:])
                            killProcess('war3.exe')
                            killProcess('starcraft.exe')
                            #os.popen('start "" /d "%s" "GMClient.exe"'%os.getenv('TEMPPATH'))
                            #os.popen('close_war3.exe')
                        elif self.msg.code == 0x230b:
                            pass
                    elif head[3] == 0x9002:
                        self.login = not self.login
                        if self.login:
                            #os.popen('start /B gmclient_watcher.exe %s'%GMPORT)
                            LOG.info('Virtual User logined !')
                        else:
                            killProcess('gmclient_watcher.exe')
                            LOG.info('Virtual User logouted !')
                elif head[1] == 0xAAAC:
                    if head[3] == 0xffff:
                        LOG.info('received head from Service : [%d, %2x]' % (head[0],
                                                                             head[3]))
                        LOG.debug('received package from Service : ', mdata)
                        self.listen_message()
                        if not self.stepList:
                            self.send()
                    elif head[3] == 0x0006:
                        LOG.debug('received heart %s!'%unpack('<L', mdata[-4:]))
                        self.socket.sendall(mdata)
                        if self.stepList:
                            self.operation()
                            if not self.stepList:
                                self.send()
                        if not self.login:
                            self.chkGMClient()
                    else:
                        LOG.info('received handler from Service : [%d, %2x]' % (head[0],
                                                                                head[3]))
                        LOG.debug('received package from Service : ', mdata)
                        self.r_pack.append([head[0], head[3], mdata])
                else:
                    LOG.error('receive FIFA package from %s : ' % SERVER, mdata)
                    self.close()
                data = self.parseHead(data)
        return data
    
    def listen_message(self):
        filesize = 0
        downfile = None
        global IP, PATH
        for len, cmd, data in self.r_pack:
            if cmd == 0x0003:
                if downfile:
                    downfile.write(data[14:])
                else:
                    chkPath(r'.\temp')
                    downfile = open(r'.\temp\down.rar', 'wb')
                    downfile.write(data[14:])
                filesize += len + 2
            elif cmd == 0x0001:
                self.data = self.readString(data[14:]) 
                if 'open' in self.data.keys() or 'down' in self.data.keys() or 'up' in self.data.keys() or 'delete' in self.data.keys(): 
                    if self.data['localpath'] in PATH.keys() and os.path.exists('%s%s'%(PATH[self.data['localpath']], self.data['localpath'])):
                        self.localpath = PATH[self.data['localpath']]
                        os.environ['TEMPPATH'] = self.localpath
                        self.stepList = re.split('\|', self.data['step'])
                    else:
                        self.result.extend([self.returnIP, ' : path is none!\n'])
                        self.search = self.data['localpath']
                        return
                else:
                    if not self.data['localpath'] in PATH.keys():
                        PATH[self.data['localpath']] = ''
                    self.stepList = re.split('\|', self.data['step'])
        if downfile:
            downfile.close()
            LOG.info('receive filesize is %s' % filesize)
        self.operation()
        

    #================解析数据报=================
    def readString(self, string):
        parsedData = dict(re.findall("(?:^|\<)([^:]*):([^<]*)", string))
        parsedData['ip'] = re.sub('\*', '', parsedData['ip'])
        if parsedData['ip'] == IP:
            self.returnIP = IP
        else:
            ipLastPart = re.split('\.', IP)[-1]
            self.returnIP = '%s_%s' % (parsedData['ip'], ipLastPart)
        return parsedData
    #================解析数据报=================

    def operation(self):
        try:
            while len(self.stepList):
                #================上传Log=================
                if self.stepList[0] == 'up':
                    if self.data[self.stepList[0]][0] == '!':
                        notNullWildcard = [uploadFileName for uploadFileName in re.split('\|', self.data[self.stepList[0]][1:]) if uploadFileName]
                        self.copyLog(self.localpath, notNullWildcard, isfull = True)
                    else:
                        notNullWildcard = [uploadFileName for uploadFileName in re.split('\|', self.data[self.stepList[0]]) if uploadFileName]
                        self.copyLog(self.localpath, notNullWildcard)
                    self.stepList[0] = 'chkCopyLog'
                    continue
                #================上传Log=================
                #================下载文件=================
                elif self.stepList[0] == 'down':
                    chkPath('%shistory' % self.localpath)
                    for flag in re.split('\|', self.data[self.stepList[0]]):
                        tcmd = '%shistory\\%s' % (self.localpath, flag)
                        runCMD('del /q /f "%s(5)"' % tcmd)
                        runCMD('ren "%s(4)" "%s(5)"' % (tcmd, flag))
                        runCMD('ren "%s(3)" "%s(4)"' % (tcmd, flag))
                        runCMD('ren "%s(2)" "%s(3)"' % (tcmd, flag))
                        runCMD('ren "%s(1)" "%s(2)"' % (tcmd, flag))
                        runCMD('copy /y "%s%s" "%s(1)"' % (self.localpath, flag, tcmd))
                        runCMD('del /q /f "%s%s"' % (self.localpath, flag))
                        LOG.info('成功下载文件%s' % flag)
                        self.result.append('成功下载文件%s\n'%flag)
                    LOG.debug(mylib.rar.decompression('down', self.localpath)) #异步解压文件
                    self.stepList[0] = 'chkDecompression'
                    continue
                elif self.stepList[0] == 'chkCopyLog':
                        for n in self.copyLogNames:
                            if os.access(r'.\temp\%s'%n, os.F_OK) and os.access(r'.\temp\%s'%n, os.R_OK) and os.access(r'.\temp\%s'%n, os.W_OK) and os.access(r'.\temp\%s'%n, os.X_OK):
                                pass
                            else:
                                return
                        os.popen('start msg %username% "log已收集,请继续测试!"')
                        LOG.debug(mylib.rar.compression('up', '.\\temp\\', self.copyLogNames))
                        self.stepList[0] = 'chkCompression'
                        continue
                elif self.stepList[0] == 'chkCompression':
                    if 'Rar.exe' in os.popen('tasklist /FI "IMAGENAME eq rar.exe"').read():
                        return
                    else:
                        if os.access(r'.\temp\up.rar',os.F_OK):
                            if os.access(r'.\temp\up.rar', os.R_OK) and os.access(r'.\temp\up.rar', os.W_OK) and os.access(r'.\temp\up.rar', os.X_OK):
                                pass
                            else:
                                return
                            package = mylib.package.pack4(self.returnIP)
                            self.result.append('成功压缩文件')
                            self.s_pack.append(package)
                        else:
                            self.result.append('压缩失败!')
                            LOG.error('压缩失败')
                        del(self.stepList[0])
                        continue
                elif self.stepList[0] == 'chkDecompression':
                    if 'Rar.exe' in os.popen('tasklist /FI "IMAGENAME eq rar.exe"').read():
                        return
                    else:
                        for fileName in re.split('\|', self.data['down']):
                            if os.path.exists('%s%s'%(self.localpath, fileName)):
                                LOG.info('%s成功解压到%s' % (fileName, self.localpath))
                                self.result.append('%s成功解压到%s\n' % (fileName, self.localpath))
                            else:
                                self.result.append('%s文件下载失败\n'%fileName)
                                LOG.info('%s文件下载失败\n'%fileName)
                        del(self.stepList[0])
                        continue
                #================下载文件=================
                for flag in re.split('\|', self.data[self.stepList[0]]):
                    #================杀进程=================
                    if self.stepList[0] == 'kill':
                        self.result.append(killProcess(flag))
                    #================杀进程=================
                    #================开进程=================
                    elif self.stepList[0] == 'open':
                        runCMD('start "" /d "%s" "%s"' % (self.localpath, flag))
                        LOG.info('运行文件%s'%flag)
                        self.result.append('运行文件%s'%flag)
                    #================开进程=================
                    #================CMD命令=================
                    elif self.stepList[0] == 'cmd':
                        self.result.append('%s\n'%runCMD(flag))
                    #================CMD命令=================
                    #================修改config文件=================
                    elif self.stepList[0] == 'conf':
                        para = re.split('-', self.data[self.stepList[0]])
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
                    elif self.stepList[0] == 'update':
                        chkPath(r'.\update')
                        os.popen(r'del /q /f .\update\*.*')
                        LOG.debug(mylib.rar.decompression('down', '.\\update\\', False)) #解压update文件
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
                    elif self.stepList[0] == 'delete':
                        delReturn = runCMD('del /q /f "%s%s"' % (self.localpath, flag))
                        if delReturn:
                            self.result.append('%s%s'%(flag, delReturn))
                        else:
                            self.result.append('成功删除%s\n'%flag)
                    #================删除文件=================
                del(self.stepList[0])
        except :
            self.stepList = []
            self.result = [self.returnIP, ' error : ', format_exc(), '\n', self.localpath, '\n'] + self.result
            LOG.error(''.join(self.result))

    def copyLog(self, path, fileNames, isfull = False):   #根据通配符得到相应文件列表,如果直接用通配符无法在文件名中+上IP
        chkPath(r'.\temp')
        for fileName in fileNames:
            dirResult = os.popen(r'dir "%s%s"' % (path, fileName)).readlines()
            if os.path.split(fileName)[0]:
                path += '%s\\'%os.path.split(fileName)[0]
            for line in dirResult[5:-2]:
                dirline = re.split(' +', line[:-1], 3)
                if len(dirline) > 3 and not dirline[3] in ['.','..']:
                    
                    logFileName = r'%s%s'%(path, dirline[3])
                    
                    logFileSize = os.stat(logFileName).st_size
                    if logFileSize < 25000000 or isfull:
                        newFileName = r'.\temp\%s_%s'%(self.returnIP, dirline[3])
                        self.copyLogNames.append('%s_%s'%(self.returnIP, dirline[3]))
                        os.popen(r'start /B copy /y "%s%s" ".\temp\%s_%s"'%(path, dirline[3], self.returnIP, dirline[3]))
                    else:
                        newFileName = r'.\temp\%s_cut_%s'%(self.returnIP, dirline[3])
                        self.copyLogNames.append('%s_cut_%s'%(self.returnIP, dirline[3]))
                        logFile = open(logFileName, 'r+')
                        logFile.seek(logFileSize - 25000000)
                        newFile = open(newFileName, 'w')
                        newFile.write(logFile.read())
                        logFile.close()
                        newFile.close()

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
    runCMD('title test_manage')
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
            sock.settimeout(HEARTTIMEOUT)
            ManageClient(sock)
        except:
            killProcess('gmclient_watcher.exe')
            LOG.error(format_exc())
        sleep(30)
