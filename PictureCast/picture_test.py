#!/usr/bin/python3.3

import os
import sys

# <- Block io ..
#saved_stdout, saved_stderr = sys.stdout, sys.stderr
#sys.stdout = sys.stderr = open(os.devnull, "w")

import aufgsettings
import aufghelper
import picture_cast
import picture_cast_todo
import picture_receiver

#sys.stdout, sys.stderr = saved_stdout, saved_stderr
# -> unblock

from io import StringIO
import unittest
from unittest.mock import MagicMock
import struct
import numpy as np
import random
import traceback


def ERR(msg):
    """ Prints an error message to stderr.
    """

    sys.stderr.write(msg + "\n\r")


def wrp(imgWidth, imgHeight, imgNrOfClrCmp, imgColorCompSize):
    """ Creates an imageProperties dictonary out of image information variables.
    """
    
    dic = {'imgWidth': imgWidth,
           'imgHeight': imgHeight,
           'imgNrOfClrCmp': imgNrOfClrCmp,
           'imgColorCompSize': imgColorCompSize}

    return dic


def test_getNrOfPxlPerPkt():
    """ Tests the getNrOfPxlPerPkt(..) function of the sender.

    """
    
    tests = [
            [picture_cast.getNrOfPxlPerPkt(500, wrp(0, 0, 4, 4)), 31],
            [picture_cast.getNrOfPxlPerPkt(1000, wrp(0, 0, 4, 4)), 62],
            [picture_cast.getNrOfPxlPerPkt(1000, wrp(40, 40, 4, 4)), 62],
            [picture_cast.getNrOfPxlPerPkt(1000, wrp(3, 100, 4, 4)), 62],
            [picture_cast.getNrOfPxlPerPkt(0, wrp(0, 0, 4, 4)), 0]
    ]

    for i in range(0, len(tests)):

        if (tests[i][0] != tests[i][1]):

            ERR("getNrOfPxlPerPkt return value not correct!")

            return -1

    return 0


def test_getReqPktCnt():
    """ Tests the getReqPktCnt(..) function of the sender.
    """
    
    tests = [
            [picture_cast.getReqPktCnt(1000, wrp(100, 100, 4, 4)), 162],
            [picture_cast.getReqPktCnt(500, wrp(100, 100, 4, 4)), 323],
            [picture_cast.getReqPktCnt(1000, wrp(50, 50, 4, 4)), 41]
    ]

    for i in range(0, len(tests)):

        if (tests[i][0] != tests[i][1]):

            ERR("getReqPktCnt return value not correct!")

            return -1

    return 0


def test_genPayloadPlusOnRcvPkt():
    """ Tests the genPayload(..) and the OnRcvPkt(..) of the sender and receiver, respectively.
    """

    (pixelData, imageProperties) = aufghelper.loadImage(aufgsettings.IMG, 1)

    pxlPerPkt = picture_cast.getNrOfPxlPerPkt(
        aufgsettings.MAX_PAYLOAD_SIZE, imageProperties)
    reqPktCnt = picture_cast.getReqPktCnt(
        aufgsettings.MAX_PAYLOAD_SIZE, imageProperties)

    rcvdPixelData = np.ndarray(shape=(imageProperties['imgHeight'], 
                                      imageProperties['imgWidth'], 
                                      imageProperties['imgNrOfClrCmp']), dtype=float)

    senderProperties = {'pxlPerPkt': pxlPerPkt,
                        'reqPktCnt': reqPktCnt,
                        'maxPktSize': aufgsettings.MAX_PAYLOAD_SIZE}

    pktStats = {'lostPkts': 0,
                'duplPkts': 0,
                'reorderedPkts': 0,
                'pktCntRcvd': 0}


    for pkt in range(0, reqPktCnt):

        payload = picture_cast.genPayload(pixelData, pxlPerPkt, reqPktCnt, pkt)

        if (len(payload) > aufgsettings.MAX_PAYLOAD_SIZE):
            
            ERR("Payload size is too large! %s > %s!" % (len(payload), aufgsettings.MAX_PAYLOAD_SIZE))  
            
            return -1

        if (len(payload) == 0):
            
            ERR("Returned packet payload is empty! !")  
            
            return -1
 
        picture_receiver.onRcvPkt(imageProperties, senderProperties, pktStats, rcvdPixelData, payload)

    if ((rcvdPixelData != pixelData).any()):

        ERR("ERROR: rcvdPixelData does not match pixelData!")
        ERR("Pakets sent: " + str(reqPktCnt))

        return -1

    return 0


def test_sendPkt():
    """ Checks if the modified sleep function works right. 
    """

    # mocking socket
    mocked_socket = MagicMock()
    mocked_socket.sendto = MagicMock(return_value=0)

    # mocking sleep
    picture_cast_todo.sleep = MagicMock(return_value=0)

    # run function
    picture_cast_todo.sendPkt(mocked_socket, 0, 0, 10)

    # check if mocked functions were called

    try:
        picture_cast_todo.sleep.assert_called_once_with(10 / 1000)
    except:
        
        print("The delay in sendPkt is not correct!")
        print(sys.exc_info())
      
        return -1

    return 0


reorder_buf = []
reorderedPkts = 0


def test_helper_pkt_flush(imageProperties, senderProperties, pktStats, rcvdPixelData):
    """ Helper function for test_genPayloadExPlusOnRcvPktEx(..).
    """
    
    global reorder_buf

    for i in range(0, len(reorder_buf)):

        picture_receiver.onRcvPktEx(imageProperties, senderProperties, pktStats, rcvdPixelData, reorder_buf[i])

    reorder_buf = []


last_list = []


def test_helper_pkt_out(imageProperties, senderProperties, pktStats, rcvdPixelData, pkt):
    """ Helper function for test_genPayloadExPlusOnRcvPktEx(..).
    """

    global reorder_buf
    global reorderedPkts
    global last_list

    reorderFreq = 0.05

    reorder_buf.append(pkt)

    if (len(reorder_buf) == 2):

        if (random.random() <= reorderFreq):

            reorder_buf[0], reorder_buf[1] = reorder_buf[1], reorder_buf[0]

            if ((reorder_buf[0] != reorder_buf[1]) and (not (reorder_buf[1] in last_list))):

                reorderedPkts += 1

        last_list = reorder_buf
        test_helper_pkt_flush(imageProperties, senderProperties, pktStats, rcvdPixelData)


def test_genPayloadExPlusOnRcvPktEx():
    """ Tests the genPayloadEx(..) and the OnRcvPktEx(..) of the sender and receiver, respectively.
    """
    
    (pixelData, imageProperties) = aufghelper.loadImage(aufgsettings.IMG, 1)

    pxlPerPkt = picture_cast.getNrOfPxlPerPkt(
        aufgsettings.MAX_PAYLOAD_SIZE, imageProperties)
    reqPktCnt = picture_cast.getReqPktCnt(
        aufgsettings.MAX_PAYLOAD_SIZE, imageProperties)

    rcvdPixelData = np.ndarray(shape=(imageProperties['imgHeight'], 
                                      imageProperties['imgWidth'], 
                                      imageProperties['imgNrOfClrCmp']), dtype=float)

    senderProperties = {'pxlPerPkt': pxlPerPkt,
                        'reqPktCnt': reqPktCnt,
                        'maxPktSize': aufgsettings.MAX_PAYLOAD_SIZE}

    pktStats = {'lostPkts': 0,
                'duplPkts': 0,
                'reorderedPkts': 0,
                'pktCntRcvd': 0}

    random.seed()

    global reorderedPkts
    lossFreq = 0.07
    dblFreq = 0.05
    lostPkts = 0
    dblPkts = 0


    for seqNr in range(0, reqPktCnt):

        if (random.random() <= lossFreq):

            lostPkts += 1
            continue

        payload = picture_cast.genPayloadEx(
            pixelData, pxlPerPkt, reqPktCnt, seqNr)

        if (len(payload) > (aufgsettings.MAX_PAYLOAD_SIZE + 4)):
            
            ERR("Payload size is too large! %s > %s!" % (len(payload), aufgsettings.MAX_PAYLOAD_SIZE))  
            
            return -1

        if (len(payload) < 6):
            
            ERR("Returned packet payload is too small to be correct! (len: %s)" % len(payload))  
            
            return -1

        if (payload[0:4] != struct.pack('>I', seqNr)):

            ERR("ERROR: The first 4 bytes of the packet do not contain the sequence number! (or not in the agreed format)")

            return -1

        test_helper_pkt_out(imageProperties, senderProperties, pktStats, rcvdPixelData, payload)

        if (random.random() <= dblFreq):

            test_helper_pkt_out(imageProperties, senderProperties, pktStats, rcvdPixelData, payload)

            dblPkts += 1

    test_helper_pkt_flush(imageProperties, senderProperties, pktStats, rcvdPixelData)

    picture_receiver.onEndMsg(imageProperties, senderProperties, pktStats)

    pktCntRcvd = (reqPktCnt - lostPkts)

    if (pktStats['pktCntRcvd'] != pktCntRcvd):

        ERR("ERROR: Packet count (i.e. pktStats['pktCntRcvd']) is wrong! It is: " +
            str(pktStats['pktCntRcvd']) + ", it should be: " + str(pktCntRcvd))

        if (pktStats['pktCntRcvd'] > pktCntRcvd):
            ERR("HINT: Duplicated packets must not be counted for pktStats['pktCntRcvd'].")

        return -1

    if (pktStats['lostPkts'] != lostPkts):

        ERR("ERROR: Lost packet count (i.e. pktStats['lostPkts']) is wrong! It is: " +
            str(pktStats['lostPkts']) + ", it should be: " + str(lostPkts))

        return -1

    if (pktStats['duplPkts'] != dblPkts):

        ERR("ERROR: Duplicate packet count (i.e. pktStats['duplPkts']) is wrong! It is: " +
            str(pktStats['duplPkts']) + ", it should be: " + str(dblPkts))

        return -1

    if (pktStats['reorderedPkts'] != reorderedPkts):

        ERR("ERROR: Re-ordered packet count (i.e. pktStats['reorderedPkts']) is wrong! It is: " +
            str(pktStats['reorderedPkts']) + ", it should be: " + str(reorderedPkts))

        return -1

    return 0

#
# Main
#

lst_aufg1 = [
    ["getNrOfPxlPerPkt", test_getNrOfPxlPerPkt],
    ["getReqPktCnt", test_getReqPktCnt],
    ["genPayload + OnRcvPkt", test_genPayloadPlusOnRcvPkt]
]

lst_aufg2 = [
    ["sendPkt", test_sendPkt]
]

lst_aufg3 = [
    ["genPayloadEx + onRcvPktEx", test_genPayloadExPlusOnRcvPktEx],
]

lst = [
    ["Aufgabe 1", lst_aufg1],
    ["Aufgabe 2", lst_aufg2],
    ["Aufgabe 3", lst_aufg3]
]

def main():

    if not sys.version_info[0] == 3:
      
        print("ERR: You are running the wrong python version!")
        print("ERR: Required 3.X, you are running %d.%d" % (sys.version_info[0], sys.version_info[1]))
        sys.exit(1)

    if not sys.version_info[:2] == (3, 3):
      
        print("WARN: You are not running python version 3.3!")
        print("WARN: Your version: %d.%d" % (sys.version_info[0], sys.version_info[1]))

    print("==========================")
    print(" UDPPictureCast Unit Test ")
    print("==========================")
    print("")

    for a in range(0, len(lst)):

        print("## " + lst[a][0] + " ##")
        print("")

        lst_aufg = lst[a][1]

        for i in range(0, len(lst_aufg)):

            print(lst_aufg[i][0], end="")

            # Prevent std output..
            saved_stdout, saved_stderr = sys.stdout, sys.stderr

            sys.stdout = buf_stdout = StringIO()
            sys.stderr = buf_stderr = StringIO()

            # Call test function
            try:
                res = lst_aufg[i][1]()
            except:

                sys.stdout, sys.stderr = saved_stdout, saved_stderr

                print(buf_stderr.getvalue())
                print(buf_stdout.getvalue())
                ERR("++==++==++ !! EXCEPTION !! ++==++==++")
                print("Exception Message: " + str(sys.exc_info()[1]))
                print("")       
                traceback.print_exc()
                ERR("++== QUITTING .. ==++")
                sys.exit(1)

            # .. activate output it again
            sys.stdout, sys.stderr = saved_stdout, saved_stderr

            if res != 0:
                print(": ERROR")
                print("")
                print(buf_stderr.getvalue())
                print(buf_stdout.getvalue())
                print("")
                print("+++ Error Message: -->")
                print(buf_stderr.getvalue())
                print("--> END +++")
                sys.exit(1)
            else:
                print(": OKAY")

        print ("")

    print ("EVERYTHING OKAY. ALL TESTS PASSED.")
    print ("")

    sys.exit(0)

#
#------------------------
#

if __name__ == "__main__":
    main()