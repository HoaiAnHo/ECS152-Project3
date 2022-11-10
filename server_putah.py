#TODO FIX ME t.t
from re import X
import socket
import struct
import datetime
import sys

def make_a_TCPheader(sourcePortIn, DestPortIn, SequenceNum, AckNum, flagsIn):
    print("Generating TCP Header...")
    header = struct.pack(
        sourcePortIn,
        DestPortIn,
        SequenceNum,
        AckNum,
        #Offset? Something technical example online was 5<<4
        flagsIn,
        #recieveWindow determines how many messages before ACK must be Sent
        # checkSum, #TODO looking up how to calc
        0 #Urgent Data PTR, not used in Project but needed for Packet Format
        print("Packet Created")
        print(header + "Is what's being sent")
    )
    return header


# Client to be replaced once put into a class with 'this'
def receive_A_Message(client, DestPort):
    reply = client.receive(DestPort)
    print("Message received at port: " + DestPort)
    return [DestPort,reply]

# creating a sender socket
def create_Socket(DestHost, DestPort):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender_socket:
        # send message to receiver at address (DestHost, DestPort)
        for message_id in range(1, 11):
            message = f"Ping #{message_id}".encode()
            sender_socket.sendto(message, (DestHost, DestPort))
            
def connect_Succeed():
    # print and log the IP address and port number of new connection sockets created
    print("Success! Receiver IP: ", sys.argv[2], " ---------- Receiver Port Num: ", sys.argv[4], "\n")
    
def log_Interactions():
    # Format: "Source | Destination | Message_Type | Message_Length"
        # Source/Destination are port nums, Message_Type = (SYN, SYN/ACK, ACK, DATA, FIN)
    print("LOG!!!")
    
# argv[1] = --server_ip        
# argv[2] = XXXX.XXXX.XXXX.XXXX is IP we're listening for
# argv[3] = --port
# argv[4] = YYYY is port num for receiver
if __name__ == '__main__':
    print("AAAAAAAAA")
    # Initiate 3-way handshake
