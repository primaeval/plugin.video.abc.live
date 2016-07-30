import xbmcaddon
import livestreamersrv
try:
    port = int(xbmcaddon.Addon(id='plugin.video.abc.live').getSetting('port'))
except:
    port = 6666
livestreamersrv.start(port)