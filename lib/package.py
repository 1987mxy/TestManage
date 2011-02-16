#coding=gbk
import os
from struct import pack

from settings import PACKAGE_SIZE
from log import LOG
from other import runCMD
import rar


def pack1(cltlist_string, cmdpack):  #ָ���
        package = pack('<LH', 
                       6 + cltlist_string.__len__() + cmdpack.__len__(), 
                       0x0001)
        package = '%s%s%s'%(package, 
                            cltlist_string, 
                            cmdpack)
        return package                   

def pack2(result):  #������
        package = pack('<LH', 
                       result.__len__() + 6, 
                       0x0002)
        package = '%s%s'%(package, result)
        return package
    
def pack3(path, names):  #���ظ����ļ���
        packages = ''
        for n in names:
            if os.path.exists('%s%s'%(path, n)):
                os.popen('copy /y "%s%s" ".\\temp\\%s"'%(path, n, n))
            else:
                raise Exception('%s%s not exists!'%(path, n))
        LOG.debug(rar.compression('down', '.\\temp\\', names))
        LOG.info('ѹ���ļ�%s'%names)
        data = open(r'.\temp\down.rar','rb').read()
        filepack_len = data.__len__()/PACKAGE_SIZE
        LOG.info(filepack_len)
        filepack_handler = pack('<LH', 
                                6 + PACKAGE_SIZE, 
                                0x0003)
        for i in range(filepack_len):
            package = '%s%s'%(filepack_handler, data[i*PACKAGE_SIZE:(i+1)*PACKAGE_SIZE])
            packages = '%s%s'%(packages, package)
        filepack_handler = pack('<LH', 
                                6 + data.__len__() - filepack_len * PACKAGE_SIZE, 
                                0x0003)
        package = '%s%s'%(filepack_handler, data[filepack_len * PACKAGE_SIZE:])
        packages = '%s%s'%(packages, package)
        LOG.info('send filesize is %s Byte'%packages.__len__())
        return packages
    
def pack4(ip, spath, names):  #�ϴ�LOG�ļ���
        result = ''
        packages = ''
        ns = []
        for n in names:
            if '\\' in n:
                realn = n.split('\\')[1]
            else:
                realn = n
            ns.append('%s_%s'%(ip, realn))
            r = runCMD(r'copy /y "%s%s" ".\temp\%s_%s"'%(spath, n, ip, realn))
            r = r[:r.__len__()-1]
            result = '%s%s%s_%s\n'%(result, r, ip, realn)
        os.system('msg %username% "log���ռ�,���������!"')
        LOG.debug(rar.compression('up', '.\\temp\\', ns))
        LOG.info('�ɹ�ѹ���ļ�')
        result = '%s�ɹ�ѹ���ļ�\n'%result
        data = open(r'.\temp\up.rar','rb').read()
        dname = '%s_up'%ip
        filepack_handler = '%s%s'%(pack('<LHH', 
                                        8 + dname.__len__() + PACKAGE_SIZE, 
                                        0x0004, 
                                        dname.__len__()), 
                                   dname)
        filepack_len = data.__len__()/PACKAGE_SIZE
        for i in range(filepack_len):
            package = '%s%s'%(filepack_handler, data[i*PACKAGE_SIZE:(i+1)*PACKAGE_SIZE])
            packages = '%s%s'%(packages, package)
#            LOG.info(package.__repr__())#####################
        filepack_handler = '%s%s'%(pack('<LHH', 
                                        8 + data.__len__() - filepack_len * PACKAGE_SIZE + dname.__len__(), 
                                        0x0004,
                                        dname.__len__()),
                                   dname)
        package = '%s%s'%(filepack_handler, data[filepack_len * PACKAGE_SIZE:])
        packages = '%s%s'%(packages, package)
#        LOG.info(package.__repr__())#####################
        LOG.info('send filesize is %s Byte'%packages.__len__())
        return [result, packages]
 
def pack5():    #��ȡclient�б������
        return '\x06\x00\x00\x00\x05\x00'
    
def pack6():    #������
        return '\x06\x00\x00\x00\x06\x00'

def packCltEnd():   #���ͻ��˵İ����������Ϣ
        return '\x06\x00\x00\x00\xff\xff'
    
def packCtrlEnd():   #�����ƶ˵İ����������Ϣ
        return '\x06\x00\x00\x00\x00\xff'