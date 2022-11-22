import socket
import struct
import datetime
import sys
from concurrent.futures import ThreadPoolExecutor

class receiver_berryessa():
    myIp = ""
    myWelcomePort = 21 # Default Welcome port
    myCommsPort = 53 # Default port for communicating with client. Must increment per client to avoid same channel use
    myRoundTripJitter = 0 # Default value for Jitter to test without it
    myPacketLossPercent = 0 # Default value for PacketLoss Percentage to test without loss initially
    myBandwidthDelayProduct = 100 # Max value in Bytes that can be sent via network in an instance
    myBufferSize = 1024 # Creating a default bufferSize, Can be edited later
    outPutFilePath = "" # Path for outputfile
    myWelcomeSocket = None #To be instantiated on creation
    maxThreadCount = 6 # Create an artificial thread count to limit too many concurrent processes
    clientTracker = {} #Dictionary stores client Ip and ports
    numClients = 0
    cWind = 1
    def __init__(self, ip, port, packetLossPercent, roundTripJitter, bdp, outputFileName):
        self.myIp = ip
        self.myWelcomePort = port
        self.myPacketLossPercent = packetLossPercent
        self.myRoundTripJitter = roundTripJitter
        self.myBandwidthDelayProduct = bdp
        self.outPutFilePath = outputFileName
        self.myWelcomeSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.myWelcomeSocket.bind(self.myIp,self.myWelcomePort) #Setup welcome port to Establish comms
        while True:
            self.accept()
    
    #Creates threads for incoming clients not in client Tracker and prints info to track Communications
    def accept(self):
        self.myWelcomeSocket.listen()
        incomingSocket,incomingAddress = self.myWelcomeSocket.accept()
        if incomingAddress not in self.clientTracker and self.numClients<self.maxThreadCount:
            self.clientTracker.update({incomingAddress:incomingSocket})
            clientTracker +=1
            self.multiThread(incomingSocket,incomingAddress)
        time_Received = datetime.datetime.now()
        time_Received_To_String = time_Received.strftime("%H:%M:%S")[-3]
        print("Client received at port: " + self.welcomePort + "at Time: " + time_Received_To_String)
        incomingMessage = socket.recv(self.myBufferSize)
        decodedMessage = incomingMessage.decode()
        print("Decoded Message: " + decodedMessage)
        log_Interactions(self.myWelcomePort, sys.argv[4], "ACK", len(decodedMessage), "STATE", self.cWind)
        return

    def multiThread(self, clientSocket,clientIp):
        with ThreadPoolExecutor(max_workers = self.maxThreadCount) as threadManager:
            while True:
                threadManager.submit(self.interactWithClients,clientSocket,clientIp, self.numClients)

    #Implement Failure % for sending
    def interactWithClients(self,clientSocket,ClientIp):
        clientCommSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        clientCommSocket.bind(self.myCommsPort)
        clientCommsPort = self.myCommsPort        
        self.myCommsPort +=1
        messageCount = 1
        messageOut =""
        clientOut = (ClientIp,clientSocket)
        while 1: #Loop until FIN
            if messageCount == 1 or messageCount %1000 == 1: #TODO find the amount to reSync and implement a condition here
                messageOut="SYN/ACK"
                # Message header details
                messageOut+=str(self.myIp) #Server IP
                messageOut+="|"
                messageOut+=str(clientCommsPort) #Server Port
                messageOut+="|"
                messageOut+=str(messageCount)
                messageOut+="|"
                messageOut+=str(len(messageOut)) #Length of message
                clientCommSocket.sendto(messageOut.encode(),clientOut)
                messageCount +=1
                log_Interactions(clientCommSocket,clientSocket,ClientIp,messageOut,len("SYN/ACK"),len(messageOut))
            #Responses In
            messageIn = clientCommSocket.recv(self.myBufferSize)
            messageCount +=1
            dataExtract = messageIn.split("|")[0]
            messageCount+=1
            #Fin Handling
            if dataExtract == "FIN":
                clientCommSocket.close()
                self.clientTracker.pop(ClientIp)
                self.numClients-=1 
                log_Interactions(clientCommSocket,clientSocket,ClientIp,messageIn,3,len(messageIn))
                print("Client has disconnected")
                break
            #Responding to received packets
            messageOut=dataExtract
            messageOut+=str(self.myIp) #Server IP
            messageOut+="|"
            messageOut+=str(clientCommsPort) #Server Port
            messageOut+="|"
            messageOut+=str(messageCount)
            messageOut+="|"
            messageOut+=str(len(messageOut)) #Length of message
            clientCommSocket.sendto(messageOut.encode(),clientOut)
            messageCount +=1
            log_Interactions(clientCommSocket,clientSocket,ClientIp, messageOut,len(dataExtract),len(messageOut))           
            

def log_Interactions(SourcePort, DestPort, MsgType, MsgLen, State, CWIND):
    with open("log_berryessa_sender.txt", "a") as text_file:
        print(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, " | ", State, " | ", CWIND, "\n")
        text_file.write(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, " | ", State, " | ", CWIND, "\n")
    
if __name__ == '__main__':
    receiver_berryessa()