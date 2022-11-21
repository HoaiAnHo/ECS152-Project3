from re import X
import socket
import struct
import datetime
import sys
import random
import time

class receiver_solano():
    welcomePort = 21 # Default port num for welcoming
    state = ""
    myIP = ""
    myWelcomeSocket = None
    myUDPSocket = None
    num_UDP_Connections = 0
    
    def __init__(self):
        while 1:
            self.receive()
        
    def receive():
        loss_value = random.randint(0, 100)
        jitter_value = random.random()
        if loss_value <= sys.argv[6]:
            # drop packet
            return
        if jitter_value > sys.argv[8]:
            time.sleep(jitter_value)
            
def log_Interactions(SourcePort, DestPort, MsgType, MsgLen):
    # for client here, we're only using (SYN, ACK, DATA, FIN)
    with open("log_putah_client.txt", "a") as text_file:
        print(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, "\n")
        text_file.write(SourcePort, " | ", DestPort, " | ", MsgType, " | ", MsgLen, "\n")


# argv[1] == --ip
# argv[2] == XXXX.XXXX.XXXX.XXXX
# argv[3] == --port
# argv[4] == YYYY
# argv[5] == --packet_loss_percentage
# argv[6] == X
# argv[7] == --round_trip_jitter
# argv[8] == Y
# argv[9] == --output
# argv[10] == output.txt
if __name__ == '__main__':
    with open(sys.argv[10], 'w') as f:
        print("open")
    receiver_solano()