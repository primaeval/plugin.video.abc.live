import xbmcaddon,xbmc
import time
import livestreamersrv
try:
    port = int(xbmcaddon.Addon(id='plugin.video.abc.live').getSetting('port'))
except:
    port = 6666
livestreamersrv.start(port)

monitor = xbmc.Monitor()
while not monitor.abortRequested():
    # Sleep/wait for abort for 10 seconds
    if monitor.waitForAbort(10):
        # Abort was requested while waiting. We should exit
        livestreamersrv.stop(port)
        break
    xbmc.log("plugin.video.abc.live tick %s" % time.time(), level=xbmc.LOGDEBUG)
