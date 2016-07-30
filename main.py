from xbmcswift2 import Plugin

import xbmc,xbmcaddon,xbmcvfs,xbmcgui
import re

import requests


import urllib

plugin = Plugin()



@plugin.route('/play/<channel>')
def play(channel):
    r = requests.get("http://iview.abc.net.au/auth/flash/")
    xml = r.content
    match = re.search(r'<tokenhd>(.*?)</tokenhd>', xml, flags=(re.DOTALL | re.MULTILINE))
    token = match.group(1).strip()

    try:
        port = int(xbmcaddon.Addon(id='plugin.video.abc.live').getSetting('port'))
    except:
        port = 6666
    
    urls = {
    "ABC1": "http://127.0.0.1:%s/?%s" % (port,urllib.quote("%s" % "hds://http://abctvlivehds-lh.akamaihd.net/z/abc1_1@360322/manifest.f4m?hdcore=true&hdnea=%s pvswf=http://iview.abc.net.au/assets/swf/cineramaWrapper_Acc_018.swf?version=0.2" % token)),
    "ABC2": "http://127.0.0.1:%s/?%s" % (port,urllib.quote("%s" % "hds://http://abctvlivehds-lh.akamaihd.net/z/abc2_1@17511/manifest.f4m?hdcore=true&hdnea=%s pvswf=http://iview.abc.net.au/assets/swf/cineramaWrapper_Acc_018.swf?version=0.2" % token)),
    "ABC3": "http://127.0.0.1:%s/?%s" % (port,urllib.quote("%s" % "hds://http://abctvlivehds-lh.akamaihd.net/z/abc3_1@62060/manifest.f4m?hdcore=true&hdnea=%s pvswf=http://iview.abc.net.au/assets/swf/cineramaWrapper_Acc_018.swf?version=0.2" % token)),
    "ABC Kids": "http://127.0.0.1:%s/?%s" % (port,urllib.quote("%s" % "hds://http://abctvlivehds-lh.akamaihd.net/z/abckids_1@390083/manifest.f4m?hdcore=true&hdnea=%s pvswf=http://iview.abc.net.au/assets/swf/cineramaWrapper_Acc_018.swf?version=0.2" % token)),
    "ABC News 24": "http://127.0.0.1:%s/?%s" % (port,urllib.quote("%s" % "hds://http://abcnews24livehds-lh.akamaihd.net/z/news24_1@321136/manifest.f4m?hdcore=true&hdnea=%s pvswf=http://iview.abc.net.au/assets/swf/cineramaWrapper_Acc_018.swf?version=0.2" % token)),
    }
    if channel in urls:
        url = urls[channel]

    item ={'label':channel, 'path':url, 'is_playable': True}
    return plugin.set_resolved_url(item)

    
@plugin.route('/')
def index():
    channels = ["ABC1", "ABC2", "ABC3", "ABC Kids", "ABC News 24"]
    items = []
    for channel in channels:
        items.append({
            'label': channel,
            'path': plugin.url_for('play',channel=channel),
            'thumbnail': "special://home/addons/plugin.video.abc.live/resources/img/%s.png" % channel,
            'is_playable': True
        })

    return items


if __name__ == '__main__':
    plugin.run()
