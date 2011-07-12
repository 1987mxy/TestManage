from sys import path
path.append('..\\lib')

import socket
from mylib import log
from struct import unpack
from traceback import format_exc
import threading

class testSrv(object):
    def __init__(self, sock, addr):
        self.address = addr
        self.sock = sock
        
    def receive(self):
        old = ''
        try:
            while True:
                data = self.sock.recv(2048)
                if data:
                    old = self.parse(old + data)
                else:
                    Exception('socket closed!')
        except:
            log.heartLog.error('%s %s'%(str(self.address), format_exc()))
            self.sock.close()
        
    def parse(self, data):
        if len(data) >= 4:
            head = unpack('<HH', data[:4])
            if head[0] <= len(data):
                mdata = data[ : head[0]]
                data = data[head[0] : ]
                if head[1] == 0x9527:
                    number = unpack('<LH',mdata[4:])
                    log.heartLog.info('receive Heart No.%s from %s_%s'%(number[0], number[1], str(self.address)))
                    self.sock.sendall(mdata)
                    log.heartLog.info('return Heart No.%s to %s_%s'%(number[0], number[1], str(self.address)))
                else:
                    Exception('receive FIFA package from %s : %s'(str(self.address), mdata.__repr__()))
                data = self.parse(data)
        return data

if __name__ == '__main__':
    from os import popen
    popen('title HeartTest_Srv')
    log.heart_log()
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('',8983))
    s.listen(5)
    while True:
        try:
            log.heartLog.info('listening ...')
            clt, addr = s.accept()
            clt.settimeout(6)
            a = testSrv(clt, addr)
            threading.Thread(target = a.receive).start()
        except:
            log.heartLog.error(format_exc())
