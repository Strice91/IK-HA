'''
Erstellt am ...

@author: GRUPPE
'''     

import socket
import time
host = "0.0.0.0"
port = 8080
         
def parseMessage(message):
    """
    Parse the received request.
    Check if request is valid.
    Check if file exist.
    Create and return answer with or without file.
    """
    ret = response400_BAD()
    return ret
        
def response404_NotFound():
    """
    Send a 404 Not Found message if the requested file does not exist on the
    server.
    """
    msg = "HTTP/1.1 404 Not Found\r\n"
    msg += get_header()
    msg += body("404 Not Found")
    return msg.encode("utf_8")
    
def response200_OK():
    """
    Send a 200 OK message if the requested file exists on the server.
    """
    msg = "HTTP/1.1 200 OK\r\n"
    return msg

def response400_BAD():
    """
    Send a 400 Bad Request message if Request could not be parsed properly
    """
    msg = "HTTP/1.1 400 Bad Request\r\n"
    msg += get_header()
    msg += body("400 Bad Request")
    return msg.encode("utf_8")

def readAndReturnTXT():
    """
    Read LKN.txt file and return the data
    """
    try:
        f = open("LKN.txt", "r")
        ret = f.read()
        f.close()
    except:
        ret = False
    return ret

def readAndReturnJPG():
    """
    Read LKN.jpg file and return the data
    """
    try:
        f = open("LKN.jpg", "rb")
        ret = f.read()
        f.close()
    except:
        ret = False
    return ret

def get_date():
    """
    Returns the present Date
    """
    date = time.strftime("%a, %d %b %Y %H:%M:%S")

    return date

def get_header():
    """
    Returns the HTTP Header
    """
    head = ""
    head += "\r\n"
    head += "Date: %s \r\n" % get_date() 
    head += "Server: PythonServer 0.1\r\n"
    head += "Content-Type: text/html\r\n"
    head += "\r\n"

    return head

def body(content):
    body = ""
    body += "<html>"
    body += "<head></head>"
    body += "<body>"
    body += "<h1>%s</h1>" % content
    body += "</body>"
    body += "</html>\r\n"

    return body

###############################################################################
###############################################################################
# Start your server application here
# Use the given functions to implement your WebServer
###############################################################################
###############################################################################

def main():
    print("Server is running!")
 
    # Create a Socket
    connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind Socket to Port
    connectionSocket.bind((host, port))
    connectionSocket.listen(1)

    try:
        while True:
            conn, addr = connectionSocket.accept()
            print ("Connection from", addr)

            while True: 
                receivedMessage = conn.recv(1024)
                print (receivedMessage)
                returnMessage = parseMessage(receivedMessage)
                conn.send(returnMessage)
                
    finally:
        connectionSocket.close()

main()