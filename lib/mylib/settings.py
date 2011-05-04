#coding=gbk

#===============================================================================
# parameter
#===============================================================================

class ServiceParameter:
    port = None
    magicCode = None
    heartCode = None

TestManage = ServiceParameter()
TestManage.port = 8782
TestManage.magicCode = 0xAAAC
TestManage.heartCode = 0x0006

VirtualMessagetoClient = ServiceParameter()
VirtualMessagetoClient.port = 16667
VirtualMessagetoClient.magicCode = 0xABDE
VirtualMessagetoClient.heartCode = 0x9006
    
VirtualMessagetoService = ServiceParameter()
VirtualMessagetoService.port = 13340
VirtualMessagetoService.magicCode = 0xABCD
VirtualMessagetoService.heartCode = None

#===============================================================================
# log
#===============================================================================

PRINT_LOG = True

PRINT_RUNLOG = True

PRINT_PERFORMANCELOG = True

#===============================================================================
# program parameter
#===============================================================================

Status = 'debug'

VirtualMessage = True

APPSERVER = r'http://172.16.4.2:8083/campus/api'

#===============================================================================
# PACKAGE
#===============================================================================

PACKAGE_SIZE = 600  #0x0003包长度
