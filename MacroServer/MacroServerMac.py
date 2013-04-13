#!/usr/bin/env python
# Run on mac with 
#    python server.py &
# Date: April 2013
# -*- coding: iso-8859-15 -*-

# For debug
import logging
# For the server
import SocketServer
# For the line command aspects
import argparse
# for the MExpressCall
from MExpressHandler import MExpressHandler
# GNTP notifier
try:
    import gntp.notifier # Standard
except ImportError:
    logging.warning('gntp not installed')
    
#https://github.com/kfdm/gntp    
class GrowlMESender(object):
    
    def  __init__(self):
        self.growl = gntp.notifier.GrowlNotifier(
            applicationName = "MacroServer",
            notifications = ["Key Modifier","Debug"],
            defaultNotifications = ["Key Modifier"],
            # hostname = "computer.example.com", # Defaults to localhost
            # password = "abc123" # Defaults to a blank password
        )
        self.growl.register()

    def sendMessage(self,modifier,state):
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

class NullNotifier(object):
    def __init__(self):
        return 
    
    def sendMessage(self,modifier, state):
        logging.debug('null modifier notifier called')
        return True

class MEUIState(object):
    def  __init__(self):
        self.sticky = dict()
        self.sticky['shift'] = False
        self.sticky['control'] = False
        self.sticky['option'] = False
        self.sticky['command'] = False
        self.leftdrag = False
    
    def sticky_toggle(self,stickyKey):
        if (self.sticky[stickyKey]):
            self.sticky[stickyKey] = False
        else:
            self.sticky[stickyKey] = True

class METCPServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, usegrowl=True):
        #create instance of KeyBoard State 
        self.meowi = MEUIState()
        logging.debug('usegrowl:'+str(usegrowl))
        if usegrowl:
            self.notifier = GrowlMESender()
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='MindExpressMacroServer',description='Runs a Mind Express Control Server.')
    parser.add_argument('--host', nargs='+', default='0.0.0.0', help='Allow from one or several ip-address. Default: Any')
    parser.add_argument('--port', type=int, default=12000, help='Change the default Mind Express Port number. Default: 12000')
    parser.add_argument('--loglevel', dest='loglevel', default='info', help='Set the logging level. Default: info (debug, warning, info)')      
    parser.add_argument('--logfile', dest='logfile', default='MacroServerMac.log', help='Where should the logging file be located. Default: .MacroServerMac.log')      
    parser.add_argument('--usegrowl', type=bool, default=False, help='Do you want to use Growl to get notified when a modifier key pressed?')      
    parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get version number')
    args = parser.parse_args() 
    hosts = list()
        
    if isinstance(args.host,str):
        hosts.append(args.host)
    else:
        hosts = args.host
    
    # Check logging level
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    FORMAT = '%(asctime)s  %(levelname)s %(message)s'
    logging.basicConfig(filename=args.logfile,level=numeric_level, format=FORMAT)
    
    #set up server    
    HOST, PORT = hosts[0], args.port
    server = METCPServer((HOST, PORT), METCPHandler, args.usegrowl)
    server.serve_forever()