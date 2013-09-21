"""
    Allows you to test the MacroServer
    NB: Easy to break! Not much error checking
    
    # To turn this into a binary
    python pyinstaller.py -F -w Client.py
    (w for windowless version)
"""

import socket
import os, sys

if len(sys.argv)>1:
    host = sys.argv[1]
else:
    host = '192.168.1.113'

if len(sys.argv)>2:
    str = sys.argv[2]
else:
    if os.name=='posix':
        from AppKit import *
        pb = NSPasteboard.generalPasteboard()
        str = pb.stringForType_(NSStringPboardType)
    else:
        import win32clipboard
        # get clipboard data
        win32clipboard.OpenClipboard()
        str = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        
    str = str.replace("'", "\\'")
    
data = '{e7ca10ca-4f8d-47ed-8902178849c7a1d5}<subject="execute_and_get_modifiers"\><command="send_key"\><normalkey="'
data +=str
data +='"\><modifier="0"\><X_MEUser"@user1-4874-305132@"\><X_MELng"9"\><X_STAVersion"1.1.1.1261"\>'

# Main

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 12000))
len_sent = s.send(data)
# Clean up
s.close()