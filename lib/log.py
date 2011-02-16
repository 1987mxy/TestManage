# -*- encoding: utf-8 -*-
import logging,sys
import settings
from os import path,mkdir

LOG = None

def _pathrule(type):
    from time import strftime,localtime
    time = strftime('%Y-%m-%d %H_%M_%S',localtime())
    if not path.exists("log"):
        mkdir("log")
    return r'./log/%s_%s.log'%(time,type)
    
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
    if settings.PRINT_RUNLOG and settings.PRINT_LOG:
        display = logging.StreamHandler(sys.stdout)
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
#        display = logging.StreamHandler(sys.stdout)
#        display.setLevel(logging.INFO)
#        plog.addHandler(display)  #print to scree
#    return plog
#===============================================================================

LOG = run_log()
