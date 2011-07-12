#coding=gbk
from os import popen,path
from time import sleep
from re import split

from mylib import log

def runCMD(command):
    result = popen(command)
    result = result.read()
    strlog = '[%s]%s'%(command, result)
    log.LOG.debug(strlog)
    return result

def chkPath(filepath):
    if not path.exists(filepath):
        runCMD(r'mkdir "%s"'%filepath)
        sleep(3)
        
#def killProcess(processName):
#    tasklist = popen('tasklist /FI "IMAGENAME eq %s"'%processName).readlines()
#    result = ''
#    if tasklist:
#        for line in tasklist[3:]:
#            pid = split('\s+', line, 2)[1]
#            result = runCMD('killprocess.exe %s' % pid)
#            if processName in popen('tasklist /FI "IMAGENAME eq %s"'%processName).read():
#                log.LOG.error('kill process fail : %s'%result)
#            else:
#                result = '关闭%s进程成功\n'%processName
#    return result

def killProcess(processName):
    i = 0
    while processName.lower() in popen('tasklist /FI "IMAGENAME eq %s"'%processName).read().lower():
        popen('start /B taskkill /F /IM %s /T'%processName)
        if i>=5:
            log.LOG.error('关闭%s进程失败\n'%processName)
        else:
            i+=1
            sleep(1)
    if i>0:
        return '关闭%s进程成功\n'%processName
    else:
        return ''