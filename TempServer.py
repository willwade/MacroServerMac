#!/usr/bin/env python
# Run on mac with 
#    python server.py &
# Date: April 2013
# -*- coding: iso-8859-15 -*-

# For the server
from SocketServer import *
from MExpressHandler import MExpressHandler

class DebugTCPServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, debug=True):
        self.debug = debug
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate=True)

class DebugMETCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # self.server is an instance of the DebugTCPServer
        DEBUG = self.server.debug
        self.data = self.request.recv(1024).strip()
        if DEBUG:
            print "{} wrote:".format(self.client_address[0])
        r = MExpressHandler(self.data, False)


server = DebugTCPServer((HOST, PORT), DebugMETCPHandler, debug=True)