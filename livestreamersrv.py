# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
#from SocketServer import ThreadingMixIn
import socket
#import thread
import threading
import os, sys

# Add our resources/lib to the python path
try:
   current_dir = os.path.dirname(os.path.abspath(__file__))
except:
   current_dir = os.getcwd()

lib = xbmc.translatePath("special://home/addons/plugin.video.abc.live/resources/lib")
#xbmc.log(lib)
#sys.path.append(os.path.join(current_dir, 'resources', 'lib'))
sys.path.append(lib)
#xbmc.log(repr(sys.path))
#try:
from livestreamer import Livestreamer
#except:
#    sys.exit()

from urllib import unquote


LIVESTREAMER = None
httpd = None


    
def Streamer(wfile, url, quality):
    global LIVESTREAMER
    #i = url.find('|')
    #if i > 0:
    #    params = url[i+1:].replace('&',';')
    #    url = url[:i]
    #    LIVESTREAMER.set_option('http-headers', params)
    import random
    ip =  "101.188.%d.%d" % (random.randint(1,200),random.randint(1,200))
    LIVESTREAMER.set_option("http-headers", {"X-Forwarded-For": ip})
    channel = LIVESTREAMER.resolve_url(url)

    streams = channel.get_streams()
    #for stream in streams:
    #    xbmc.log(stream)
    if not streams:
        raise Exception("No Stream Found!")

    quality_setting = xbmcaddon.Addon(id='plugin.video.abc.live').getSetting('quality')
    if quality_setting:
        quality = quality_setting
    stream = streams[quality]
    fd = stream.open()
    while True:
        buff = fd.read(1024)
        if not buff:
           raise Exception("No Data!")
        try:   
            wfile.write(buff)
        except:
            break
    fd.close()
    fd = None
    #raise Exception("End Of Data!")
    
class StreamHandler(BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        #s.send_header("Server", "Enigma2 Livestreamer")
        #s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        #s.send_header("Server", "Enigma2 Livestreamer")
        #s.send_header("Content-type", "text/html")
        s.end_headers()

        quality = "best"

        url = unquote(s.path[2:])
        try:
            Streamer(s.wfile, url, quality)
        except Exception as ex:
            xbmc.log("{0}".format(ex), 3)
            pass
        #s.wfile.close()

class StoppableHTTPServer(HTTPServer):

    def server_bind(self):
        HTTPServer.server_bind(self)
        self.socket.settimeout(1)
        self.run = True

    def get_request(self):
        while self.run:
            try:
                sock, addr = self.socket.accept()
                sock.settimeout(None)
                return (sock, addr)
            except socket.timeout:
                pass

    def stop(self):
        self.run = False

    def serve(self):
        while self.run:
            self.handle_request()
            
#class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
#   """Handle requests in a separate thread."""

def start(portNum):
    global LIVESTREAMER
    LIVESTREAMER = Livestreamer()
    LIVESTREAMER.set_option('hls-segment-threads', '3')
    LIVESTREAMER.set_option('hds-segment-threads', '3')
    LIVESTREAMER.set_option('stream-segment-threads', '3')

    global httpd
    #httpd = ThreadedHTTPServer(('', portNum), StreamHandler)
    httpd = StoppableHTTPServer(('', portNum), StreamHandler)
    try:
        #thread.start_new_thread(httpd.serve, ())
        t1 = threading.Thread(target = httpd.serve, args = ())
        t1.daemon = True
        t1.start()
        xbmc.log("Livestreamer: Server Starts - {0} on port {1}".format("localhost", portNum), 2)
        
    except Exception as ex:
        xbmc.log("{0}".format(ex), 3)
        #pass
    #xbmc.log("Livestreamer: Server Stops - {0} on port {1}".format("localhost", portNum), 2)
    
def stop(portNum):
    global httpd
    try:
        if httpd is not None:
            httpd.stop()
            xbmc.log("Livestreamer: Server Stops - {0} on port {1}".format("localhost", portNum), 2)
    except Exception as ex:
        xbmc.log("{0}".format(ex), 3)
