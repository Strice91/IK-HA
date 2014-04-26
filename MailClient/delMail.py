#!/usr/bin/python3.3
import sys

from socket import *

host = ""
port = 0
user = ""
password = ""
mailNr = -1


def parse_arguments():
    argv = sys.argv
    global host
    host = argv[1]
    global port
    port = int(argv[2])
    global user
    user = argv[3]
    global password
    password = argv[4]

    if len(sys.argv) > 5:
        global mailNr
        mailNr = argv[5]
        return True
    return False


def connect():
    # ToDo write some code <-----------
    pass


def send_user(clientSocket):
    ''' Send USER command and print server response.'''
    # ToDo write some code <-----------
    pass


def send_pass(clientSocket):
    ''' Send PASS command and print server response.'''
   # ToDo write some code <-----------
    pass


def send_list(clientSocket):
    '''Send LIST command and get server response.'''
   # ToDo write some code <-----------
    pass


def delete_all_mails(clientSocket, list):
    '''delete all emails'''
    # ToDo write some code <-----------
    pass


def delete_specific_mail(clientSocket, mailNr):
   # ToDo write some code <-----------
    pass


def close_connection(clientSocket):
    '''Send QUIT command and get server response.'''
    # ToDo write some code <-----------
    pass


def main():
    if(parse_arguments()):
        # ToDo write some code <-----------
        pass
    else:
        # ToDo write some code <-----------
        pass

if __name__ == "__main__":
    main()
