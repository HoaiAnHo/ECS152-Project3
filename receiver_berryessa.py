from re import X
import socket
import struct
import datetime
import sys
import random
import time

class receiver_berryessa():
    welcomePort = 21 # Default port num for welcoming
    state = ""
    myIP = ""
    myWelcomeSocket = None
    myTCPSocket = None
    num_TCP_Connections = 0
    
    def __init__(self):
        print("ohhhh")
        
def log_Interactions(SourcePort, DestPort, MsgType, MsgLen, State, CWIND):
    with open("log_berryessa_receiver.txt", "a") as text_file:
        print(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, " | ", State, " | ", CWIND, "\n")
        text_file.write(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, " | ", State, " | ", CWIND, "\n")


# argv[1] == --ip
# argv[2] == XXXX.XXXX.XXXX.XXXX
# argv[3] == --port
# argv[4] == YYYY
# argv[5] == --packet_loss_percentage
# argv[6] == X
# argv[7] == --round_trip_jitter
# argv[8] == Y
# argv[9] == --bdp
# argv[10] == Z
# argv[11] == --output
# argv[12] == output.txt
if __name__ == '__main__':
    with open(sys.argv[10], 'w') as f:
        print("open")
    receiver_berryessa()