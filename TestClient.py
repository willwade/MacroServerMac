import socket
import argparse

data = """{e7ca10ca-4f8d-47ed-8902-178849c7a1d5}<command="mouse"\><subcommandid="change_location"\><value="100"\><direction="270"\><click="0"\><X_MEUser"@user1@"\><X_MELng"9"\><X_STAVersion="1.1.1.1261"\>
"""

parser = argparse.ArgumentParser(prog='MindExpressTestClient',description='Pretends to be a MindExpress client')
parser.add_argument('--host', type=str, default='localhost', help='Connect to what server? Default: localhost')
parser.add_argument('--port', type=int, default=12000, help='Change the default Mind Express Port number. Default: 12000')
parser.add_argument('--debug', action='store_true', help='Debug the server.')      
parser.add_argument('--data', type=argparse.FileType('r'), help='Read data from a file')
parser.add_argument('--version', action='version', version='%(prog)s 1.0', help='Get version number')
args = parser.parse_args() 

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.host, args.port))

# Send the data
if (args.data!=None):
    data = args.data.read()

len_sent = s.send(data)

# Receive a response
response = s.recv(len_sent)
print 'Received: "%s"' % response

# Clean up
s.close()