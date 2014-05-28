"""
    Allows you to test the MacroServer
    NB: Easy to break! Not much error checking
    
    # To turn this into a binary
    python pyinstaller.py -F -w Client.py
    (w for windowless version)
    
    <command="window_control"\><subcommandid="dock"\><value="100"\><direction="0"\><gotocorner="0"\>
    -cmd window_control -scmd subcommandid:dock|value:100|direction:0|gotocorner:0
    python Client.py --host 10.211.55.8 -cmd mouse -scmd "subcommandid:change_location|value:100|direction:0|click:0" -sbj ''
"""

import socket
import argparse
import logging

def dataform(args):
    data = '{'+args.pluginid+'}'
    if (args.subject != ''): 
        data += '<subject="'+args.subject+'"\>'
    data += '<command="'+args.command+'"\>'
    for subcmd in args.subcommand.split('|'):
        data += '<'+str(subcmd.split(':')[0])+'="'+subcmd.split(':')[1]+'"\>'
    data += '<X_MEUser"@'+args.xmeuser+'@"\>'
    data += '<X_MELng"'+str(args.xmelang)+'"\>'
    data += '<X_STAVersion"'+args.xstaver+'"\>'
    return data

parser = argparse.ArgumentParser(prog='MindExpressTestClient',description='Pretends to be a MindExpress client')
# Basics
parser.add_argument('--host','-ho', type=str, default='localhost', help='Connect to what server? Default: localhost')
parser.add_argument('--port','-p', type=int, default=12000, help='Change the default Mind Express Port number. Default: 12000')
parser.add_argument('--debug','-db', action='store_true', help='Debug the server, and recieve the debug notes')      
parser.add_argument('--data', type=argparse.FileType('r'), help='Read data from a file')
parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get version number')
# All the components of a Server request
parser.add_argument('--pluginid','-pid', type=str, default='e7ca10ca-4f8d-47ed-8902178849c7a1d5', help='The Plugin-ID of the server')
parser.add_argument('--subject','-sbj', type=str, default='execute_and_get_modifiers', help='Send what subject')
parser.add_argument('--command','-cmd', type=str, default='send_key', help='Send what command')
parser.add_argument('--subcommand','-scmd', type=str, default='normalkey:h|modifier:0', help='Send what sub-command. Note: Needed subelements provided in a key:value pair')
# All the MeX info
parser.add_argument('--xmeuser','-xu', type=str, default='user1', help='MindExpress User')
parser.add_argument('--xmelang','-xl', type=int, default='9', help='Language int')
parser.add_argument('--xstaver','-xs', type=str, default='1.1.1.1354', help='Version ID of this client')
# delay the running?
parser.add_argument('--delay','-d', action='store_true', default=False, help='Delay the running of this script?')
args = parser.parse_args() 

# Main
data = dataform(args)
# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if args.delay:
    import time
    time.sleep(5)
try:
    # Connect to server and send data
    sock.connect((args.host, args.port))
    # the following is from the suggested docs of how it works - but then just sending these bytes below seems to work. No idea..
    header = chr(0)+chr(len(data))
    sock.sendall(header+data)
    #sock.sendall(data)
finally:
    sock.close()


 