import socket
import sys

HOST, PORT = "localhost", 12000
#data = " ".join(sys.argv[1:])
data = '{e7ca10ca-4f8d-47ed-8902178849c7a1d5}<subject="execute_and_get_modifiers"\><command="send_key"\><normalkey="p"\><modifier="0"\><X_MEUser"@user1-4874-305132@"\><X_MELng"9"\><X_STAVersion"1.1.1.1261"\>'

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)