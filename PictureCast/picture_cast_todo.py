#!/usr/bin/python3.3

# ================
# Library Imports
# ================

# Load required libraries
import matplotlib.image as mpimg
import math
import socket
import struct
from time import sleep

# Load common sender/receiver settings & helper functions
import aufgsettings
import aufghelper

"""
The variable AUFGABE sets which functions to use for
generating the payload and for receiving the pixel data.

AUFGABE == 1:
    Use genPayload + onRcvPkt

AUFGABE > 1
    Use genPayloadEx + onRcvPktEx
   
NOTE: The value has to be the same for the sender and receiver!
"""
AUFGABE = 1
#AUFGABE = 3

"""
The variable AUFGABE_DELAY sets which time value in milliseconds
be given to your sendPkt(..) function as sleepTime parameter.

"""
AUFGABE2_DELAY=5


"""
Explanation of the used data dictonaries:

  imageProperties:
  ----------------
  Properties of the image to receive:
            
      imageProperties['imgWidth']: 
          Width of the image in pixels.
          
      imageProperties['imgHeight']: 
          Height of the image in pixels.
          
      imageProperties['imgNrOfClrCmp']: 
          Nr. of color components of each pixel.
          
      imageProperties['imgColorCompSize']:
          Size in bytes of one color component.
          
"""


def getNrOfPxlPerPkt(udpMaxPayloadSize, imageProperties):
    """Aufgabe 1: Calculate the number of (full) pixels per packet/datagram.

    Full pixel refers to a pixel with all its color components.
    Note that not all parameters may be required for this function.

    Args:
        udpMaxPayloadSize:
            Maximum payload size per packet in bytes.
            
        imageProperties:
            See definition in file header.
                    
    Returns:
            Returns the number of pixels per packet/datagram.
    """

# <-
#
# Put your code for Aufgabe 1 here
#
# ->
    return 0  # <- dummy return


def getReqPktCnt(udpMaxPayloadSize, imageProperties):
    """Aufgabe 1: Calculate the number of packets/datagrams required to send the whole image.

    Note that not all parameters may be required for this function.

    Args:
        udpMaxPayloadSize:
            Maximum payload size per packet in bytes.
            
        imageProperties:
            See definition in file header.

    Returns:
            Returns the number of packets/datagrams required to send the whole picture.
    """

# <-
#
# Put your code for Aufgabe 1 here
#
# ->
    return 0  # <- dummy return


def genPayload(pixelData, pxlPerPkt, reqPktCnt, pktNr):
    """Aufgabe 1: Generate the payload for a packet.

    To solve this exercise, use only the supplied parameters. The generated payload
    is supposed to only contain pixel data, no other pieces of information. The parameters
    pixelData, pxlPerPkt and reqPktCnt stay the same for all calls of this function. The pktNr
    parameter counts from 0 to (reqPktCnt - 1).

    Args:
            pixelData:
                    3-dimensional array with the pixel data.
            pxlPerPkt:
                    Number of pixels to send per packet (as returned by getReqPktCnt(..)).
            reqPktCnt:
                    Numbers of packets required for the whole image (as returned by getReqPktCnt(..)).
            pktNr:
                    Number of the packet to be generated (0 for the first packet)

    Returns:
            A 1-dimensional byte array with the payload data for one packet.
    """

    imgWidth = pixelData.shape[1]
    imgHeight = pixelData.shape[0]
    imgNrOfClrCmp = pixelData.shape[2]

# <-
#
# Put your Aufgabe 1 code here
#
# ->
    return bytes("", "UTF-8") # <- dummy return (delete when implementing your solution)


def genPayloadEx(pixelData, pxlPerPkt, reqPktCnt, seqNr):
    """Aufgabe 3: Generate the payload for a packet with a specific sequence number.

    To solve this exercise, use only the supplied parameters. The generated payload
    is supposed to contain the sequence number and the pixel data, as described in
    the description of the exercise. The parameters pixelData, pxlPerPkt and reqPktCnt
    stay the same for all calls of this function. The seqNr parameter counts from 0
    to (reqPktCnt - 1).

    Args:
            pixelData:
                    3-dimensional array with the pixel data.
            pxlPerPkt:
                    Number of pixels to send per packet (as returned by getReqPktCnt(..)).
            reqPktCnt:
                    Numbers of packets required for the whole image (as returned by getReqPktCnt(..)).
            seqNr:
                    Sequence number of the packet to be generated (0 for the first packet)

    Returns:
            A 1-dimensional byte array with the sequence number and the payload data for
            one packet.
    """

    imgWidth = pixelData.shape[1]
    imgHeight = pixelData.shape[0]
    imgNrOfClrCmp = pixelData.shape[2]

# <-
#
# Put your Aufgabe 3 code here
#
# ->
    return bytes("", "UTF-8") # <- dummy return (delete when implementing your solution)


def sendPkt(sock, dest, payload, sleepTime=0):
    """Sends a packet/datagram to a specific destination.

    Args:
            sock:
                    The UDP socket to use for sending the payload.
            dest:
                    The dest to send the datagram to.
            payload:
                    The payload of the datagram.
            sleepTime:
                    Optional parameter for Aufgabe 2. Time to sleep in
                    milliseconds after sending a packet. Accepts floating point
                    values.
    Returns:
            (no return value)
    """

    sock.sendto(payload, dest)

    if sleepTime > 0:

        # <-
        #
        # Put your code for Aufgabe 2 here
        #
        # ->
        pass


if __name__ == "__main__":
    print("")
    print("---- Please execute picture_cast.py! ----")
    print("")