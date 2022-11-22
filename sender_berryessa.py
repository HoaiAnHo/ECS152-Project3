from re import X
import socket
import struct
import datetime
import sys
import random
import time
import matplotlib.pyplot as plot

class sender_berryessa():
    welcomePort = 21 # Default port num for welcoming
    state = "" #Used for tracking state of server
    myIP = ""
    myWelcomeSocket = None
    myTCPSocket = None
    num_TCP_Connections = 0
    
    # Tahoe/Reno vars
    cWind = 1
    protocol = sys.argv[6]
    boundary = 10000
    bound_hit = 0
    reno_boundary = 10000
    ssthresh = 8000
    s_hit = 0
    
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
        total_data = 0
        start = time.time()
        while 1:
            self.send()
            break
        end = time.time()
        total_time = end - start
        print("Time taken to transfer file: ", end - start, "\n")
        print("Total bandwidth achieved: ", total_data / total_time,"\n")
        print("Packet loss observed: ", len(message) - total_data)
            
        
    def send(self):
        state = "Exponential"
        for message in self.packets:
            try:
                if self.protocol == "tahoe":
                    if bound_hit == 1:
                        self.cWind = 1
                        bound_hit = 0
                        self.ssthresh -= 500
                    else:
                        if self.s_hit == 1:
                            self.cWind += 1000
                            state = "Congestion Avoidance"
                            self.s_hit = 0
                        else:
                            self.cWind = self.cWind*2
                            state = "Slow Start"
                        # if ssthresh is hit, go into congestion avoidance
                        # else, continue as slow start
                        
                elif self.protocol == "reno":
                    if bound_hit == 1:
                        self.cWind = self.reno_boundary / 2
                        bound_hit = 0
                    else:
                        if self.s_hit == 1:
                            self.cWind += 1000
                            bound_hit = 0
                            state = "Congestion Avoidance"
                        else:
                            self.cWind = self.cWind*2
                            state = "Slow Start"
                if self.cWind >= self.boundary:
                    bound_hit = 1
                if self.ssthresh <= self.cWind:
                    self.s_hit = 1
                # NOW SEND THAT MESSAGE AAAAAAAAAAAA
                log_Interactions(self.welcomePort, sys.argv[4], "ACK", len(message), state, self.cWind)
            except:
                print("oops send again")
                # DevRTT = (1 - B) * DevRTT + B*abs(SampleRTT - EstimatedRTT)
                # EstimatedRTT = (1 - a) * EstimatedRTT + a*SampleRTT
                # Timeout Interval = EstimatedRTT + 4*DevRTT
        
def log_Interactions(SourcePort, DestPort, MsgType, MsgLen, State, CWIND):
    with open("log_berryessa_sender.txt", "a") as text_file:
        print(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, " | ", State, " | ", CWIND, "\n")
        text_file.write(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, " | ", State, " | ", CWIND, "\n")


# argv[1] == --dest_ip
# argv[2] == XXXX.XXXX.XXXX.XXXX
# argv[3] == --dest_port
# argv[4] == YYYY
# argv[5] == --tcp_version
# argv[6] == tahoe/reno
# argv[7] == --input
# argv[8] == input.txt
if __name__ == '__main__':
    sender_berryessa()
