import socket
from mylib import log
from struct import pack, unpack
import time
from traceback import format_exc
import os,re
from mylib.config import CONF

address = (CONF.getServer(),8983)

IP = None

def getIP():
    inf = os.popen('ipconfig')
    ipcfg = inf.readlines()
    for i in xrange(len(ipcfg)):
        lineinf = re.findall('^\s+IP[^:]+: ([^\r]+)\s$', ipcfg[i])   
        if lineinf and re.findall('^\s+[^:]+: ([^\r]+)\s$', ipcfg[i + 2]):
            return re.split('\.', lineinf[0])[-1]

class testClt():
    def __init__(self, sock):
        self.sock = sock
        self.switch = True
        self.pingQueue = []
        self.i = 0
        
    def makeHeart(self, number):
        return pack('<HHLH',10,0x9527,number,IP)
    
    def send(self):
        string = self.makeHeart(self.i)
        self.pingQueue.append(time.time())
        self.sock.sendall(string)
        log.heartLog.info('sent Heart No.%s to %s'%(self.i, str(address)))
        self.i+=1

    def receive(self):
        old = ''
        while self.switch:
            data = self.sock.recv(2048)
            if data:
                old = self.parse(old + data)
            else:
                Exception('socket closed!')
    
    def parse(self, data):
        if len(data) >= 4:
            head = unpack('<HH', data[:4])
            if head[0] <= len(data):
                mdata = data[ : head[0]]
                data = data[head[0] : ]
                if head[1] == 0x9527:
                    ping = time.time() - self.pingQueue.pop(0)
                    number = unpack('<LH',mdata[4:])[0]
                    log.heartLog.info('receive Heart No.%s from %s spend time %s'%(number, str(address), ping))
                    time.sleep(2)
                    self.send()
                else:
                    Exception('receive FIFA package from %s : %s'(str(address), mdata.__repr__()))
                data = self.parse(data)
        return data

if __name__ == '__main__':
    IP = int(getIP())
    log.heart_log()
    while True:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(6)
            s.connect(address)
            b = testClt(s)
            b.send()
            b.receive()
        except:
            log.heartLog.error('%s %s'%(str(address), format_exc()))
            s.close()
            time.sleep(10)