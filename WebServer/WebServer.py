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
    ret = ""

    if request[0] == "GET":
        # Requested Content
        reqCont = request[1][1:]

        # Check if there is a File Requested
        if reqCont.rfind(".") > -1:

            # Extract File Ending
            reqEnd = reqCont[reqCont.rfind("."):]
            print ("Recquested Content: ", reqCont)
            # Check if it is a valid Ending
            if (reqEnd == ".jpg") or (reqEnd == ".txt"):

                # Check picure of text
                if reqCont == "LKN.txt":
                    # Send LKN.txt
                    content = readAndReturnTXT()
                    ret = response200_OK()
                    ret += get_header(len(content), "txt")
                    ret += content

                elif reqCont == "LKN.jpg":
                    # Send LKN.jpg
                    content = readAndReturnJPG()
                    ret = response200_OK().encode() + get_header(len(content),"img").encode() + content
                    #ret += get_header(len(content))
                    #ret += content

                else:
                    # Send 404_NotFound
                    ret = response404_NotFound()

            else:
                # Send 404_NotFound
                ret = response404_NotFound()

        else:
            # Send 400_Bad
            ret = response400_BAD()

    else:
        # Send 400_Bad
        ret = response400_BAD()

    return ret


def response404_NotFound():
    """
    Send a 404 Not Found message if the requested file does not exist on the
    server.
    """
    body = get_body("404 Not Found")
    msg = "HTTP/1.1 404 Not Found\r\n"
    msg += get_header(len(body),"")
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
    msg += get_header(len(body),"")
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

def get_header(lenght,cont):
    """
    Returns the HTTP Header
    """
    if cont == "img":
        contType = "image/jpeg"
    elif cont == "txt":
        contType = "text/plain"
    else:
        contType = "text/html"

    head = ""
    head += "Date: %s \r\n" % get_date() 
    head += "Content-Type: %s\r\n" % contType
    head += "Server: PythonServer 0.1\r\n"
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
        receivedMessage = conn.recv(1024).decode()
        print("\r\nRES: ",  receivedMessage, "\r\n")

        if not receivedMessage: break

        returnMessage = parseMessage(receivedMessage)
        print("\r\nRET: ", returnMessage)

        if type(b'byte') == type(returnMessage):
            conn.send(returnMessage)
        else:
            conn.send(returnMessage.encode())

    conn.close()

# only if webserver is top class, call the main function. This is important for unittesting
if __name__ == "__main__":
    print("Webserver is main process.")
    main()