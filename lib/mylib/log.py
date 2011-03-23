# -*- encoding: utf-8 -*-
import logging
from sys import stdout
from os import path,mkdir
from win32gui import GetWindowDC
from win32ui import CreateDCFromHandle, CreateBitmap
from win32api import EnumDisplayMonitors
from win32con import SRCCOPY

import mylib.settings
LOG = None

def _pathrule(logtype, filetype = 'log'):
    from time import strftime,localtime
    time = strftime('%Y-%m-%d %H_%M_%S',localtime())
    if not path.exists("log"):
        mkdir("log")
    return r'./log/%s_%s.%s'%(time, logtype, filetype)
    
def _get_screen():
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
    return rlog

#===============================================================================性能指数暂时不用
# def performance_log():
#    plog = logging.getLogger('performancelog')
#    plog.setLevel(logging.INFO)
#    lpath = _pathrule('performance')
#    logfile = logging.FileHandler(lpath, "w")
#    logfile.setLevel(logging.INFO)
#    fmt = logging.Formatter("%(message)s")
#    logfile.setFormatter(fmt)
#    plog.addHandler(logfile)
#    if settings.PRINT_PERFORMANCELOG and settings.PRINT_LOG:
#        display = logging.StreamHandler(stdout)
#        display.setLevel(logging.INFO)
#        plog.addHandler(display)  #print to scree
#    return plog
#===============================================================================

LOG = run_log()
