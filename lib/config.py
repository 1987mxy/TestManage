#coding=gbk
import os
import ConfigParser

class myConfig(object):
    def __init__(self):
        self.conf = ConfigParser.ConfigParser()
        self.conf.read('config.ini')
    
    def getPort(self):
        return int(self.conf.get('service', 'port'))
    
    def getServer(self):
        return self.conf.get('service', 'server')
    
    def getCltPath(self):
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