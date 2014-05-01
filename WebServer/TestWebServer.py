'''
Code for testing the correctness of an implementation of the Web Server.
All functions are tested one after another Code returns an error if a request
is not processed as expected.
'''

__author__ = "Maximilian Pautzke, Andreas Blenk"
__version__ = "1.0"

import unittest
import logging
import sys

# import modules to be tested
from WebServer import *
# from WebServer_ML import *
from socket import *  # @UnusedWildImport

# Setup the logging configuration here? No ... go before main()
logger = logging.getLogger('Test2_Webserver_ML')
logger.setLevel(logging.CRITICAL)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.CRITICAL)

# create formatter
formatterString = '[%(asctime)s'
formatterString += ' - '
formatterString += '%(name)s'
formatterString += ' - '
formatterString += '%(levelname)s'
formatterString += ' - '
formatterString += 'Method: %(funcName)s] \n'
formatterString += '%(message)s'
# formatter = logging.Formatter('[%(asctime)s - %(name)s -
# %(levelname)s - Method: %(funcName)s] \n    %(message)s')
formatter = logging.Formatter(formatterString)

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

blankLine = "\r\n"
statusLine = "HTTP/1.1 404 Not Found"
statusLine += blankLine
headerLines = "Server: NewType"
headerLines += blankLine
headerLines += "Content-Type: text/html"
headerLines += blankLine
message404 = statusLine + headerLines + blankLine


def parseMessage_ML(message):
    """
    Modified parseMessage function.
    """

    # parse message into an array to make the received message readable and
    # print the request
    messageArray = message.split('\n')
    for text in messageArray:
        logger.debug("Print messageArray: %s", text)

    # if request is not correct, return the 404 response
    returnMessage = bytes(message404, encoding="utf-8")

    return returnMessage


def compare(m1, m2, self):
    """
    This function makes sure that the server name in a http response can be
    chosen randomly, all other parts have to be equal
    change here if requests differ in other parts
    """

    m1_array = m1.split(blankLine)
    m2_array = m2.split(blankLine)

    # test if relevant parts are equal:
    # compare statusLine
    message = "Something is wrong with your statusline!"
    self.assertEqual(m1_array[0], m2_array[0], message)

    # compare headerLines (ContentType)
    message = "Something is wrong with your headerline!"
    self.assertEqual(m1_array[2], m2_array[2], message)

    # compare headerLines (blank)
    message = "Something is wrong with your headerline!"
    self.assertEqual(m1_array[4], m2_array[4], message)


class Test(unittest.TestCase):
    def test_version(self):
        self.assertTrue(sys.version > '3',
                        'You are using the wrong python version!')

    def test_readAndReturnTXT(self):
        """
        Test LKN.txt
        """
        rawBytes = readAndReturnTXT()
        self.assertTrue("love" in rawBytes)

    def test_readAndReturnJPG(self):
        """
        Test LKN.jpg
        """
        rawBytes = readAndReturnJPG()
        jpgBytes = '\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00/\x00/\x00'
        self.assertTrue('JFIF' in str(rawBytes))
        self.assertFalse(jpgBytes in str(rawBytes))

    def test_response404_NotFound(self):
        # receive message from webserver
        bytes_from_webserver = response404_NotFound()
        str_from_webserver = bytes.decode(bytes_from_webserver,
                                          encoding='utf_8',
                                          errors='strict')

        httpTestString = "HTTP/1.1 404 Not Found"
        entityBodyTestString = \
            "<html><head></head><body><h1>404 Not Found</h1>"
        entityBodeTestString2 = "<body><h1>404 Not Found"
        entityBodyTestString3 = "Found</h1></body></html>"
        serverTestString = "Server:"
        contentTypeTestString = "Content-Type: text/html"

        message = "There is no \"HTTP\/1\.1 404 Not Found in your header!"
        self.assertTrue(httpTestString in str_from_webserver, message)

        message = "Your body seems to be wrong!"
        self.assertTrue(entityBodyTestString in str_from_webserver, message)

        message = "Your body seems to be wrong!"
        self.assertTrue(entityBodeTestString2 in str_from_webserver, message)

        message = "Your body seems to be wrong!"
        self.assertTrue(entityBodyTestString3 in str_from_webserver, message)

        message = "Server is missing!"
        self.assertTrue(serverTestString in str_from_webserver, message)
        self.assertTrue(contentTypeTestString in str_from_webserver)

    def test_response200_OK(self):
        # receive response from webserver
        response_from_webserver = response200_OK()

        # now create correct response
        statusLine = "HTTP/1.1 200 OK"
        statusLine += blankLine
        response = statusLine

        # test whether header contains HTTP
        message = "There is no \"HTTP\" in your response header!"
        self.assertTrue("HTTP" in response_from_webserver, message)

        # test whether header contains 200
        message = "There is no \"200 OK\" in your response header!"
        self.assertTrue("200 OK" in response_from_webserver)

        # test whether equal
        message = \
            "Message is not correct! Anything is missing ... or too much?"
        self.assertEqual(response, response_from_webserver, message)

    def test_parseMessage_Wrong(self):
        # set of possible requests to test the functionality of parseMessage
        messages = []

        # incorrect request (wrong prefix)
        messages.append("GET /LKW.jpg HTTP/1.1\r\nHost: localhost:8080\r\n")

        # incorrect request (wrong suffix)
        messages.append("GET /LKN.yay HTTP/1.1\r\nHost: localhost:8080\r\n")

        for message in messages:
            # receive message from webserver
            message_from_webserver = parseMessage(message)
            stringMessageFromWebServer = str(message_from_webserver)
            splitArMsgFroWebSer = stringMessageFromWebServer.split()

            # show parts of the splitted message. only for debugging
            for part in splitArMsgFroWebSer:
                logger.debug(part)

            strMessageFromWebserverToTest = \
                bytes.decode(message_from_webserver)

            # now create correct message
            returnMessage = parseMessage_ML(message)
            incorrectStrMessage = bytes.decode(returnMessage)

            # test if equal:
            compare(incorrectStrMessage, strMessageFromWebserverToTest, self)

    def test_parseMessage_Correct(self):
        # correct LKN.jpg request
        message = "GET /LKN.jpg HTTP/1.1\r\nHost: localhost:8080\r\n"

        testMessageBytesWebserver = parseMessage(message)
        correctMessageBytesWebserver = parseMessage_ML(message)

        self.assertFalse(bytes("404", encoding="utf-8") in 
                         testMessageBytesWebserver)
        self.assertNotEqual(testMessageBytesWebserver,
                            correctMessageBytesWebserver)

        logger.info('JFIF' in str(testMessageBytesWebserver))
        debug_message = \
            "Did you really load a JPG? There is something missing."

        self.assertTrue('JFIF' in str(testMessageBytesWebserver),
                        debug_message)

        # Correct LKN.txt request
        message = "GET /LKN.txt HTTP/1.1\r\nHost: localhost:8080\r\n"

        testMessageBytesWebserver = parseMessage(message)
        incorrectMessageBytesWebserver = parseMessage_ML(message)

        debug_message = "Return should not be 404"
        self.assertFalse(bytes("404", encoding="utf-8") in
                         testMessageBytesWebserver,
                         debug_message)
        self.assertNotEqual(testMessageBytesWebserver,
                            incorrectMessageBytesWebserver)

        # Search for jpg bytes in received data
        jpgBytes = '\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00/\x00/\x00'
        self.assertFalse('JFIF' in str(testMessageBytesWebserver))
        self.assertFalse(jpgBytes in str(testMessageBytesWebserver))


if __name__ == "__main__":
    """
    Start testing here.
    """
    logger.debug("WebServer.py is tested...")
    unittest.main(verbosity=2)
