from os import popen
from log import LOG

def runCMD(command):
    result = popen(command)
    result = result.read()
    strlog = '[%s]%s'%(command, result)
    LOG.info(strlog)
    return result        