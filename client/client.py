#coding=gbk
import sys
sys.path.append('..\\lib')

import socket,os,re,win32file,time,struct
import log
import config
from _winreg import *

IP = None
LOG = None
PATH = {}
CONF = None

def getIP():
    inf = os.popen('ipconfig')
    ipcfg = inf.readlines()
    for i in xrange(len(ipcfg)):
        lineinf = re.findall('^\s+IP[^:]+: ([^\r]+)\s$', ipcfg[i])   
        if lineinf and re.findall('^\s+[^:]+: ([^\r]+)\s$', ipcfg[i+2]):
            return lineinf[0]

def findPath(flag):
    global LOG,PATH,CONF
    r = win32file.GetLogicalDrives()
    for d in range(2,27):
        if(r>>d&1):
            import string
            drive = '%s:\\'%string.ascii_letters[d]
            for localpath,fields,files in os.walk(drive):
                if flag in files:
                    if open(r'%s\%s'%(localpath, flag), 'r').read() == '95279527':
                        LOG.info('localpath: %s\\'%localpath)
                        CONF.save(flag, localpath)
                        PATH[flag] = localpath
                        print '%s\\'%localpath
                        return '%s\\'%localpath
    LOG.info('localpath: path is none!')
    return ''

def runcmd(command):
    global LOG
    result = os.popen(command)
    result = result.read()
    strlog = '[%s]%s'%(command, result)
    LOG.info(strlog)
    return result

def manageChar(path, char):   #����ͨ����õ���Ӧ�ļ��б�,uplogʱ+ip��
    filename = []
    print char.__repr__()
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
        global PATH, LOG
        self.request = sock
        self.reset()
        self.receive()
        
    def send(self):
        for pack in self.spack:
            LOG.debug('send to Service : %s'%pack.__repr__())
            self.request.sendall(pack)
    
    def reset(self):
        self.search = ''
        self.spack = ['']
        self.rpack = []
        self.localpath = ''
        self.result = ''
        self.switch = True
    
    def receive(self):
        pdata = ''
        while self.switch:
            rdata = self.request.recv(4096)
            LOG.debug('receive raw_string : %s'%rdata.__repr__())
            if not rdata:
                LOG.error('disconnect...%s'%addr)
                del(CHList[addr])
                self.switch = False
            else:
                pdata = self.parseHead(pdata + rdata)
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack('<LH', data[:6])
            if head[1] == 0xffff:
                self.do()
                self.send()
                if self.search:
                    PATH[self.search]=findPath(self.search)
                LOG.info('='*30)
                self.reset()
                data = data[head[0]:]
            if head[0] <= len(data):
                mdata = data[6:head[0]]
                data = data[head[0]:]
                if head[1] != 0xffff:
                    self.rpack.append([head[0], head[1], mdata])
                    LOG.info('received handler : [%d, %2x]'%(head[0], 
                                                             head[1]))
                    LOG.debug('received package : %s'%mdata.__repr__())
                self.parseHead(data)
        return data
    
    def do(self):
        global IP, PATH
        for len, type, data in self.rpack:
            if type == 0x0001:
                data = self.readData(data)
                if data['ip'] == IP:
                    self.fip = IP
                else:
                    t = re.split('\.',IP)
                    t = t[t.__len__()-1]
                    self.fip = '%s_%s'%(data['ip'], t)
                if 'open' in data.keys() or 'down' in data.keys() or 'up' in data.keys() or 'delete' in data.keys(): 
                    if data['localpath'] in PATH.keys() and os.path.exists(PATH[data['localpath']] + data['localpath']):
                        self.localpath = PATH[data['localpath']]
                        self.operation(data)
                    else:
                        self.result = '%s: path is none!\n%s'%(self.fip, '=' * 30)
                        self.search = data['localpath']
                        break
                else:
                    if not data['localpath'] in PATH.keys():
                        PATH[data['localpath']]=''
                    self.operation(data)
                break
        for len, type, data in self.rpack:
            if type == 0x0003:
#                filelen = len - 16  #�ļ���С
#                mdata = struct.unpack('<%ss'%filelen, data[10:]) #�ļ�����
                file = open(r'.\temp\down.rar','wb')
#                file.write(mdata[0])
                file.write(data)
                file.close()
                break
        self.packResult()
        self.packEnd()

    #================�������ݱ�=================
    def readData(self,data):
        data = re.findall("(?:^|\<)([^:]*):([^<]*)",data)
        data = dict(data)
        data['ip'] = re.sub('\*', '', data['ip'])
        return data
    #================�������ݱ�=================

    def operation(self,data):
        global IP
        rule = data['step']                 #���������˳��
        try:
            for step in re.split('\|', rule):
                #================�ϴ�Log=================
                if step == 'up':
                    fs = []
                    for f in re.split('\|', data['up']):
                        if f:
                            fs += manageChar(self.localpath, f)
                    if fs:
                        self.packFile(self.localpath, fs)
                    continue
                #================�ϴ�Log=================
                for flag in re.split('\|', data[step]):
                    #================ɱ����=================
                    if step == 'kill':
                        self.result += runcmd(r'taskkill /f /im %s'%flag)
                    #================ɱ����=================
                    #================������=================
                    elif step == 'open':
                        runcmd('start "" /d "%s" "%s"'%(self.localpath, flag))
                    #================������=================
                    #================�����ļ�=================
                    elif step == 'down':
                        if not os.path.exists('%shistory'%self.localpath):
                            runcmd('mkdir "%shistory"'%self.localpath)
                            time.sleep(3)
                        tcmd = '%shistory\\%s'%(self.localpath, flag)
                        runcmd('del /q /f "%s(5)"'%tcmd)
                        runcmd('ren "%s(4)" "%s(5)"'%(tcmd,tcmd))
                        runcmd('ren "%s(3)" "%s(4)"'%(tcmd,tcmd))
                        runcmd('ren "%s(2)" "%s(3)"'%(tcmd,tcmd))
                        runcmd('ren "%s(1)" "%s(2)"'%(tcmd,tcmd))
                        runcmd('copy /y "%s" "%s(1)"'%(self.localpath + flag,tcmd))
                        import rar
                        rar.decompression('down', self.localpath) #��ѹ�ļ�
                        LOG.info('�ɹ������ļ�%s'%flag)
                        self.result += '�ɹ������ļ�%s\n'%flag
                        LOG.info('�ɹ���ѹ��%s'%self.localpath)
                        self.result += '�ɹ���ѹ��%s\n'%self.localpath
                    #================�����ļ�=================
                    #================CMD����=================
                    elif step == 'cmd':
                        runcmd('start %s'%flag)
                    #================CMD����=================
                    #================���Ҹ���=================
                    elif step == 'update':
                        os.popen(r'del /q /f .\update\*.*')
                        import rar
                        rar.decompression('down', '.\\update\\') #��ѹupdate�ļ�
                        os.system('update.bat')
                    #================���Ҹ���=================
                    #================ɾ���ļ�=================
                    elif step == 'delete':
                        r = runcmd('del /q /f "%s%s"'%(self.localpath, flag))
                        if r:
                            self.result += r
                        else:
                            self.result += '�ɹ�ɾ��%s\n'%flag
                    #================ɾ���ļ�=================
            self.result = '%s: done\n%s\n%s\n'%(self.fip, self.localpath, self.result)
        except Exception, e:
            LOG.error(str(e))
            self.result = '%s error:%s\n%s\n%s\n'%(self.fip, str(e), self.localpath, self.result)

    def packResult(self):  #����ָ���
        self.result += '='*30
        package = struct.pack('<LH', 
                              self.result.__len__() + 6, 
                              0x0002)
        package += self.result
        self.spack[0] = package

    def packFile(self, spath, names):  #up������
        ns = []
        for n in names:
            if '\\' in n:
                realn = n.split('\\')[1]
            else:
                realn = n
            ns.append('%s_%s'%(self.fip, realn))
            r = runcmd(r'copy /y "%s%s" ".\temp\%s_%s"'%(spath, n, self.fip, realn))
            r = r[:r.__len__()-1]
            self.result += '%s%s_%s\n'%(r, self.fip, realn)
        os.system('msg %username% "log���ռ�,���������!"')
        import rar
        rar.compression('up', '.\\temp\\', ns)
        LOG.info('�ɹ�ѹ���ļ�')
        self.result += '�ɹ�ѹ���ļ�\n'
        data = open(r'.\temp\up.rar','rb').read()
        dname = '%s_up'%self.fip
        package = struct.pack('<LHH', 
                              8 + dname.__len__() + data.__len__(), 
                              0x0004, 
                              dname.__len__())
        package += (dname + data)
        self.spack.append(package)
        
    def packEnd(self):
        package = struct.pack('<LH', 
                              6, 
                              0xff00)
        self.spack.append(package)

if __name__ == '__main__':
    os.system('title test_manage')
    LOG = log.run_log()
    CONF = config.myConfig()
    PORT = CONF.getPort()
    SERVER = CONF.getServer()
    PATH = CONF.getCltPath()
    IP = getIP()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER, PORT))
    ManageClient(sock)