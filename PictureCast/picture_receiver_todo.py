'''
Erstellt am 02.05.2014

@author: Stefan Röhrl
@MatrikNr: 03623862
@lrz: ga68bow
'''     

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
import numpy as np

# =============
# Load Settings
# =============

ListOfPkt = []

"""
The variable AUFGABE sets which functions to use for
generating the payload and for receiving the pixel data.

AUFGABE == 1:
    Use genPayload + onRcvPkt

AUFGABE > 1
    Use genPayloadEx + onRcvPktEx
    
NOTE: The value has to be the same for the sender and receiver!
    
"""
#AUFGABE=1
AUFGABE=3


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

    # Store Imageparameters
    imgHeight = imageProperties["imgHeight"]
    imgWidth = imageProperties["imgWidth"]
    pxlPerPkt = senderProperties['pxlPerPkt']
    pixelByte = imageProperties['imgNrOfClrCmp'] * imageProperties['imgColorCompSize']
    pktNr = pktStats['pktCntRcvd']

    # Calulating Start Pixel
    startPX = pktNr * pxlPerPkt
    startLine = math.floor(startPX / imgWidth)
    startCol = startPX - (imgWidth * startLine)
 
    # Make temporary line and col
    line = startLine
    col = startCol

    for n in range(0,len(pkt),pixelByte):

        if line > imgHeight-1:
            break

        # Decode each byte
        comp1 = struct.unpack('f', pkt[n:n+4])
        comp2 = struct.unpack('f', pkt[n+4:n+8])
        comp3 = struct.unpack('f', pkt[n+8:n+12])
        comp4 = struct.unpack('f', pkt[n+12:n+16])
        
        # Combine the 4 color components
        rcvdPixelData[line][col] = np.array([comp1[0], comp2[0], comp3[0], comp4[0]], np.float32)

        # If col < maximum Column increase col
        if col < imgWidth-1:
            col += 1
        # Else go to next line and start in colum 0
        else:
            col = 0
            line += 1

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

    # Store Imageparameters
    imgHeight = imageProperties["imgHeight"]
    imgWidth = imageProperties["imgWidth"]
    pxlPerPkt = senderProperties['pxlPerPkt']
    pixelByte = imageProperties['imgNrOfClrCmp'] * imageProperties['imgColorCompSize']

    # Get Sequence Number at the begining
    seqNr = struct.unpack('I',pkt[0:4])[0]
    # If seqNr is not expected -> Packet is reordered 
    if not (seqNr == pktStats['pktCntRcvd']):
        pktStats['reorderedPkts'] += 1
    #print(seqNr)

    # Add recieved Packet to List
    ListOfPkt.append(seqNr)
    
    # Calulating Start Pixel
    startPX = seqNr * pxlPerPkt

    # Determine StartLine and StartColumn
    startLine = math.floor(startPX / imgWidth)
    startCol = startPX - (imgWidth * startLine)

    # Make temporary line and col
    line = startLine
    col = startCol

    # Remove Sequence Number from Packet
    pkt = pkt[4:]

    for n in range(0,len(pkt),pixelByte):

        if line > imgHeight-1:
            break

        # Decode each byte
        comp1 = struct.unpack('f', pkt[n:n+4])
        comp2 = struct.unpack('f', pkt[n+4:n+8])
        comp3 = struct.unpack('f', pkt[n+8:n+12])
        comp4 = struct.unpack('f', pkt[n+12:n+16])
        
        # Combine the 4 color components
        rcvdPixelData[line][col] = np.array([comp1[0], comp2[0], comp3[0], comp4[0]], np.float32)
        
        # If col < maximum Column increase col
        if col < imgWidth-1:
            col += 1

        # Else go to next line and start in colum 0 
        else:
            col = 0
            line += 1
        
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

    # Calculate lost Packets    
    pktStats['lostPkts'] = senderProperties['reqPktCnt'] - pktStats['pktCntRcvd']
    
    # Empty list of Checked Packets
    seenList = []

    # Go through the list of recieved Packets
    for nr in ListOfPkt:
        if not (nr in seenList):
            seenList.append(nr)
        # If Packet Nr is already in list -> duplicate
        else:
            pktStats['duplPkts'] += 1

    pass


if __name__ == "__main__":
    print("")
    print("---- Please execute picture_receiver.py! ----")
    print("")