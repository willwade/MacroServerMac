"""
    Simply runs and allows multiple commands to the server
    
"""

import subprocess

input = ''
while input != 'END':
    input = raw_input('Enter command: ')
    if (input !='END'):
        subprocess.Popen("python /Users/willwade/bin/MacroSeverMac/MacroClient/Client.py "+input, shell=True)