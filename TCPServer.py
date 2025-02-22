from socket import *
import sys

if len(sys.argv) != 2:
        raise Exception("2 arguments required: file name and server port number.")
try:
        serverPort = int(sys.argv[1]) #our chosen port
except ValueError:
        print('Port number needs to be an integer')
        sys.exit()
except:
        print('Something went wrong.')
        sys.exit()

serverSocket = socket(AF_INET, SOCK_STREAM)
try:
        serverSocket.bind(("", serverPort)) # this is for initial client connections
except:
        print('Something went wrong. Did you choose a valid port?')
        sys.exit()
serverSocket.listen(1) # waiting for handshake
print('Server listening for connections...')
while True:
        connectionSocket, addr = serverSocket.accept() #connection socket for this specific client
        sentence = connectionSocket.recv(1024).decode()
        print('Connection made! Client message: ',sentence)
        connectionSocket.close() #closing connection between this specific client
        break
serverSocket.close() #closing initial client socket


