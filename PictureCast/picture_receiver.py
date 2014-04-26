#!/usr/bin/python3.3
#
# Vorlesung Interkommunikation
# UDP Programmieraufgabe
#
# Receiver Application
#
#


# ================
# Library Imports
# ================

# Load required libraries
import socket
import sys
import struct
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import threading
from time import sleep
from collections import defaultdict

# Load common sender/receiver settings & helper
import aufgsettings
import aufghelper
import picture_cast

from picture_receiver_todo import *

# =============
# Load Settings
# =============
bindAddr = aufgsettings.RCV_BIND_ADDR
bindPort = aufgsettings.RCV_PORT
maxPktSize = aufgsettings.MAX_PAYLOAD_SIZE

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket
sock.bind((bindAddr, bindPort))


# Helper Variables
(sentPixelData, imageProperties) = aufghelper.loadImage(aufgsettings.IMG)

pxlPerPkt = picture_cast.getNrOfPxlPerPkt(
    aufgsettings.MAX_PAYLOAD_SIZE, imageProperties)
reqPktCnt = picture_cast.getReqPktCnt(
    aufgsettings.MAX_PAYLOAD_SIZE, imageProperties)

senderProperties = {'pxlPerPkt': pxlPerPkt,
                    'reqPktCnt': reqPktCnt,
                    'maxPktSize': maxPktSize}

# Packet statistics variables to update for Aufgabe 3
pktStats = {'lostPkts': 0,
            'duplPkts': 0,
            'reorderedPkts': 0,
            'pktCntRcvd': 0}

rcvdPixelData = np.ndarray(
    shape=(imageProperties['imgHeight'], imageProperties['imgWidth'], imageProperties['imgNrOfClrCmp']), dtype=float)

threadOpts = {'running': True}

class CompPlot:

    def __init__(self, sentPixelData):

        self.pauseTime = 0.0001

        plt.ion()

        self.f, (self.pic1, self.pic2) = plt.subplots(1, 2)

        self.f.canvas.set_window_title("VL_IK: UDP Programmieraufgabe - Receiver")
        self.f.suptitle("Comparison of source image to received image data")

        self.pic1.imshow(sentPixelData)

        plt.draw()
        plt.pause(self.pauseTime)

    def update(self, rcvdPixelData):

        self.pic2.imshow(rcvdPixelData)
        plt.draw()
        plt.pause(self.pauseTime)


#
# -----------------------------
# Main
# -----------------------------
#

def main_rcv():
  
    # Helper Variables
    global imageProperties
    global senderProperties

    # Variables to update
    global pktStats
    global rcvdPixelData
    global threadOpts
    
    sock.settimeout(0.5)
    
    print("Listening for incoming packets..")
    
    while True:

        try:
            
            data, addr = sock.recvfrom(senderProperties['maxPktSize'])
        
        except:
            
            if threadOpts["running"]:
                continue
            else:
                break
        
        if (data[0:3] == b'END'):
            break

        if (AUFGABE == 1):
            
            onRcvPkt(imageProperties, senderProperties, 
                     pktStats, rcvdPixelData, data)
        else:

            onRcvPktEx(imageProperties, senderProperties, 
                       pktStats, rcvdPixelData, data)

    onEndMsg(imageProperties, senderProperties, pktStats)

    threadOpts['running'] = False

    lostRatio = 0

    if (pktStats['lostPkts'] != 0):
        lostRatio = round((pktStats['lostPkts'] / senderProperties['reqPktCnt']) * 100, 1)

    print("Transmission END")
    print("Aufgabe 3: Lost packets: " + str(pktStats['lostPkts']) + "/" + str(senderProperties['reqPktCnt']) + " (" 
           + str(lostRatio) + "%)" + ", duplicated: " + str(pktStats['duplPkts']) 
           + ", re-ordered packets: " + str(pktStats['reorderedPkts']))


def main():

    if not sys.version_info[0] == 3:
      
        print("ERR: You are running the wrong python version!")
        print("ERR: Required 3.X, you are running %d.%d" % (sys.version_info[0], sys.version_info[1]))
        sys.exit(1)

    if not sys.version_info[:2] == (3, 3):
      
        print("WARN: You are not running python version 3.3!")
        print("WARN: Your version: %d.%d" % (sys.version_info[0], sys.version_info[1]))

    global sentPixelData
    global rcvdPixelData
    global threadOpts

    # Start new thread for the receive function
    t = threading.Thread(target=main_rcv)
    t.start()
  
    compPlt = CompPlot(sentPixelData)
  
    while threadOpts['running']:
      
        sleep(GUI_UPDATE_SLEEP)
        
        if plt.get_fignums():
        
            compPlt.update(rcvdPixelData)
            
        else:
  
            break     

    threadOpts['running'] = False

    t.join()
    
    sleep(2)
    
#
#------------------------
#

if __name__ == "__main__":
    main()
