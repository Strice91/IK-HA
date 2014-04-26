'''
Erstellt am ...

@author: GRUPPE
'''     
            
def parseMessage(message):
    """
    Parse the received request.
    Check if request is valid.
    Check if file exist.
    Create and return answer with or without file.
    """
    return None
        
def response404_NotFound():
    """
    Send a 404 Not Found message if the requested file does not exist on the
    server.
    """
    return None
    
def response200_OK():
    """
    Send a 200 OK message if the requested file exists on the server.
    """
    return None

def readAndReturnTXT():
    """
    Read LKN.txt file and return the data
    """
    return None

def readAndReturnJPG():
    """
    Read LKN.jpg file and return the data
    """
    return None

###############################################################################
###############################################################################
# Start your server application here
# Use the given functions to implement your WebServer
###############################################################################
###############################################################################

def main():
   while 1:
        returnMessage = parseMessage(receivedMessage)
        connectionSocket.send(returnMessage)
