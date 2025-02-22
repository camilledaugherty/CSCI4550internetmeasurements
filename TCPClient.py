import sys
from socket import *

if len(sys.argv) != 3:
        raise Exception("3 arguments required: file name, host name/IP, and port number.")

serverName = sys.argv[1] #server's ip address
try:
        serverPort = int(sys.argv[2])
except ValueError:
        print("Port number needs to be an integer")
        sys.exit()
except:
        print("Something went wrong.")
        sys.exit()

clientSocket = socket(AF_INET, SOCK_STREAM) #open socket
try:
        clientSocket.connect((serverName, serverPort)) # connecting to server based on ip and port number
except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        sys.exit()
clientSocket.send("testing one two three!".encode()) #send data to server
clientSocket.close() #close upon send
