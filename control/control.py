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
from mylib.other import chkPath
import mylib.rar
import mylib.package
from mylib.log import LOG

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
        self.socket.shutdown()
        
    def send(self):
        self.socket.sendall(self.s_pack)
        LOG.debug('send to Serivce : ', self.s_pack)
        
    def receive(self):
        while self.switch:
            rdata = self.socket.recv(4096)
            if not rdata:
                LOG.error('%s_%s socket is closed!\n'%(SERVER, PORT))
                self.close()
            else:
                LOG.debug('receive raw_string : ', rdata)
                self.pdata = self.parseHead('%s%s'%(self.pdata, rdata))
                
    def parseHead(self, data):
        if len(data) >= 14:
            head = unpack('<HLHHL', data[:14])
            if head[0] + 2 <= len(data):
                mdata = data[ : head[0] + 2]
                data = data[head[0] + 2 : ]
                if head[1] == 0xAAAC:
                    if head[3] == 0xff00:
                        self.close()
                        LOG.info('%s receive data done!\n'%SERVER)
                    elif head[3] == 0x0006:
                        self.socket.sendall(mdata)
                        LOG.debug('received heart!')
                    else:
                        self.r_pack.append([head[0], head[3], mdata])
                        LOG.debug('received head from Service : [%d, %2x]'%(head[0], 
                                                                            head[1]))
                        LOG.debug('received package from Service : %s'%mdata.__repr__())
                else:
                    LOG.error('receive FIFA package from %s : %s'%(SERVER, mdata.__repr__()))
                    self.close()
                data = self.parseHead(data)
        return data
    
    def listen_message(self):
        global PATH
        filesize = 0
        total = 0
        for len, type, data in self.r_pack:
            if type == 0x0002:  #对指令的结果反馈
                LOG.info(data[14:])
                LOG.info('='*30)
                total += 1
            elif type == 0x0004:
                filename_len = unpack('<H',data[14 : 16])[0]   #log文件名长度
                filename = data[16 : filename_len + 16]
                if filename in self.file.keys():
                    self.file[filename].write(data[filename_len + 16 : ])   #补充文件
                else:
                    chkPath(r'.\temp')
                    self.file[filename] = open(r'.\temp\%s.rar'%filename,'wb')
                    self.file[filename].write(data[filename_len + 16 : ])
                filesize += data[filename_len + 16 : ].__len__()
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
        self.s_pack = []
        self.e_pack = mylib.package.packCltEnd()
        self.w_pack = mylib.package.pack5()

    def operation(self, cmdline):
        global OTHER
        cmds = cmdline.split(' ')   #分割参数
        dtldata = CONF.getList(PATH, cmds[0])
        step = dtldata['step'].split('|')
        if 'who' in step:
            self.s_pack.append(self.w_pack)
        elif 'shutdown' in step:
            self.s_pack.append(mylib.package.packSrvEnd())
        else:
            cmdpack = self.makeCMDString(dtldata)
            cltlist_string = self.makeCLTString()
            self.s_pack.append(mylib.package.pack1(cltlist_string, cmdpack))    #先发0x0001包是让server知道该转发给那些玩家
        if 'up' in step:
            dtldata['logpath'] = ''.join([dtldata['logpath'], TIME, '_', cmds[1], '\\'])
            OTHER = 'up'
        if 'down' in step:   #step中没有down就不会产生文件包
            files = dtldata['down'].split('|')
            self.s_pack.append(mylib.package.pack3(PATH['filepath'], files))
        if 'update' in step:
            self.s_pack.append(self.s_pack, mylib.package.pack3('%supdate\\'%PATH['filepath'], ['*.*']))
            OTHER = 'update'
        
        self.s_pack.append(self.e_pack)
        self.s_pack = ''.join(self.s_pack)
        try:
            t = NetOperation(self.s_pack)
            t.connect()
            t.send()
            t.socket.settimeout(60)
            t.receive()
            t.listen_message()
        except Exception, e:
            if e.message == 'timed out':
                LOG.error('%s : time out!'%SERVER)
            else:
                LOG.error('%s : %s\n'%(SERVER, format_exc()))
            t.close()
        if OTHER == 'up':
            system('explorer "%s"'%PATH['logpath'])

    def makeCMDString(self, dtldata):
        string = []
        for key in dtldata.keys():
            string += [key, dtldata[key]]
        return ''.join(string)
        
    def makeCLTString(self):
        cltlist_string = ''
        if PATH['list'] == 'all':
            cltlist_string = '\xff\xff'
        else:
            if PATH['list'][0] == '!':
                cltlist = split('[|:.]', PATH['list'][1:])
                cltlist_string_len = int(cltlist.__len__() * 1.2 + 0xf000)
            else:
                cltlist = split('[|:.]', PATH['list'])
                cltlist_string_len = int(cltlist.__len__() * 1.2)
            if cltlist.__len__()/5 > 10000:   #list中不能超10000个否则包长度字段溢出
                raise Exception('cltlist is too more')
            for i in range(0, cltlist.__len__(), 5):
                cltlist_string +=  [chr(int(cltlist[i])),
                                    chr(int(cltlist[i + 1])),
                                    chr(int(cltlist[i + 2])),
                                    chr(int(cltlist[i + 3]))]
                if cltlist[i + 4]:            #添加端口号，2字节
                    cltlist_string += [chr(int(cltlist[i + 4]) / 256),
                                       chr(int(cltlist[i + 4]) % 256)]
                else:
                    cltlist_string.append('\x00\x00')
            
            cltlist_string = ''.join([chr(cltlist_string_len % 256), chr(cltlist_string_len / 256)] + cltlist_string)
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
