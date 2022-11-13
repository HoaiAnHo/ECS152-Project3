#fix me t.t
from re import X
import socket
import struct
import datetime
import sys

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


def send_A_Message(client,SourcePortIn,DestPortIn,DestinationIP,message):
    outGoingPacket = make_a_TCPheader(SourcePortIn ,DestPortIn, client.get_Sequence_Num(), client.getAckNum(), client.flags_Needed())
    outGoingPacket += struct.pack(">H",message)  # Message is usually at the Tail end of TCP packets
    #Client and server will have a socket that will be used for transmission of and receipt of packets.
    print("Attempting to send this packet: " + outGoingPacket)
    client.Socket.sendto(outGoingPacket,(DestinationIP, DestPortIn))
    timeSent = datetime.datetime.now()
    timeToStr = timeSent.strftime("%H:%M:%S")[-3]
    # do message type if statements here
    msg_type = "SYN/ACK" # (SYN/ACK, DATA, FIN)
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
        for message_id in range(1, 11):
            message = f"Ping #{message_id}".encode()
            sender_socket.sendto(message, (DestHost, DestPort))
        connect_Succeed()


def connect_Succeed():
    # print and log the IP address and port number of new connection sockets created
    print("Success! Receiver IP: ", sys.argv[2], " ---------- Receiver Port Num: ", sys.argv[4], "\n")


def log_Interactions(SourcePort, DestPort, MsgType, MsgLen):
    # Format: "Source | Destination | Message_Type | Message_Length"
        # Source/Destination are port nums, Message_Type = (SYN, SYN/ACK, ACK, DATA, FIN)
        # for server here, we're only using (SYN/ACK, DATA, FIN)
    with open("log_putah_server.txt", "a") as text_file:
        print(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, "\n")
        text_file.write(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, "\n")

    
# argv[1] = --server_ip        
# argv[2] = XXXX.XXXX.XXXX.XXXX is IP we're listening for
# argv[3] = --port
# argv[4] = YYYY is port num for receiver
if __name__ == '__main__':
    # create a server log file at the start HERE
    print("AAAAAAAAA")
    # Initiate 3-way handshake
