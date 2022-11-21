from re import X
import socket
import struct
import datetime
import sys


class server_putah():
    welcomePort = 21 # Default port num for welcoming
    currentUDP = 53 # Used as default value for UDP comms and gets incremented as new Clients connect
    state = "" # Used for tracking state of server. Might just remove this since it's making my head spin
    myIP = "" # To be taken from User input on creation
    myWelcomeSocket = None # Should be established on 
    num_UDP_Connections = 0
    clientHolder = {}

    def __init__(self,IPin, TCPportIn):
        state = "FREE"
        print("Server being constructed")
        myIp = IPin
        welcomePort = TCPportIn
        myWelcomeSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        myWelcomeSocket.bind((myIp,welcomePort)) #TCP socket bound to IP address and Port
        print("Server now listening at TCP port: " + self.welcomePort)
        # sending and listening loop
        while 1:
            # everything in this loop will multithread
            state = "Listening"
            self.accept()
        # if we sent and receive FIN, log and end
        # destructor

    #TODO create timeout system + Handle received messages after decode
    def accept(self):
        incoming_message,incoming_address = self.myWelcomeSocket.recvfrom(60)  
        time_Received = datetime.datetime.now()
        time_Received_To_String = time_Received.strftime("%H:%M:%S")[-3]
        print("Message received at port: " + self.welcomePort + "at Time: " + time_Received_To_String)
        decodedMessage =  incoming_message.decode()
        print(decodedMessage)
        self.state = "Receiving and Handling"
        messageHandlerServer(decodedMessage,)
        # Handle message here
        return

    def messageHandlerServer(self,message, DestPort, DestIP, mySocketOut):
        #Need to implement a better parsing method for message
        if message == "SYN":
            # Check availability of ports (relevant in later parts)
            # return SYNCACK to sender and connect them to new port
            syncHandler(message, DestIP, DestPort, mySocketOut)
        elif message == "ACK":
            #UDP Comms established here
            client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            client.bind(self.currentUDP)
            self.clientHolder.update{self.currentUDP:client}
            self.currentUDP +=1
            self.num_UDP_Connections +=1
            print("New UDP Connection Established")
        elif message == "FIN":
            #Need to add a method to parse client 
            #Close Socket used for cnxn
            print("Closing connection on request from Client")
        else:
            print("Looks like message format was not correct or something unexpected")
            print("Message: " + message)
            print("Destination Port: " + DestPort + "Destination IP: " + DestIP)
            print("Attempted to use the following port: " + mySocketOut)

    # Generic function for sending message, Takes string message, converts to Bytes. Requires Dest IP, Dest Port and Local Port to transmit through
    # Added port generic to allow call in other handling functions.
    # would we be adding the ACKs here or in another function?
    # I think I'd like to create handler that has 3 sub functions. One for sending SyncAck, 
        # One for Sending new Port info, One for Fin
    def sendAMessage(self, message, destIp,destPort,mySocketOut):
        mySocketOut.sendto(bytes(message,"utf-8"),(destIp,destPort))
        timeSent = datetime.datetime.now()
        timeToStr = timeSent.strftime("%H:%M:%S")[-3]
        print("Message: " + message + " transmitting")
        log_Interactions(self.welcomePort, destPort, msg_type, len(message))
        print("Packet transmitted to: " + DestinationIP + "At time: " + timeToStr)
                
    
    def syncHandler(DestIP,DestPort,mySocketOut):
        #This might be a good spot to create a new port to handle UDP comms as opposed to Welcoming port.
        sendAMessage("SYNC/ACK",DestIP,DestPort,mySocketOut)

# Used in transmission of packets. Creates a generic TCP header. 
# TODO Trying to figure out if there is a way to omit fields
#We don't actually need this anymore since we're not sending TCP packets. Comment out imo in case we want reference
    
# def make_a_TCPheader(sourcePortIn, DestPortIn, SequenceNum, AckNum, flagsIn):
#     print("Generating TCP Header...")
#     header = struct.pack(">H",sourcePortIn)
#     header += struct.pack(">H",DestPortIn)
#     header += struct.pack(">H",SequenceNum)
#     header += struct.pack(">H",AckNum)
#     #Offset? Something technical example online was 5<<4
#     header += struct.pack(">H", flagsIn)
#     #recieveWindow determines how many messages before ACK must be Sent
#     #TODO looking up how to calc checksum which should go here.
#     header += struct.pack(">H", 0) #Urgent Data PTR, not used in Project but needed for Packet Format
#     #TODO look up exact structure for TCP 
#     print("Packet Created")
#     print(header + "Is the header being sent")
#     return header


def send_A_Message(client,SourcePortIn,DestPortIn,DestinationIP,message):
    outGoingPacket = make_a_TCPheader(SourcePortIn ,DestPortIn, client.get_Sequence_Num(), client.getAckNum(), client.flags_Needed())
    outGoingPacket += struct.pack(">H",message)  # Message is usually at the Tail end of TCP packets
    #Client and server will have a socket that will be used for transmission of and receipt of packets.
    print("Attempting to send this packet: " + outGoingPacket)
    client.Socket.sendto(outGoingPacket,(DestinationIP, DestPortIn))
    timeSent = datetime.datetime.now()
    timeToStr = timeSent.strftime("%H:%M:%S")[-3]
    
    # do message type if statements here
    if client.getAckNum():
        msg_type = "SYN/ACK" # (SYN/ACK, DATA, FIN)
    elif client.getAckNum():
        msg_type = "DATA"
    elif client.getAckNum():
        msg_type = "FIN"
    
    log_Interactions(SourcePortIn, DestPortIn, msg_type, len(message))
    print("Packet transmitted to: " + DestinationIP + "At time: " + timeToStr)
    

# Client to be replaced once put into a class with 'this'
def receive_A_Message(client, DestPort):
    reply = client.receive(DestPort)
    time_Received = datetime.datetime.now()
    time_Received_To_String = time_Received.strftime("%H:%M:%S")[-3]
    print("Message received at port: " + DestPort + "at Time: " + time_Received_To_String)
    return [DestPort,reply]


# creating a sender socket
def create_Socket(DestHost, DestPort):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender_socket:
        # send message to receiver at address (DestHost, DestPort)
        message = "Pong"
        sender_socket.sendto(message, (DestHost, DestPort))
        print("Success! Receiver IP: ", sys.argv[2], " ---------- Receiver Port Num: ", sys.argv[4], "\n")

def log_Interactions(SourcePort, DestPort, MsgType, MsgLen):
    # Format: "Source | Destination | Message_Type | Message_Length"
        # Source/Destination are port nums, Message_Type = (SYN, SYN/ACK, ACK, DATA, FIN)
        # for server here, we're only using (SYN/ACK, DATA, FIN)
    with open("log_putah_server.txt", "a") as text_file:
        print(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, "\n")
        text_file.write(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, "\n")

    
# argv[1] = --_ip        
# argv[2] = XXXX.XXXX.XXXX.XXXX is IP we're listening for
# argv[3] = --port
# argv[4] = YYYY is port num for client
if __name__ == '__main__':
    # create a server log file at the start HERE
    with open('log_putah_server.txt', 'w') as f:
        print("AAAAAAAAA")
    server_putah()