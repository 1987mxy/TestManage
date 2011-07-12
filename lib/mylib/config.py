#coding=gbk
from os import path as ospath
from ConfigParser import ConfigParser

CONF = None

class myConfig(object):
    def __init__(self):
        self.conf = ConfigParser()
        self.conf.read('config.ini')
        
    def getStatus(self):
        return self.conf.get('service', 'status')
    
    def getPort(self):
        return int(self.conf.get('service', 'port'))
    
    def getServer(self):
        return self.conf.get('service', 'server')
    
    def getCltPath(self):
        path = {}
        for flag in self.conf.options('localpath'):
            tpath = self.conf.get('localpath', flag)
            if not ospath.exists(tpath):
                self.save('localpath', flag, '')
            else:
                path[flag] = tpath
        return path

    def save(self, section, item, value):
        self.conf.set(section, item, value)
        self.conf.write(open('config.ini','w+'))
        
#===============================================================================
#    control
#===============================================================================
        
    def getCMD(self):
        cmds = self.conf.get('run','command')
        cmds = cmds.split('|')
        return cmds
        
    def getCtrlPath(self):
        return dict(self.conf.items('path'))

    def getList(self, path, cmd):
        path.update(dict(self.conf.items(cmd)))
        return path
    
#===============================================================================
#    vittual
#===============================================================================
    
    def getUser(self):
        user = self.conf.get('Script','user')
        return user
    
    def getPasswd(self):
        password = self.conf.get('Script', 'password')
        return password
    
    def getGMPort(self):
        return int(self.conf.get('Script', 'gmport'))
    
    def getDelayKill(self):
        return int(self.conf.get('Script', 'delaykill'))
    
CONF = myConfig()