from os import popen,path
from time import sleep

from mylib.log import LOG


def runCMD(command):
    result = popen(command)
    result = result.read()
    strlog = '[%s]%s'%(command, result)
    LOG.info(strlog)
    return result

def chkPath(filepath):
    if not path.exists(filepath):
        runCMD(r'mkdir "%s"'%filepath)
        sleep(3)