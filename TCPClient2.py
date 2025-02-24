import sys
from socket import *
import time

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
except:
        print("Something went wrong. Did you input the right IP address and port number?")
        sys.exit()
#initial message format: protocol phase, m-type, msg size, probes, server delay, newline (whitespace in between all of these)
message = "s "
print("Starting measurement setup!\n")
# m-type input
while True:
        userinput = input("Input 1 for RTT or 2 for throughput: ")
        if int(userinput)==1:
                message+="rtt "
                measurement = "rtt"
                break
        elif int(userinput)==2:
                message+="tput "
                measurement = "tput"
                break
        else:
                print("Try again with a valid input.\n")
#msg size input
while True:
        userinput = input("Please specify the message size (in bytes): ")
        try:
                payload = int(userinput)
                message+=(userinput+" ")
                break
        except:
                print("Input must be in integer format.\n")
#probes
while True:
        userinput = input("Please specify the number of probes the server should expect to recieve: ")
        try:
                numProbes = int(userinput)
                message+=(userinput+" ")
                break
        except:
                print("Input must be in integer format.\n")
#server delay
userinput = input("How long should server wait before echoing message back to client (default is 0): ")
try:
        int(userinput)
        message+=(userinput+"\n")
except:
        message+="0\n"

clientSocket.send(message.encode())

#moving on to measurement phase
allRTT = []
allTPUT = []
for i in range(numProbes):
        message = "m "
        arbitrarychar = "a"
        arbitrarytext = arbitrarychar*payload
        message+=(arbitrarytext+" ")
        message+=(str(i+1)+"\n")
        try:
                startTime = time.time()
                totalBytesSent = 0
                while totalBytesSent < len(message):
                        sent = clientSocket.send(message[totalBytesSent:].encode())
                        if sent == 0:
                                raise RuntimeError("socket connection broken")
                        totalBytesSent+=sent
                echo = clientSocket.recv(100000).decode()
                if len(echo)>20000: 
                        time.sleep(0.1)
                stopTime = time.time()
                if echo!=message:
                        raise Exception
                if measurement == "rtt":
                        rtt = stopTime-startTime
                        print(str(rtt))
                        allRTT.append(rtt)
                elif measurement == "tput":
                        tput = payload / (stopTime-startTime) #is this right???
                        print(str(tput))
                        allTPUT.append(tput)
                else:
                    raise Exception
        except:
                print("Something went wrong.")
                clientSocket.close()

#connection termination phase
print("Measurement Phase Finished!\n")
if measurement == "rtt":
        mean = sum(allRTT)/len(allRTT)
        print("Mean RTT of message with "+str(payload)+" byte payload and "+str(numProbes)+" total probes: "+str(mean))
elif measurement == "tput":
        mean = sum(allTPUT)/len(allTPUT)
        print("Mean TPUT of message with "+str(payload)+" byte payload and "+str(numProbes)+" total probes: "+str(mean))
message = "t\n"
clientSocket.send(message.encode())

clientSocket.close()
