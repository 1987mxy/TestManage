import os
from logging import getLogger

def compression(spath, files):
    allpath = ''
    for f in files:
        allpath += ' "%s"'%(spath + f)
    os.popen(r'del /q /f ".\temp\up.rar"')
    os.popen(r'rar.exe a -ep -df ".\temp\up.rar"%s'%allpath)

def decompression(dpath):
    os.popen(r'rar.exe e -o+ ".\temp\down.rar" "%s"'%dpath)
    os.popen(r'del /q /f ".\temp\down.rar"')
