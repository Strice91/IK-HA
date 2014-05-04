#!/usr/bin/python3.3

# ================
# Library Imports
# ================

# Load required libraries
import matplotlib.image as mpimg
import math
import socket
import struct
import sys
from time import sleep

# Load common sender/receiver settings & helper functions
import aufgsettings
import aufghelper

# Load the implemented functions
from picture_cast_todo import *


def sendEndMsg(sock, dest):
    """Sends the END message to the receiver to indicate the end of the tranmission.

    Args:
            sock:

            dest:

    Returns:
            (no return value)
    """

    MSG_END = "END"

    sock.sendto(bytes(MSG_END, 'UTF-8'), dest)

#
# -----------------------------
# Main
# -----------------------------
#

def main():

    if not sys.version_info[0] == 3:
      
        print("ERR: You are running the wrong python version!")
        print("ERR: Required 3.X, you are running %d.%d" % (sys.version_info[0], sys.version_info[1]))
        sys.exit(1)

    if not sys.version_info[:2] == (3, 3):
      
        print("WARN: You are not running python version 3.3!")
        print("WARN: Your version: %d.%d" % (sys.version_info[0], sys.version_info[1]))

    global AUFGABE
    global AUFGABE2_DELAY

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Destination of the transmission
    dst = (aufgsettings.RCV_ADDR, aufgsettings.RCV_PORT)

    imageProperties = {}

    # Read image into array
    (pixelData, imageProperties) = aufghelper.loadImage(aufgsettings.IMG)

    # Calculate how many pixels per packet
    pxlPerPkt = getNrOfPxlPerPkt(aufgsettings.MAX_PAYLOAD_SIZE, imageProperties)
    reqPktCnt = getReqPktCnt(aufgsettings.MAX_PAYLOAD_SIZE, imageProperties)

    # Loop through the required packets
    for pkt in range(0, reqPktCnt):

        if (AUFGABE == 1):    
            payload = genPayload(pixelData, pxlPerPkt, reqPktCnt, pkt)
        else:
            payload = genPayloadEx(pixelData, pxlPerPkt, reqPktCnt, pkt)    

        if (AUFGABE2_DELAY <= 0):
            sendPkt(sock, dst, payload)
        else:
            sendPkt(sock, dst, payload, AUFGABE2_DELAY)

    print("Transmission finished!");
    sleep(1)

    sendEndMsg(sock, dst)
    

#
#------------------------
#

if __name__ == "__main__":
    main()
