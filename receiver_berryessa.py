import socket
import struct
import datetime
import sys

class receiver_berryessa():
    myIp = ""
    myWelcomePort = 21 # Default Welcome port
    myCommsPort = 53 # Default port for communicating with client. Must increment per client to avoid same channel use
    myRoundTripJitter = 0 # Default value for Jitter to test without it
    myPacketLossPercent = 0 # Default value for PacketLoss Percentage to test without loss initially
    myBandwidthDelayProduct = 100 #Max value in Bytes that can be sent via network in an instance
    myBufferSize = 1024 #Creating a default bufferSize, Can be edited later
    outPutFilePath = ""
    myWelcomeSocket = None
    clientTracker = {}
    numClients = 0
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
    
    def accept(self):
        self.myWelcomeSocket.listen()
        incomingSocket,incomingAddress = self.myWelcomeSocket.accept()
        self.clientTracker.update({incomingAddress:incomingSocket})
        clientTracker +=1
        time_Received = datetime.datetime.now()
        time_Received_To_String = time_Received.strftime("%H:%M:%S")[-3]
        print("Client received at port: " + self.welcomePort + "at Time: " + time_Received_To_String)
        incomingMessage = socket.recv(self.myBufferSize)
        decodedMessage = incomingMessage.decode()
        print("Decoded Message: " + decodedMessage)
        return