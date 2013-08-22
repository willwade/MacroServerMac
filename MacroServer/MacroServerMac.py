#!/usr/bin/env python
# Run on mac with
#    python server.py &
# Date: April 2013
# -*- coding: iso-8859-15 -*-
"""
MacroServer for Mac.  Control your mac from another Machine over TCP/IP. 

usage: MindExpressMacroServer [-h] [--host=HOST] [--port=PORT]
                              [--loglevel=LOGLEVEL] [--logfile=LOGFILE]
                              [--notifier=NOTIFIER]

Runs a Mind Express Control Server.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show the version number of this script and exit
  --host=HOST           Allow from one or several ip-address. [default: 0.0.0.0]
  --port=PORT           Change the default Mind Express Port number. [default: 12000]
  --loglevel=LOGLEVEL   Set the logging level. (debug, warning, info) [default: info]
  --logfile=LOGFILE     Where should the logging file be located. 
                        [default: MacroServerMac.log]
  --notifier=NOTIFIER   Do you want to use Growl, Notifier, or None to get notified when 
                        a modifier key pressed? [default: None]
"""
# For debug
import logging
# For the server
import SocketServer
# for the MExpressCall
try:
    from MExpressHandler import MExpressHandler
except ImportError:
    exit('This script requires that `Mexpresshandler` library'
         ' is installed: \n'
         'https://github.com/willwade/MacroServerMac')
# For the line command aspects
try:
    from docopt import docopt
except ImportError:
    exit('This script requires that `docopt` library'
         ' is installed: \n    pip install docopt\n'
         'https://github.com/docopt/docopt')


# for the little GUI
from Tkinter import *
import sys
         
class GrowlMESender(object):
    """https://github.com/kfdm/gntp 
         NB: You need to pip install --upgrade gntp, and then http://www.canebas.org/LWC/Tutorials/Growl_networking/"""
   
    def  __init__(self):
        """GNTP notifier. """
        try:
            import gntp.notifier # Standard
            # Really need to now start up a dummy notifier
            self.growl = gntp.notifier.GrowlNotifier(
                applicationName = "MacroServer",
                notifications = ["Key Modifier","Debug"],
                defaultNotifications = ["Key Modifier"],
                # hostname = "computer.example.com", # Defaults to localhost
                # password = "abc123" # Defaults to a blank password
            )
            self.growl.register()
            self.sendStartUpMessage()
        except ImportError:
            logging.warning('gntp not installed')
   
    def sendStartUpMessage(self):
        """we need a startup message """
        self.growl.notify(
            noteType = "Key Modifier",
            title = "MacroServer Mac started up..",
            description = "Will Wade",
            icon = "http://example.com/icon.png",
            sticky = False,
            priority = -1,
        )


    def sendMessage(self, modifier, state):
        """The main sendMessage def"""
        if state:
            msg = 'On'
        else:
            msg = 'Off'
        # Try to send a different type of message
        # This one may fail since it is not in our list
        # of defaultNotifications
        self.growl.notify(
            noteType = "Key Modifier",
            title = modifier+" has been turned "+msg,
            description = modifier+" has been turned "+msg,
            icon = "http://example.com/icon.png",
            sticky = False,
            priority = -1,
        )

class LionNotifierMESender(object):
    """Makes use of the standard notifier that comes in Lion+ https://github.com/maranas/pyNotificationCenter"""
    def  __init__(self):    
        """Lion notifier. """
        try:
            from pyNotificationCenter import pyNotificationCenter
            self.notifier = pyNotificationCenter()
            self.sendStartUpMessage()
        except ImportError:
            logging.warning('pyNotificationCenter not installed')
            return
   
    def sendStartUpMessage(self):
        self.notifier.notify("MacroServer Mac started up..", "Will Wade", "...", sound=True)

    def sendMessage(self, modifier, state):
        if state:
            msg = 'On'
        else:
            msg = 'Off'
           
        self.notifier.notify(modifier+" has been turned "+msg, "MacroServerMac", "...", sound=True)
        logging.debug('pyNotifier called')

class NullNotifier(object):
    """A null notifier if no notifications required"""

    def __init__(self):
        """Basic init"""
        return

    def sendStartUpMessage(self):
        """Basic startup"""
        logging.debug('null notifier started up')
        return True

    def sendMessage(self, modifier, state):
        """Basic sendMessage"""
        logging.debug('null modifier notifier called')
        return True

class MEUIState(object):
    """Mind Express keyboard and mouse settings reciever. 
       Simply keeps a track of any settings"""

    def  __init__(self):
        """Sets the settings to false on inital run. NB: This could be confusing.."""
        self.sticky = dict()
        self.sticky['shift'] = False
        self.sticky['control'] = False
        self.sticky['option'] = False
        self.sticky['command'] = False
        self.leftdrag = False
   
    def sticky_toggle(self, stickyKey):
        """Allows a setting to be toggled on or off"""
        if (self.sticky[stickyKey]):
            self.sticky[stickyKey] = False
        else:
            self.sticky[stickyKey] = True
   
    def drag_toggle(self):
        """A bit like stick toggle. Toggles the dragging. """
        if (self.leftdrag):
            self.leftdrag = False
        else:
            self.leftdrag = True

class METCPServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, notifier='None'):
        """Create an instance of the Keyboard state"""
        self.meowi = MEUIState()
        logging.debug('notifier:'+str(notifier))
        if notifier == 'Growl':
            self.notifier = GrowlMESender()
        elif notifier == 'Notifier':
            self.notifier = LionNotifierMESender()
        else:
            self.notifier = NullNotifier()
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)

class METCPHandler(SocketServer.BaseRequestHandler):
           
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        logging.debug(self.data)
        r = MExpressHandler(self.data, self.server.meowi, self.server.notifier)
        if (r.isMex):
            r.doCommand()
        else:
            logging.warning('Not MindExpress')
        # if need to send anything back..
        #self.request.sendall(self.data.upper())

def callback():
    master.destroy()
    sys.exit()

def startserver(host, port, tcphandler, notifier):
    server = METCPServer((host, port), tcphandler, True, notifier)
    server.serve_forever()


if __name__ == '__main__':
    args = docopt(__doc__, version='MindExpressMacroServer vb1')
    hosts = list()
       
    if isinstance(args['--host'], str):
        hosts.append(args['--host'])
    else:
        hosts = args['--host']
   
    # Check logging level 
    numeric_level = getattr(logging, args['--loglevel'].upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    FORMAT = '%(asctime)s  %(levelname)s %(message)s'
    logging.basicConfig(filename=args['--logfile'], level=numeric_level, format=FORMAT)
    
    # set up win    
    #master = Tk()    
    #b = Button(master, text="Kill MacroServer", command=callback)
    #b.pack()
    #set up server
    HOST, PORT = hosts[0], int(args['--port'])
    startserver(HOST, PORT, METCPHandler, args['--notifier'])
    #master.mainloop()
    
