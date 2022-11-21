#modify part 1 for byte size checks and cumulative ACKS
from re import X
import socket
import struct
import datetime
import sys
import random
import time

class sender_solano():
    welcomePort = 21 # Default port num for welcoming
    state = "" #Used for tracking state of server
    myIP = ""
    myWelcomeSocket = None
    myUDPSocket = None
    num_UDP_Connections = 0
    
    PKT_SIZE = 1000
    packets = []
    
    def __init__(self):
        # return the message
        def create_message(message_id, message):
            return f"#{message_id}: {message}"
        
        # read alice29.txt file
        with open(sys.argv[6], "r") as file:
            message = file.read()
            
        # create packets using create message function
        for i in range(0, len(message), self.PKT_SIZE):
            self.packets.append(create_message(i//self.PKT_SIZE, message[i:i+self.PKT_SIZE]))

        # append the last message with message id -1
        self.packets.append(create_message(-1, ""))
        
        # create a udp socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            # bind the socket to a OS port
            udp_socket.bind(("localhost", 5000))
            total_data = 0
            start = time.time()
            for message in self.packets:
                try:
                    print("send")
                    total_data += len(message)
                except:
                    print("oops send again")
                    # DevRTT = (1 - B) * DevRTT + B*abs(SampleRTT - EstimatedRTT)
                    # EstimatedRTT = (1 - a) * EstimatedRTT + a*SampleRTT
                    # Timeout Interval = EstimatedRTT + 4*DevRTT
            end = time.time()
            total_time = end - start
            print("Time taken to transfer file: ", total_time, "\n")
            print("Total bandwidth achieved: ", total_data / total_time,"\n")
            print("Packet loss observed: ", len(message) - total_data)
            
        
    def send():
        print("send")

# argv[1] == --dest_ip
# argv[2] == XXXX.XXXX.XXXX.XXXX
# argv[3] == --dest_port
# argv[4] == YYYY
# argv[5] == --input
# argv[6] == input.txt
if __name__ == '__main__':
    sender_solano()