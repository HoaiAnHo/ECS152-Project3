from re import X
import socket
import struct
import datetime
import sys

class client_putah():
    # default port for comms 
    # client chooses what port num to contact on server
    serverIP = sys.argv[2]
    serverPort = sys.argv[4]
    myIP = "127.0.0.1" # arbitrary
    myPort = 8000 # arbitrary
    mySocket = None
    
    def __init__(self):
        state = "FREE"
        print("Server being constructed")
        mySocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        mySocket.bind(("", 8888))
        
        #send syn
        message = "Ping"
        self.mySocket.sendto(message, (self.serverIP, self.serverPort))
        log_Interactions(self.myPort, self.serverPort, "SYN", 0)
        
        #receive syn/ack
        while(1):
            if mySocket.recvfrom(self.serverPort):
                #send ack
                self.mySocket.sendto(message, (self.serverIP, self.serverPort))
                log_Interactions(self.myPort, self.serverPort, "ACK", 0)
                break
                
        while(1):
            if mySocket.recvfrom(self.serverPort):
                self.send(self.serverIP, self.serverPort)
        # if we sent and receive FIN, log and end
        # if mySocket.recvfrom(TCPport):
        #     log_Interactions(self.myPort, TCPport, "FIN", len(message))
        
    def send(self, IPin, TCPport):
        message = "Ping"
        self.mySocket.sendto(message, (IPin, TCPport))
        log_Interactions(self.myPort, TCPport, "DATA", len(message))
        
    #Respond to TCP message
    def replyTCP(self,DestPort,DestIP):
        message += make_a_TCPheader()

# Used in transmission of packets. Creates a generic TCP header. 
# TODO Trying to figure out if there is a way to omit fields
def make_a_TCPheader(sourcePortIn, DestPortIn, SequenceNum, AckNum, flagsIn):
    print("Generating TCP Header...")
    header = struct.pack(">H",sourcePortIn)
    header += struct.pack(">H",DestPortIn)
    header += struct.pack(">H",SequenceNum)
    header += struct.pack(">H",AckNum)
    #Offset? Something technical example online was 5<<4
    header += struct.pack(">H", flagsIn)
    #recieveWindow determines how many messages before ACK must be Sent
    #TODO looking up how to calc checksum which should go here.
    header += struct.pack(">H", 0) #Urgent Data PTR, not used in Project but needed for Packet Format
    #TODO look up exact structure for TCP 
    print("Packet Created")
    print(header + "Is the header being sent")
    return header

def log_Interactions(SourcePort, DestPort, MsgType, MsgLen):
    # for client here, we're only using (SYN, ACK, DATA, FIN)
    with open("log_putah_client.txt", "a") as text_file:
        print(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, "\n")
        text_file.write(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, "\n")
        
# argv[1] = --server_ip        
# argv[2] = XXXX.XXXX.XXXX.XXXX is our local IP
# argv[3] = --port
# argv[4] = YYYY is port num for the server
if __name__ == '__main__':
    # create a server log file at the start HERE
    with open('log_putah_client.txt', 'w') as f:
        print("AAAAAAAAA")
    # Initiate 3-way handshake
    client_putah()