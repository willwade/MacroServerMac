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

class MEUIState(object):
    def  __init__(self):
        self.sticky = dict()
        self.sticky['set'] = False
        self.sticky['shift'] = False
        self.sticky['control'] = False
        self.sticky['alt'] = False
        self.sticky['cmd'] = False
        self.leftdrag = False
    
    def helloworld(self):
        print 'hello world'

    def sticky_toggle(self,stickyKey):
        if (self.sticky[stickyKey]):
            self.sticky[stickyKey] = False
        else:
            self.sticky[stickyKey] = True

class METCPServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, debug=False):
        self.debug = debug
        #create instance of KeyBoard State 
        self.meowi = MEUIState()
        #set up logging
        FORMAT = '%(asctime)s  %(levelname)s %(message)s'
        logging.basicConfig(filename='MacroServerMac.log', level=logging.DEBUG, format=FORMAT)
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)

class METCPHandler(SocketServer.BaseRequestHandler):
            
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        if self.server.debug:
            logging.debug(self.data)
        r = MExpressHandler(self.data, self.server.meowi, self.server.debug)
        if (r.isMex):
            r.doCommand()
        else:
            if (self.server.debug):
                logging.warning('Not Mex')
        # if need to send anything back..
        #self.request.sendall(self.data.upper())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='MindExpressMacroServer',description='Runs a Mind Express Control Server.')
    parser.add_argument('--host', nargs='+', default='0.0.0.0', help='Allow from one or several ip-address. Default: Any')
    parser.add_argument('--port', type=int, default=12000, help='Change the default Mind Express Port number. Default: 12000')
    parser.add_argument('--debug', action='store_true', help='Debug the server to a log file')      
    parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get version number')
    args = parser.parse_args() 
    hosts = list()
    
    
    if isinstance(args.host,str):
        hosts.append(args.host)
    else:
        hosts = args.host
    

    HOST, PORT = hosts[0], args.port
    server = METCPServer((HOST, PORT), METCPHandler, debug=args.debug)
    server.serve_forever()