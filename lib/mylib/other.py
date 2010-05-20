from os import popen,path
from time import sleep

from mylib.log import LOG


def runCMD(command):
    result = popen(command)
    result = result.read()
    strlog = '[%s]%s'%(command, result)
    LOG.debug(strlog)
    return result

def chkPath(filepath):
    if not path.exists(filepath):
        runCMD(r'mkdir "%s"'%filepath)
        sleep(3)
        
def killProcess(processName):
    result = runCMD('taskkill /f /im %s'%processName)
    if processName in popen('tasklist /FI "IMAGENAME eq %s"'%processName).read():
        LOG.warning('Process %s do not death!')
    return result