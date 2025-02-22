from socket import *
import sys
import time

if len(sys.argv) != 2:
        raise Exception("2 arguments required: file name and server port number.")
try:
        serverPort = int(sys.argv[1]) #our chosen port
except ValueError:
        print("Port number needs to be an integer")
        sys.exit()
except:
        print("Something went wrong.")
        sys.exit()

serverSocket = socket(AF_INET, SOCK_STREAM)
try:
        serverSocket.bind(("", serverPort)) # this is for initial client connections
except:
        print("Something went wrong. Did you choose a valid port?")
        sys.exit()
serverSocket.listen(1) # waiting for handshake
print("Server listening for connections...")
connectionSocket, addr = serverSocket.accept()#connection socket for this specific client
probecount=0
while True:
        ##send a ping back to client that message recieved,
        message = connectionSocket.recv(1024).decode()
        print("message: "+message)
        messagesplit = message.split("\n")
        args = messagesplit[0].split(" ")
        if args[0]=="s":
                try:
                        mType = args[1]
                        msgSize = int(args[2])
                        probes = int(args[3])
                        serverDelay = int(args[4])
                        print("200 OK: Ready\n")
                except:
                        print("404 ERROR: Invalid Connection Setup Message\n")
                        connectionSocket.close()
                        break
        elif args[0]=="m":
                try:
                        probenum = int(args[2])
                        probecount = probecount+1
                        if probenum != probecount:
                                raise Exception
                        print("probe number "+str(probenum)+" recieved!\n")
                        time.sleep(serverDelay)
                        connectionSocket.send(message.encode())
                
                except Exception as err:
                        print("404 ERROR: Invalid Measurement Message:"+err+"\n")
                        connectionSocket.close()
                        serverSocket.close()
                        break
        elif args[0]=="t":
                if message == "t\n":
                        print("200 OK: Closing Connection\n")
                else:
                        print("404 ERROR: Invalid Connection Termination Message\n")
                break
        else:
                print("404 ERROR: Invalid Message\n")
                break
connectionSocket.close() #closing connection between this specific client
serverSocket.close() #closing initial client socket
