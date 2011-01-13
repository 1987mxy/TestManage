import os

def compression(path, files):
    allpath = ''
    for f in files:
        allpath += ' "%s"'%(path + f)
    os.popen(r'del /q /f ".\temp\down.rar"')
    os.popen(r'rar.exe a -ep ".\temp\down.rar"%s'%allpath)

def decompression(sfile, dpath):
    os.popen(r'rar.exe e ".\temp\%s" "%s"'%(sfile, dpath))
    os.popen(r'del /q /f ".\temp\%s"'%sfile)