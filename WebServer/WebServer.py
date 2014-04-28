'''
Erstellt am ...

@author: GRUPPE
'''     

import socket
host = "0.0.0.0"
port = 8080
         
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
    # Create a Socket
    connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind Socket to Port
    connectionSocket.bind((host, port))
    connectionSocket.listen(2)
    # Accept Connections
    conn,addr = connectionSocket.accept()

    while 1:
        # Wait for a Request
        receivedMessage = connectionSocket.recv(1024)
        print(receivedMessage)
        # Parse Request
        returnMessage = parseMessage(receivedMessage)
        # Send Answer Message
        connectionSocket.send(returnMessage)

main()
