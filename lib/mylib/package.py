#coding=gbk
from os import system
from os import path as ospath
from struct import unpack, pack, calcsize

from mylib.settings import PACKAGE_SIZE
from mylib.other import runCMD,chkPath
from mylib.log import LOG
import mylib.rar


def getBasicData():
    pass
    

def pack1(cltlist_string, cmdpack):  #指令包
    mdata_len = cltlist_string.__len__() + cmdpack.__len__()
    package = pack('<HLHHL%ss'%mdata_len, 12 + mdata_len, 
                                          0xAAAC, 
                                          12 + mdata_len, 
                                          0x0001, 
                                          0, 
                                          '%s%s'%(cltlist_string, cmdpack))
    return package                   

def pack2(result):  #反馈包
    package = pack('<HLHHL%ss'%result.__len__(), 12 + result.__len__(), 
                                                 0xAAAC, 
                                                 12 + result.__len__(), 
                                                 0x0002, 
                                                 0, 
                                                 result)
    return package
        
def pack3(path, names):
        packages = []
        chkPath(r'.\temp')
        for n in names:
            if n == '*.*' or ospath.exists('%s%s'%(path, n)):
                runCMD('copy /y "%s%s" ".\\temp\\%s"'%(path, n, n))
            else:
                raise Exception('%s%s not exists!'%(path, n))
        LOG.debug(mylib.rar.compression('down', '.\\temp\\', names, False))
        LOG.info('压缩文件%s'%names)
        data = open(r'.\temp\down.rar','rb').read()
        filepack_len = data.__len__()/PACKAGE_SIZE
        filepack_handler = pack('<HLHHL', 12 + PACKAGE_SIZE, 
                                          0xAAAC, 
                                          12 + PACKAGE_SIZE, 
                                          0x0003, 
                                          0)
        for i in range(filepack_len):
            packages += [filepack_handler, data[i*PACKAGE_SIZE:(i+1)*PACKAGE_SIZE]]
        filepack_handler = pack('<HLHHL', 12 + data.__len__() - filepack_len * PACKAGE_SIZE, 
                                          0xAAAC, 
                                          12 + data.__len__() - filepack_len * PACKAGE_SIZE, 
                                          0x0003, 
                                          0)
        packages += [filepack_handler, data[filepack_len * PACKAGE_SIZE:]]
        packages = ''.join(packages)
        LOG.info('send filepackage_size is %s Byte'%packages.__len__())
        return packages

def pack4(ip):
        packages = []
        data = open(r'.\temp\up.rar','rb').read()
        dname = '%s_up'%ip
        filepack_handler = pack('<HLHHLH%ss'%dname.__len__(), 14 + dname.__len__() + PACKAGE_SIZE, 
                                                              0xAAAC, 
                                                              14 + dname.__len__() + PACKAGE_SIZE, 
                                                              0x0004, 
                                                              0, 
                                                              dname.__len__(),
                                                              dname)
        filepack_len = data.__len__()/PACKAGE_SIZE
        for i in range(filepack_len):
            packages += [filepack_handler, data[i*PACKAGE_SIZE:(i+1)*PACKAGE_SIZE]]
        filepack_handler = pack('<HLHHLH%ss'%dname.__len__(), 14 + data.__len__() - filepack_len * PACKAGE_SIZE + dname.__len__(), 
                                                              0xAAAC, 
                                                              14 + data.__len__() - filepack_len * PACKAGE_SIZE + dname.__len__(), 
                                                              0x0004, 
                                                              0, 
                                                              dname.__len__(),
                                                              dname)
        packages += [filepack_handler, data[filepack_len * PACKAGE_SIZE:]]
        packages = ''.join(packages)
        LOG.info('send filesize is %s Byte'%packages.__len__())
        return packages
 
def pack5():    #获取client列表操作包
        return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x05\x00\x00\x00\x00\x00'
    
def pack6(heartID):    #心跳包
        heartIDString = pack('<L',heartID)
        return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x06\x00%s'%heartIDString

def packSrvEnd():
        return '\x0c\x00\xac\xaa\x00\x00\x06\x00\xf0\xf0\x00\x00\x00\x00'

def packCltEnd():   #给客户端的包发送完成信息
        return '\x0c\x00\xac\xaa\x00\x00\x06\x00\xff\xff\x00\x00\x00\x00'
    
def packCtrlEnd():   #给控制端的包发送完成信息
        return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x00\xff\x00\x00\x00\x00'
    
def make_response_app(response_code):   
        #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4), response_code(2)
        message_pack_header_def='<HLHHLH'
        package = pack(message_pack_header_def,
                       calcsize(message_pack_header_def) -2,
                       0xABCD,
                       calcsize(message_pack_header_def) -2,
                       0x7002,
                       0,
                       response_code)
        return package
    
def make_response_clt(encoded):  #logined
        #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4)
        message_pack_header_def='<HLHHL'
        package = '%s%s'%(pack(message_pack_header_def,
                               calcsize(message_pack_header_def) - 2 +len(encoded),
                               0xABDE,
                               calcsize(message_pack_header_def) - 2 +len(encoded),
                               0x9002,
                               0),
                          encoded)
        return package
    
def make_transmit(encoded):
        #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4)
        message_pack_header_def='<HLHHL'
        package = "%s%s" %(pack(message_pack_header_def,
                                calcsize(message_pack_header_def) - 2 +len(encoded),
                                0xABDE,
                                calcsize(message_pack_header_def) - 2 +len(encoded),
                                0x9003,
                                0, 
                                ),
                           encoded)
        return package