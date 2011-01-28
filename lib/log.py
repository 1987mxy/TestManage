# -*- encoding: utf-8 -*-
import logging,sys
import settings
from os import path,mkdir


def _pathrule(type):
    from time import strftime,localtime
    time = strftime('%Y-%m-%d %H_%M_%S',localtime())
    if not path.exists("log"):
        mkdir("log")
    return r'.\log\%s %s.log'%(time,type)
    
def run_log():
    rlog = logging.getLogger('runlog')
    rlog.setLevel(logging.DEBUG)
    lpath = _pathrule('run')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logfile.setFormatter(fmt)
    rlog.addHandler(logfile)
    if settings.PRINT_RUNLOG and settings.PRINT_LOG:
        rlog.addHandler(logging.StreamHandler(sys.stdout))  #print to screen
    return rlog
    
def error_log():
    elog = logging.getLogger('runlog')
    lpath = _pathrule('error')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.ERROR)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logfile.setFormatter(fmt)
    elog.addHandler(logfile)
    return elog
            
def performance_log():
    plog = logging.getLogger('performancelog')
    plog.setLevel(logging.INFO)
    lpath = _pathrule('performance')
    logfile = logging.FileHandler(lpath, "w")
    logfile.setLevel(logging.INFO)
    fmt = logging.Formatter("%(message)s")
    logfile.setFormatter(fmt)
    plog.addHandler(logfile)
    if settings.PRINT_PERFORMANCELOG and settings.PRINT_LOG:
        plog.addHandler(logging.StreamHandler(sys.stdout))  #print to scree
    return plog