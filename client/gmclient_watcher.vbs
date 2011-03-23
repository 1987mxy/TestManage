Set ws = CreateObject("Wscript.Shell")
ws.run "cmd /c gmclient_watcher.exe " + Wscript.Arguments(0),vbhide