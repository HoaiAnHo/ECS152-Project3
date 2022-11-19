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
        start = time.time()
        for message in self.packets:
            try:
                print("send")
            except:
                print("oops send again")
                # DevRTT = (1 - B) * DevRTT + B*abs(SampleRTT - EstimatedRTT)
                # EstimatedRTT = (1 - a) * EstimatedRTT + a*SampleRTT
                # Timeout Interval = EstimatedRTT + 4*DevRTT
        end = time.time()
        print("Time taken to transfer file: ", end - start, "\n")
        print("Total bandwidth achieved: \n")
        print("Packet loss observed: ")
            
        
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