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
import struct
import math

# =============
# Load Settings
# =============


"""
The variable AUFGABE sets which functions to use for
generating the payload and for receiving the pixel data.

AUFGABE == 1:
    Use genPayload + onRcvPkt

AUFGABE > 1
    Use genPayloadEx + onRcvPktEx
    
NOTE: The value has to be the same for the sender and receiver!
    
"""
AUFGABE=1
#AUFGABE=3


"""
The GUI is automatically updated after every GUI_UPDATE_SLEEPth seconds
with information out of the rcvdPixelData array. You can increase the
update frequency (by decreasing the value of GUI_UPDATE_SLEEP) but you
may get a high CPU usage and more lost packets.

"""
GUI_UPDATE_SLEEP=0.5


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
          
   senderProperties:
   -----------------
   Properties of the sent packets:
   
      senderProperties['pxlPerPkt']:
          Number of pixels to send per packet (as returned by getReqPktCnt(..)).
      
      senderProperties['reqPktCnt']:
           Numbers of packets required for the whole image (as returned by getReqPktCnt(..)).
      
      senderProperties['maxPktSize']:
           Maximal number of bytes for the payload per packet. Note that in Aufgabe 3 we
           are violating the set maximum. But it has no negative consequences on the
           transmission, because the resulting number of bytes in the packet is still lower
           than the MTU of most communication channels.
           
   pktStats:
   ---------
   Packet receive statistics:
   
       pktStats['lostPkts']:
           Nr. of lost packets.
       
       pktStats['duplPkts']:
           Nr. of duplicated packets.
       
       pktStats['reorderedPkts']:
           Nr. of reordered packets.
       
       pktStats['pktCntRcvd']:
           Nr. of received packets (EXCLUDING duplicated packets)
      
"""


def onRcvPkt(imageProperties,
             senderProperties,
             pktStats, 
             rcvdPixelData, 
             pkt):
    """Aufgabe 1: Function called when a packet/datagram is received.

    Receives a packet containing only pixel data. The data is put back into
    the rcvdPixelData array based on the count of packets received so far.

    Args:
            imageProperties: (read only)
                See definition in file header.
    
            senderProperties: (read only)
                See definition in file header.
                    
            pktStats:
                See definition in file header. Only the
                field 'pktCntRcvd' is of relevance in this
                function.
                
            rcvdPixelData:
                Array of the size [imgWidth] x [imgHeight] x [imgNrOfClrCmp].
                Put the received pixel data back into this array.
                    
            pkt:
                The received payload of the packet.
                    
    Returns:
            (no return value)
    """

    # <-
    # Put your code for Aufgabe 1 here to update the rcvdPixelData array
    # with the received data.
    #
    # Note:
    #
    # The GUI is automatically updated after every //GUI_UPDATE_SLEEP//th seconds
    # with information out of the rcvdPixelData array. You can increase the
    # update frequency (by decreasing the value of //GUI_UPDATE_SLEEP//) but you
    # may get a high CPU usage and more lost packets.
    # ->

    pktStats['pktCntRcvd'] += 1


def onRcvPktEx(imageProperties,
               senderProperties,
               pktStats,
               rcvdPixelData,
               pkt):
    """Aufgabe 3: Function called when a packet with a sequence number is received.

    Receives a packet containing pixel data and a sequence number. The
    pixel data is put back into the rcvdPixelData array based on the received
    sequence number.

    Args:
            imageProperties: (read only)
                See definition in file header.
    
            senderProperties: (read only)
                See definition in file header.
                    
            pktStats:
                See definition in file header. Update all the fields
                of the statistics accordingly.
                
            rcvdPixelData:
                Array of the size [imgWidth] x [imgHeight] x [imgNrOfClrCmp].
                Put the received pixel data back into this array.
                    
            pkt:
                The received payload of the packet.
                
    Returns:
            (no return value)
    """

    # <-
    # Put your code for Aufgabe 3 here to update the pixelData array
    # with the received data based on the received sequence number.
    #
    # Note:
    #
    # The GUI is automatically updated after every //GUI_UPDATE_SLEEP//th packet
    # with information out of the pixelData array. You can increase the
    # update frequency (by decreasing the value of //GUI_UPDATE_SLEEP//) but you
    # may get a high CPU usage and more lost packets.
    # ->

    pktStats['pktCntRcvd'] += 1


def onEndMsg(imageProperties, senderProperties, pktStats):
    """onEndMsg is called when the END packet is received.
    
    You can use this function to finalize your packet statistics.
    
    Args:
            imageProperties: (read only)
                See definition in file header.
    
            senderProperties: (read only)
                See definition in file header.
                    
            pktStats:
                See definition in file header.
    """
  
    # <-
    # Put your code to finalize the packet statistics here.
    # ->
    pass


if __name__ == "__main__":
    print("")
    print("---- Please execute picture_receiver.py! ----")
    print("")