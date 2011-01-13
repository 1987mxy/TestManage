#coding=gbk

import SocketServer,os,re,win32file,time,struct

from _winreg import *

IP = None
LOGGER = None
PATH = {}
PORT = None


def setLog():
    import logging
    logger = logging.getLogger()
    logfile = logging.FileHandler('log.txt', "w")
    logger.addHandler(logfile)
    logger.setLevel(logging.DEBUG)
    _fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logfile.setFormatter(_fmt)
    from sys import stdout
    logger.addHandler(logging.StreamHandler(stdout))
    return logger

def getIP():
    inf = os.popen('ipconfig')
    ipcfg = inf.readlines()
    for i in xrange(len(ipcfg)):
        lineinf = re.findall('^\s+IP[^:]+: ([^\r]+)\s$', ipcfg[i])   
        if lineinf and re.findall('^\s+[^:]+: ([^\r]+)\s$', ipcfg[i+2]):
            return lineinf[0]

def findPath(flag):
    global LOGGER,PATH
    r = win32file.GetLogicalDrives()
    for d in range(2,27):
        if(r>>d&1):
            import string
            drive = '%s:\\'%string.ascii_letters[d]
            for localpath,fields,files in os.walk(drive):
                if flag in files:
                    if open(r'%s\%s'%(localpath, flag), 'r').read() == '95279527':
                        LOGGER.info('localpath: %s\\'%localpath)
                        myConfig().save(flag, localpath)
                        PATH[flag] = localpath
                        print '%s\\'%localpath
                        return '%s\\'%localpath
    LOGGER.info('localpath: path is none!')
    return ''

def runcmd(command):
    global LOGGER
    result = os.popen(command)
    result = result.read()
    strlog = '[%s]%s'%(command, result)
    LOGGER.info(strlog)
    return result

def manageChar(path, char):   #����ͨ����õ���Ӧ�ļ��б�,uplogʱ+ip��
    filename = []
    result = os.popen(r'dir "%s%s"'%(path, char)).read()
    result = re.split(r'\n', result)
    for line in result[5:len(result)-3]:
        filename.append(re.split(' +', line, 3)[3])
    return filename

class myConfig(object):
    def __init__(self):
        import ConfigParser
        self.conf = ConfigParser.ConfigParser()
        self.conf.read('config.ini')
    
    def getPort(self):
        return int(self.conf.get('server', 'port'))    
    
    
    def getPath(self):
        path = {}
        for flag in self.conf.options('localpath'):
            tpath = self.conf.get('localpath', flag)
            if not os.path.exists(tpath):
                self.save(flag, '')
            else:
                path[flag] = tpath
        return path

    def save(self,flag,path):
        self.conf.set('localpath', flag, '%s\\'%path)
        self.conf.write(open('config.ini','w+'))

class workserver(SocketServer.BaseRequestHandler):
    def handle(self):
        global PATH, LOGGER
        self.search = ''
        self.logger = LOGGER
        self.spack = ['']
        self.rpack = []
        self.localpath = ''
        self.result = ''
        self.switch = True
        self.receive()
        self.do()
        self.send()
        if self.search:
            PATH[self.search]=findPath(self.search)
        LOGGER.info('='*30)
        
    def send(self):
        for pack in self.spack:
            self.request.sendall(pack)
        self.request.sendall(struct.pack('<IH', 6, 0xffff))
    
    def receive(self):
        pdata = ''
        while self.switch:
            rdata = self.request.recv(4096)
            pdata = self.parseHead(pdata + rdata)
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = struct.unpack('<IH', data[:6])
            if head[1] == 0xffff:
                self.switch = False
            elif head[0] <= len(data):
                mdata = data[6:head[0]]
                data = data[head[0]:]
                self.rpack.append([head[0], head[1], mdata])
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
            elif type == 0x0003:
#                filelen = len - 16  #�ļ���С
#                mdata = struct.unpack('<%ss'%filelen, data[10:]) #�ļ�����
                file = open(r'.\temp\down.rar','wb')
#                file.write(mdata[0])
                file.write(data[10:])
                file.close()
        self.packResult()

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
                        rar.decompression(self.localpath) #��ѹ�ļ�
                        self.logger.info('�ɹ������ļ�%s'%flag)
                        self.result += '�ɹ������ļ�%s\n'%flag
                        self.logger.info('�ɹ���ѹ��%s'%self.localpath)
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
                        rar.decompression('.\\update\\') #��ѹupdate�ļ�
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
            self.logger.error(str(e))
            self.result = '%s error:%s\n%s\n%s\n'%(self.fip, str(e), self.localpath, self.result)

    def packResult(self):  #����ָ���
        self.result += '='*30
        package = struct.pack('<IH', 
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
            ns.append('%s_%s'%(self.fip, n))
            r = runcmd(r'copy /y "%s" ".\temp\%s_%s"'%(spath + n, self.fip, realn))
            r = r[:r.__len__()-1]
            self.result += '%s%s_%s\n'%(r, self.fip, realn)
        os.system('msg %username% "log���ռ�,���������!"')
        import rar
        rar.compression('.\\temp\\', ns)
        self.logger.info('�ɹ�ѹ���ļ�')
        self.result += '�ɹ�ѹ���ļ�\n'
        data = open(r'.\temp\up.rar','rb').read()
        dname = '%s_up.rar'%self.fip
        package = struct.pack('<IHH', 
                              8 + dname.__len__() + data.__len__(), 
                              0x0003, 
                              dname.__len__())
        package += (dname + data)
        self.spack.append(package)

if __name__ == '__main__':
    os.system('title test_manage')
    LOGGER = setLog()
    PORT = myConfig().getPort()
    PATH = myConfig().getPath()
    IP = getIP()
    try:
        server = SocketServer.TCPServer((IP,PORT),workserver)
        server.serve_forever()
    except Exception, e:
        LOGGER.error(str(e))