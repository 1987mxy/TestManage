#coding=gbk

import logging
from sys import stdout
from os import path,mkdir,popen
from win32gui import GetWindowDC
from win32ui import CreateDCFromHandle, CreateBitmap
from win32api import EnumDisplayMonitors
from win32con import SRCCOPY
from mylib.config import CONF

import mylib.settings
LOG = None

class mylog(object):
    def __init__(self, logger):
        self.logger = logger
        if path.exists('config.ini'):
            mylib.settings.Status = CONF.getStatus()
    
    def formatHex(self, string):
        hexlist = []
        for s in string:
            hexlist.append('%02x '%ord(s))
        return ''.join(hexlist)
    
    def critical(self, string, argument = None):   #high
        if  mylib.settings.Status == 'release':
            if argument:
                self.logger.critical('%s%s'%(string, argument.__len__()))
            else:
                self.logger.critical(string)
        elif  mylib.settings.Status == 'debug':
            if argument:
                self.logger.critical('%s%s'%(string, self.formatHex(argument)))
            else:
                self.logger.critical(string)
    
    def error(self, string, argument = None):
        if mylib.settings.Status == 'release':
            if argument:
                self.logger.error('%s%s'%(string, argument.__len__()))
            else:
                self.logger.error(string)
        elif mylib.settings.Status == 'debug':
            if argument:
                self.logger.error('%s%s'%(string, self.formatHex(argument)))
            else:
                self.logger.error(string)

    def warning(self, string, argument = None):
        if mylib.settings.Status == 'release':
            if argument:
                self.logger.warning('%s%s'%(string, argument.__len__()))
            else:
                self.logger.warning(string)
        elif mylib.settings.Status == 'debug':
            if argument:
                self.logger.warning('%s%s'%(string, self.formatHex(argument)))
            else:
                self.logger.warning(string)

    def info(self, string, argument = None):
        if mylib.settings.Status == 'release':
            if argument:
                self.logger.info('%s%s'%(string, argument.__len__()))
            else:
                self.logger.info(string)
        elif mylib.settings.Status == 'debug':
            if argument:
                self.logger.info('%s%s'%(string, self.formatHex(argument)))
            else:
                self.logger.info(string)
    
    def debug(self, string, argument = None):  #low
        if mylib.settings.Status == 'release':
            if argument:
                self.logger.debug('%s%s'%(string, argument.__len__()))
            else:
                self.logger.debug(string)
        elif mylib.settings.Status == 'debug':
            if argument:
                self.logger.debug('%s%s'%(string, self.formatHex(argument)))
            else:
                self.logger.debug(string)
                
def _pathrule(logtype, filetype = 'log'):
    from time import strftime,localtime
    time = strftime('%Y-%m-%d %H_%M_%S',localtime())
    if not path.exists("log"):
        mkdir("log")
    return r'./log/%s_%s.%s'%(time, logtype, filetype)
    
def get_screen():
    hwnd = 0
    hwndDC = GetWindowDC(hwnd)
    mfcDC = CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = CreateBitmap()
    MoniterDev = EnumDisplayMonitors(None,None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0,0),(w, h) , mfcDC, (0,0), SRCCOPY)  
    bmpname = _pathrule('error', 'bmp')
    saveBitMap.SaveBitmapFile(saveDC, bmpname)
    
def run_log():
#    runlog
    rlog = logging.getLogger('runlog')
    rlog.setLevel(logging.DEBUG)
    lpath = _pathrule('run')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logfile.setFormatter(fmt)
    rlog.addHandler(logfile)
    if mylib.settings.PRINT_RUNLOG and mylib.settings.PRINT_LOG:
        display = logging.StreamHandler(stdout)
        display.setLevel(logging.INFO)
        rlog.addHandler(display)  #print to screen
#    errorlog
    lpath = _pathrule('error')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.ERROR)
    logfile.setFormatter(fmt)
    rlog.addHandler(logfile)
    myrlog = mylog(rlog)
    return myrlog

#===============================================================================暂不统计性能指数
# def performance_log():
#    plog = mylog.getLogger('performancelog')
#    logging.setLevel(mylog.INFO)
#    lpath = _pathrule('performance')
#    logfile = mylog.FileHandler(lpath, "w")
#    logfile.setLevel(mylog.INFO)
#    fmt = mylog.Formatter("%(message)s")
#    logfile.setFormatter(fmt)
#    logging.addHandler(logfile)
#    if settings.PRINT_PERFORMANCELOG and settings.PRINT_LOG:
#        display = mylog.StreamHandler(stdout)
#        display.setLevel(mylog.INFO)
#        logging.addHandler(display)  #print to scree
#    myplog = mylog(plog)
#    return myplog
#===============================================================================

def uuid_log():
#    runlog
    uuidlog = logging.getLogger('uuidlog')
    uuidlog.setLevel(logging.DEBUG)
    lpath = _pathrule('uuidlog')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logfile.setFormatter(fmt)
    uuidlog.addHandler(logfile)
    return uuidlog

LOG = run_log()
uuidLog = uuid_log()

