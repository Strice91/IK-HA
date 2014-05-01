import sys
from socket import *


def printStart(user):
    print("Mailbox from " + user + "\t--------------------------------------")
    return 0


def printEnd():
    print("--------------------------------------------------------------")
    return 0


def printMailHeader(mailnum, mailfrom, subjekt):
    print(str(mailnum) + "\t" + mailfrom + '\t' + subjekt)
    return 0


def printMail(mailfrom, mailto, subjekt, date, text):
    print("")
    print("E-Mail")
    print("")
    print("From:\t\t" + mailfrom)
    print("To:\t\t" + mailto)
    print("Date:\t\t" + date)
    print("Subjekt:\t" + subjekt)
    print("Message:")
    print(text)
    return 0


def printError():
    print("No e-mail")
    return 0


def connect(host, port):
    """connect to the server
        params:
            host: the server host
            port: the server port (normally 110)
        returns: a socket that is connected to the server
    """
    # New TCP Socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Connect Socket to HOST and PORT
    clientSocket.connect((host, int(port)))
    return clientSocket

def send_user(clientSocket, user):
    """ send the user command """
    command = "user %s\r\n" % user
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024)
    #print(ans)
    if("ERR" in ans):
        print("User not known.")


def send_pass(clientSocket, password):
    """ send the pass command """
    command = "pass %s\r\n" % password
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024) 
    #print(ans)
    if("ERR" in ans):
        print("Password falsch")


def close_connection(clientSocket):
    """ close the connection """
    command = "QUIT\r\n"
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024)
    clientSocket.close()


def send_rset(clientSocket):
    """ send rset command """
    command = "RSET\r\n"
    clientSocket.sendall(command.encode())
    ans = clientSocket.recv(1024)


def send_list(clientSocket):
    """ send list command """
    command = "LIST\r\n"
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024)
    return ans


def retr_mail(clientSocket, emailnum, user):
    """ retrieve mail """
    # Get mailList
    mailList = send_list(clientSocket)
    # Decode Bytes
    mailList = mailList.decode()
    # Split List in Array
    mailList = mailList.split()
    if len(mailList) > 0:
        # Only store Mail Lengths
        mailList = mailList[4:len(mailList)-1:2]
        # Select Mail Length
        mailLenght = mailList[emailnum-1]

    clientSocket.send(("RETR %d\r\n" % emailnum).encode())
    ans = clientSocket.recv(1024)


def retr_header(clientSocket, a, list):
    """ retrieve header """
    for mailNr in list:
        command = "TOP %d\r\n" % mailNr
        clientSocket.send(command.encode())
        ans = clientSocket.recv(1024)

        


def getSpecificMail(argv):
    """ get a specific mail """

    host = argv[1]
    port = int(argv[2])
    user = argv[3]
    password = argv[4]
    emailnum = argv[5]

    clientSocket = connect(host, port)
    send_user(clientSocket, user)
    send_pass(clientSocket, password)

    retr_mail(clientSocket, emailnum, user)

    return 0


def getAllMails(argv):
    """ get all mails """

    host = argv[1]
    port = int(argv[2])
    user = argv[3]
    password = argv[4]

        # ToDo write some code <--

    return 0


def main():
    # decide witch case (Starting point)
    argv = sys.argv
    length = len(argv)
    if(length == 5):
        getAllMails(argv)
    elif(length == 6):
        getSpecificMail(argv)
    else:
        print("For e-mail overview:")
        print("getMail.py host prot user password")
        print("For specific e-mail:")
        print("getMail.py host prot user password e-mail-number")

if __name__ == "__main__":
    main()
