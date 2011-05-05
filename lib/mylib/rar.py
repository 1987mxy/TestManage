from os import popen

def compression(rar, spath, files):
    allpath = ''
    for f in files:
        allpath += ' "%s"'%(spath + f)
    popen(r'del /q /f ".\temp\%s.rar"'%rar)
    cmd = r'start rar.exe a -ep -df ".\temp\%s.rar"%s'%(rar, allpath)
    popen(cmd)
    return cmd

def decompression(rar, dpath, async = True):
    cmd = r'rar.exe e -o+ ".\temp\%s.rar" "%s"'%(rar, dpath)
    if async:
        cmd = 'start %s'%cmd
        popen(cmd)
    else:
        popen(cmd)
        popen(r'del /q /f ".\temp\%s.rar"'%rar)
    return cmd
