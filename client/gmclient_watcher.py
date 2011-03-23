#coding=gbk

import sys
sys.path.append('..\\lib')

import socket
import traceback
from time import sleep

from mylib import log

class GMClient(object):
    def __init__(self, sock):
        self.switch = True
        self.socket = sock
        self.gamestatus = 0
    
    def receive(self):
        pdata = ''
        while self.switch:
            rdata = self.socket.recv(4096)
            log.LOG.debug('receive raw_string from GMClient : %s'%rdata.__len__())
            if not rdata:
                log.LOG.error('GMClient disconnect...')
                self.close()
            else:
                pdata = self.parseHead(pdata + rdata)
                
    def parseHead(self, data):
        if len(data) >= 6:
            head = unpack('<LH', data[:6])
            if head[1] <= len(data):
                mdata = data[ : head[1] + 2]
                data = data[head[1] + 2 : ]
                package = unpack("<LHHHBB%ss"%(head[1]-12), mdata)
                if head[0] == 0x21332621 and package[3] == 0x4101:    #四步校验消息
                    if package[4] == '1':
                        self.gamestatus += 1
                    elif package[4] == '2':
                        self.gamestatus = 0
                elif head[0] == 0x21332621 and package[3] == 0x4095:    #游戏进程关闭消息
                    if self.gamestatus > 0 and self.gamestatus < 4:
                        log._get_screen()
                        log.LOG.error("Oh No! Play game failed!")
                data = self.parseHead(data)
        return data        

if __name__ == '__main__':
    GMSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        try:
            GMSocket.connect(('127.0.0.1', int(sys.argv[1])))
            GMSocket.settimeout(1)
            GM = GMClient(GMSocket)
            GM.receive()
        except Exception, e:
            if str(e) == "(10056, 'Socket is already connected')":
                log.LOG.info('GMClient connecting ...')
            else:
                log.LOG.error('GMClient : %s'%traceback.format_exc())
        sleep(30)