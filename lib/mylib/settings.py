#coding=gbk

#===============================================================================
# parameter
#===============================================================================

class ServiceParameter:
    port = None
    magicCode = None
    heartCode = None
    responseCode = None

TestManage = ServiceParameter()
TestManage.port = 8782
TestManage.magicCode = 0xAAAC
TestManage.heartCode = 0x0006
TestManage.responseCode = 0x9ff3

VirtualMessagetoClient = ServiceParameter()
VirtualMessagetoClient.port = 16667
VirtualMessagetoClient.magicCode = 0xABDE
VirtualMessagetoClient.heartCode = 0x9006
VirtualMessagetoClient.responseCode = 0x9ff3
    
VirtualMessagetoService = ServiceParameter()
VirtualMessagetoService.port = 13340
VirtualMessagetoService.magicCode = 0xABCD

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

VirtualMessage = False

APPSERVER = r'http://172.16.4.2:8083/campus/api'

#===============================================================================
# PACKAGE
#===============================================================================

PACKAGE_SIZE = 600  #0x0003包长度

CUTLOG_SIZE = 25000000   #LOG大于25MB时截取LOG尾部25MB内容
