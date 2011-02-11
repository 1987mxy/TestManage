import os

def compression(rar, spath, files):
    allpath = ''
    for f in files:
        allpath += ' "%s"'%(spath + f)
    os.popen(r'del /q /f ".\temp\%s.rar"'%rar)
    cmd = r'rar.exe a -ep -df ".\temp\%s.rar"%s'%(rar, allpath)
    result = os.popen(cmd).read()
    return '%s\n%s'%(cmd, result)

def decompression(rar, dpath):
    cmd = r'rar.exe e -o+ ".\temp\%s.rar" "%s"'%(rar, dpath)
    result = os.popen(cmd).read()
    os.popen(r'del /q /f ".\temp\%s.rar"'%rar)
    return '%s\n%s'%(cmd, result)
