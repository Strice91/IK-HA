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

    # ToDo write some code <--


def send_user(clientSocket, user):
    """ send the user command """

    # ToDo write some code <--


def send_pass(clientSocket, password):
    """ send the pass command """

    # ToDo write some code <--


def close_connection(clientSocket):
    """ close the connection """

    # ToDo write some code <--


def send_rset(clientSocket):
    """ send rset command """

    # ToDo write some code <--


def send_list(clientSocket):
    """ send list command """

    # ToDo write some code <--


def retr_mail(clientSocket, emailnum, user):
    """ retrieve mail """

    # ToDo write some code <--


def retr_header(clientSocket, a, list):
    """ retrieve header """

    # ToDo write some code <--


def getSpecificMail(argv):
    """ get a specific mail """

    host = argv[1]
    port = int(argv[2])
    user = argv[3]
    password = argv[4]
    emailnum = argv[5]

        # ToDo write some code <--

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
