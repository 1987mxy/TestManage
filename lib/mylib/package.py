#coding=gbk
from os import system, path
from os import path as ospath
from struct import pack, calcsize
from time import sleep

from mylib.settings import PACKAGE_SIZE
from mylib.other import runCMD,chkPath
from mylib.log import LOG
import mylib.rar


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
    
def pack3_compression(path, names):  #下载更新文件包
        chkPath(r'.\temp')
        for n in names:
            if n == '*.*' or ospath.exists('%s%s'%(path, n)):
                runCMD('copy /y "%s%s" ".\\temp\\%s"'%(path, n, n))
            else:
                raise Exception('%s%s not exists!'%(path, n))
        LOG.debug(mylib.rar.compression('down', '.\\temp\\', names))
        LOG.info('压缩文件%s'%names)
        
def pack3_upload():
        packages = []
        insertHeartFlag = 50
        data = open(r'.\temp\down.rar','rb').read()
        filepack_len = data.__len__()/PACKAGE_SIZE
        filepack_handler = pack('<HLHHL', 12 + PACKAGE_SIZE, 
                                          0xAAAC, 
                                          12 + PACKAGE_SIZE, 
                                          0x0003, 
                                          0)
        for i in range(filepack_len):
            packages += [filepack_handler, data[i*PACKAGE_SIZE:(i+1)*PACKAGE_SIZE]]
            if insertHeartFlag:
                insertHeartFlag -= 1
            else:
                packages.append(pack6())
                insertHeartFlag = 50
        filepack_handler = pack('<HLHHL', 12 + data.__len__() - filepack_len * PACKAGE_SIZE, 
                                          0xAAAC, 
                                          12 + data.__len__() - filepack_len * PACKAGE_SIZE, 
                                          0x0003, 
                                          0)
        packages += [filepack_handler, data[filepack_len * PACKAGE_SIZE:]]
        packages = ''.join(packages)
        LOG.info('send filepackage_size is %s Byte'%packages.__len__())
        return packages
    
def pack4_compression(ip, spath, names):  #上传LOG文件包
        result = ''
        ns = []
        chkPath(r'.\temp')
        for n in names:
            if '\\' in n:
                realn = n.split('\\')[1]
            else:
                realn = n
            ns.append('%s_%s'%(ip, realn))
            r = runCMD(r'copy /y "%s%s" ".\temp\%s_%s"'%(spath, n, ip, realn))
            r = r[:r.__len__()-1]
            result = '%s%s%s_%s\n'%(result, r, ip, realn)
        system('msg %username% "log已收集,请继续测试!"')
        LOG.debug(mylib.rar.compression('up', '.\\temp\\', ns))
        return result

def pack4_upload(ip):
        result = ''
        insertHeartFlag = 50
        packages = []
        LOG.info('成功压缩文件')
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
            if insertHeartFlag:
                insertHeartFlag -= 1
            else:
                packages.append(pack6())
                insertHeartFlag = 50
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
        return [result, packages]
 
def pack5():    #获取client列表操作包
        return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x05\x00\x00\x00\x00\x00'
    
def pack6():    #心跳包
        return '\x0c\x00\xac\xaa\x00\x00\x06\x00\x06\x00\x00\x00\x00\x00'

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
                               calcsize(message_pack_header_def) -2 +len(encoded),
                               0xABDE,
                               calcsize(message_pack_header_def) -2 +len(encoded),
                               0x9002,
                               0),
                          encoded)
        return package
    
def make_transmit(encoded):
        #Total Length(2), magic code(4), Total Length(2), code1(2), reserved(4)
        message_pack_header_def='<HLHHL'
        package = "%s%s" %(pack(message_pack_header_def,
                                calcsize(message_pack_header_def) -2 +len(encoded),
                                0xABDE,
                                calcsize(message_pack_header_def) -2 +len(encoded),
                                0x9003,
                                0),
                           encoded)
        return package