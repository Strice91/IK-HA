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
    ans = clientSocket.recv(1024)
    return clientSocket

def send_user(clientSocket, user):
    """ send the user command """
    # Build Command
    command = "user %s\r\n" % user
    # Send Command-String
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024).decode()
    #print(ans)
    if("ERR" in ans):
        print("User not known.")
        sys.exit()


def send_pass(clientSocket, password):
    """ send the pass command """
    # Build Command
    command = "pass %s\r\n" % password
    # Send Command-String
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024).decode() 
    #print(ans)
    if("ERR" in ans):
        print("Password falsch")
        sys.exit()


def close_connection(clientSocket):
    """ close the connection """
    # Build Command
    command = "QUIT\r\n"
    # Send Command-String
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024)
    clientSocket.close()


def send_rset(clientSocket):
    """ send rset command """
    # Build Command
    command = "RSET\r\n"
    # Send Command-String
    clientSocket.sendall(command.encode())
    ans = clientSocket.recv(1024)


def send_list(clientSocket):
    """ send list command """
    # Build Command
    command = "LIST\r\n"
    # Send Command-String
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024).decode().split()
    return ans


def retr_mail(clientSocket, emailnum, user):
    """ retrieve mail """
    # Request Mail from Server
    clientSocket.send(("RETR %d\r\n" % int(emailnum)).encode())
    ans = clientSocket.recv(1024).decode()

    if not ("ERR" in ans):
        # Get Index of the Header Components
        IND_From = ans.index("From:")
        IND_To = ans.index("To:")
        IND_Subject = ans.index("Subject:")
        IND_Msg = ans.index("\r\n", IND_Subject)

        # Build Header Dict from parsed Answer
        ret = {}
        ret["mailfrom"] = ans[IND_From+6:IND_To-1]
        ret["mailto"] = ans[IND_To+4:IND_Subject-1]
        ret["subjekt"] = ans[IND_Subject+9:IND_Msg]
        ret["date"] = ""
        ret["text"] = ans[IND_Msg+2:len(ans)-3]

        return ret

    else:
        return False

    



def retr_header(clientSocket, a, list):
    """ retrieve header """
    # Store the requested MailNr
    mailNr = list[a]
    command = "TOP %d\r\n" % int(mailNr)
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024).decode().split()

    # Parse Header
    ret = {}
    ret["mailnum"] = int(mailNr)
    ret["mailfrom"] = ans[2] + " " + ans[3]
    SubjIndex = ans.index("Subject:")
    ret["subjekt"] = ' '.join(ans[SubjIndex+1:len(ans)-1])

    return ret





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

    # Get a complete Mail
    mail = retr_mail(clientSocket, emailnum, user)

    printStart(user)
    if mail:
        printMail(mail["mailfrom"], mail["mailto"], mail["subjekt"], mail["date"], mail["text"])
    else:
        printError()
    printEnd()

    return 0


def getAllMails(argv):
    """ get all mails """

    host = argv[1]
    port = int(argv[2])
    user = argv[3]
    password = argv[4]

    clientSocket = connect(host, port)
    send_user(clientSocket, user)
    send_pass(clientSocket, password)

    # Get Mail List
    mailList = send_list(clientSocket)
    # Reduce Mails to Mail Numbers
    mailList = mailList[3:len(mailList)-1:2]
    
    printStart(user)

    if not mailList:
        printError()
    else:
        a = 0
        for mail in mailList:
            # Get Mail Headers
            head = retr_header(clientSocket,a,mailList)
            printMailHeader(head["mailnum"],head["mailfrom"],head["subjekt"])
            a += 1

    printEnd()

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
