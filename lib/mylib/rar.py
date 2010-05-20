from os import popen

def compression(rar, spath, files, async = True):
    allpath = ''
    for f in files:
        allpath += ' "%s"'%(spath + f)
    popen(r'del /q /f ".\temp\%s.rar"'%rar)
    if async:
        cmd = r'start /B rar.exe a -ep -df ".\temp\%s.rar"%s'%(rar, allpath)
        popen(cmd)
        return cmd
    else:
        cmd = r'rar.exe a -ep -df ".\temp\%s.rar"%s'%(rar, allpath)
        result = popen(cmd).read()
        return '%s\n%s'%(cmd, result)

def decompression(rar, dpath, async = True):
    if async:
        cmd = r'start /B rar.exe e -o+ ".\temp\%s.rar" "%s"'%(rar, dpath)
        popen(cmd)
        return cmd
    else:
        cmd = r'rar.exe e -o+ ".\temp\%s.rar" "%s"'%(rar, dpath)
        result = popen(cmd).read()
        popen(r'del /q /f ".\temp\%s.rar"'%rar)
        return '%s\n%s'%(cmd, result)
