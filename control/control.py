#coding=gbk

import sys
sys.path.append('..\\lib')

import socket
from os import system
from traceback import format_exc
from struct import unpack, pack
from re import sub, split
from datetime import datetime

from mylib.config import CONF
from mylib.log import LOG
from mylib.other import chkPath
import mylib.rar
import mylib.package

PATH = {}
TIME = None
OTHER = ''

def _getFTime():
    time = str(datetime.now())
    time = sub(':', '_', time)
    return time

class NetOperation(object):
    def __init__(self, packages):
        global SERVER, PORT
        self.pdata = ''
        self.r_pack = []
        self.s_pack = packages
        self.other = None
        self.switch = True
        self.socket = None
        self.file = {}

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((SERVER, PORT))
        self.socket.settimeout(30)
        self.socket.sendall(mylib.package.pack6())   #第一个心跳包
        
    def close(self):
        self.switch = False
        self.socket.close()
        
    def send(self):
        self.socket.sendall(self.s_pack)
        LOG.debug('send to Serivce : %s'%self.s_pack.__len__())
        
    def receive(self):
        while self.switch:
            rdata = self.socket.recv(4096)
            if not rdata:
                LOG.error('%s_%s socket is closed!\n'%(SERVER, PORT))
                self.close()
            else:
                LOG.debug('receive raw_string : %s'%rdata.__repr__())
                self.pdata = self.parseHead('%s%s'%(self.pdata, rdata))
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = unpack('<LH', data[:6])
            if head[1] == 0xff00:
                self.close()
                LOG.info('%s receive data done!\n'%SERVER)
            if head[0] <= len(data):
                mdata = data[ : head[0]]
                data = data[head[0] : ]
                if head[1] == 0x0006:
                    self.socket.sendall(mdata)
                    LOG.debug('received heart!')
                elif head[1] != 0xff00:
                    self.r_pack.append([head[0], head[1], mdata])
                    LOG.debug('received head from Service : [%d, %2x]'%(head[0], 
                                                                        head[1]))
                    LOG.debug('received package from Service : %s'%mdata.__repr__())
                data = self.parseHead(data)
        return data
    
    def runCommand(self):
        global PATH
        filesize = 0
        total = 0
        for len, type, data in self.r_pack:
            if type == 0x0002:  #对指令的结果反馈
                LOG.info(data[6:])
                LOG.info('='*30)
                total += 1
            elif type == 0x0004:
                filename_len = unpack('<H',data[6 : 8])[0]   #log文件名长度
                filename = data[8 : filename_len + 8]
                if filename in self.file.keys():
                    self.file[filename].write(data[filename_len + 8 : ])   #补充文件
                else:
                    chkPath(r'.\temp')
                    self.file[filename] = open(r'.\temp\%s.rar'%filename,'wb')
                    self.file[filename].write(data[filename_len + 8 : ])
                filesize += data[filename_len + 8 : ].__len__()
        LOG.info('receive filesize is %s'%filesize)
        LOG.info('response client total %s'%total)
        for filename in self.file.keys():
            self.file[filename].close()
            chkPath(PATH['logpath'])
            LOG.debug(mylib.rar.decompression(filename, PATH['logpath'])) #解压log,此时socket已经断开不需要settimeout
            LOG.info('解压%s到%s\n'%(filename, PATH['logpath']))
            
class MainOperation(object):
    def __init__(self):
        global SERVER,PATH
        self.s_pack = ''
        self.e_pack = mylib.package.packCltEnd()
        self.w_pack = mylib.package.pack5()

    def operation(self, cmdline):
        global OTHER
        cmds = cmdline.split(' ')   #分割参数
        dtldata = CONF.getList(PATH, cmds[0])
        step = dtldata['step'].split('|')
        if 'who' in step:
            self.s_pack = '%s%s'%(self.s_pack, self.w_pack)
        elif 'shutdown' in step:
            self.s_pack = '%s%s'%(self.s_pack, mylib.package.packSrvEnd())
        else:
            cmdpack = self.makeCMDString(dtldata)
            cltlist_string = self.makeCLTString()
            self.s_pack = '%s%s'%(self.s_pack, mylib.package.pack1(cltlist_string, cmdpack))    #先发0x0001包是让server知道该转发给那些玩家
        if 'up' in step:
            dtldata['logpath'] = '%s%s_%s\\'%(dtldata['logpath'], TIME, cmds[1])
            OTHER = 'up'
        if 'down' in step:   #step中没有down就不会产生文件包
            files = dtldata['down'].split('|')
            self.s_pack = '%s%s'%(self.s_pack, mylib.package.pack3(PATH['filepath'], files))
        if 'update' in step:
            self.s_pack = '%s%s'%(self.s_pack, mylib.package.pack3('%supdate\\'%PATH['filepath'], ['*.*']))
            OTHER = 'update'
        
        self.s_pack = '%s%s'%(self.s_pack, self.e_pack)
        try:
            t = NetOperation(self.s_pack)
            t.connect()
            t.send()
            t.socket.settimeout(60)
            t.receive()
            t.runCommand()
        except Exception, e:
            if e.message != 'timed out':
                LOG.error('%s : %s\n'%(SERVER, format_exc()))
            else:
                LOG.error('%s : time out!'%SERVER)
            t.close()
        if OTHER == 'up':
            system('explorer "%s"'%PATH['logpath'])

    def makeCMDString(self, dtldata):
        string = ''
        for key in dtldata.keys():
            string = '%s%s:%s<'%(string, key, dtldata[key])
        return string
        
    def makeCLTString(self):
        cltlist_string = ''
        if PATH['list'] == 'all':
            cltlist_string = '\xff\xff'
        else:
            cltlist = split('[|:.]', PATH['list'])
            for i in range(0, cltlist.__len__(), 5):
                cltlist_string = '%s%s%s%s%s'%(cltlist_string,
                                               chr(int(cltlist[i])),
                                               chr(int(cltlist[i + 1])),
                                               chr(int(cltlist[i + 2])),
                                               chr(int(cltlist[i + 3])))
                if cltlist[i + 4]:            #添加端口号，2字节
                    cltlist_string = '%s%s%s'%(cltlist_string,
                                               chr(int(cltlist[i + 4]) / 256),
                                               chr(int(cltlist[i + 4]) % 256))
                else:
                    cltlist_string = '%s\x00\x00'%cltlist_string
            cltlist_string = '%s%s'%(pack('<H', 
                                          cltlist_string.__len__()),
                                     cltlist_string)
        return cltlist_string

if __name__ == '__main__':
    TIME = _getFTime()
    SERVER = CONF.getServer()
    PORT = CONF.getPort()
    PATH = CONF.getCtrlPath()
    cmds = CONF.getCMD()
    for cmd in cmds:
        MainOperation().operation(cmd)
    system('pause')
