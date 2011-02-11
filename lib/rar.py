import os

def compression(rar, spath, files):
    allpath = ''
    for f in files:
        allpath += ' "%s"'%(spath + f)
    os.popen(r'del /q /f ".\temp\%s.rar"'%rar)
    os.popen(r'rar.exe a -ep ".\temp\%s.rar"%s'%(rar, allpath))

def decompression(rar, dpath):
    os.popen(r'rar.exe e -o+ ".\temp\%s.rar" "%s"'%(rar, dpath))
    os.popen(r'del /q /f ".\temp\%s.rar"'%rar)
