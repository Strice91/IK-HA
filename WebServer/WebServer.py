'''
Erstellt am ...

@author: GRUPPE
'''     

import socket
import time

HOST = "0.0.0.0"
PORT = 8080 
         
def parseMessage(message):
    """
    Parse the received request.
    Check if request is valid.
    Check if file exist.
    Create and return answer with or without file.
    """
    request = message.split()
    ret = []
    ret_str = ""
    print(request[1])
    if request[0] == "GET".encode():
        ret_str += response200_OK()
        ret_str += readAndReturnTXT()
        #ret.append(response200_OK().encode())
        #ret.append(readAndReturnTXT().encode())
    else:
        ret_str = response400_BAD()
    return ret_str


def response404_NotFound():
    """
    Send a 404 Not Found message if the requested file does not exist on the
    server.
    """
    body = get_body("404 Not Found")
    msg = "HTTP/1.1 404 Not Found\r\n"
    msg += get_header(len(body))
    msg += body
    return msg.encode()
    
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
    body = get_body("400 Bad Request")
    msg = "HTTP/1.1 400 Bad Request\r\n"
    msg += get_header(len(body))
    msg += body
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

def get_header(lenght):
    """
    Returns the HTTP Header
    """
    head = ""
    head += "Date: %s \r\n" % get_date() 
    head += "Server: PythonServer 0.1\r\n"
    head += "Content-Type: text/html\r\n"
    head += "Content-Length: %d \r\n" % lenght
    head += "\r\n"

    return head

def get_body(heading):
    body = ""
    body += "<html>"
    body += "<head></head>"
    body += "<body>"
    body += "<h1>%s</h1>" % heading
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

    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print ('could not open socket')
        sys.exit(1)
    conn, addr = s.accept()
    print ('Connected by', addr)
    while 1:
        receivedMessage = conn.recv(1024)
        print("\r\nRES: ",  receivedMessage, "\r\n\r\n")
        if not receivedMessage: break
        returnMessage = parseMessage(receivedMessage)
        print("\r\nRET: ", returnMessage, "\r\n")

        for msg in returnMessage:
            conn.send(msg)

    conn.close()

main()