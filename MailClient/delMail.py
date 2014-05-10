'''
Erstellt am 29.04.2014

@author: Stefan Röhrl
@MatrikNr: 03623862
@lrz: ga68bow
'''     

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
    # New TCP Socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Connect Socket to HOST and PORT
    clientSocket.connect((host, int(port)))
    ans = clientSocket.recv(1024)
    return clientSocket


def send_user(clientSocket):
    ''' Send USER command and print server response.'''
    # Build Command
    command = "user %s\r\n" % user
    clientSocket.send(command.encode())
    # Send Command-String
    ans = clientSocket.recv(1024).decode()
    #print(ans)
    if("ERR" in ans):
        print("User not known.")


def send_pass(clientSocket):
    ''' Send PASS command and print server response.'''
    # Build Command
    command = "pass %s\r\n" % password
    # Send Command-String
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024).decode()
    #print(ans)
    if("ERR" in ans):
        print("Password falsch")


def send_list(clientSocket):
    '''Send LIST command and get server response.'''
    # Build Command
    command = "LIST\r\n"
    # Send Command-String
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024)
    return ans.decode().split()


def delete_all_mails(clientSocket, list):
    '''delete all emails'''
    
    delMails = 0
    for mailNr in list:
        # Build Command
        command = "DELE %s\r\n" % mailNr
        # Send Command-String
        clientSocket.send(command.encode())
        ans = clientSocket.recv(1024)
        if ("OK" in ans.decode()):
            delMails += 1
    return delMails


def delete_specific_mail(clientSocket, mailNr):
    # Build Command
    command = "DELE %s\r\n" % mailNr
    # Send Command-String
    clientSocket.send(command.encode())
    ans = clientSocket.recv(1024)
    if ("OK" in ans.decode()):
        return True
    else:
        return False


def close_connection(clientSocket):
    '''Send QUIT command and get server response.'''
    # Send Command-String
    clientSocket.send("QUIT\r\n".encode())
    ans = clientSocket.recv(1024)
    clientSocket.close()


def main():
    

    if(parse_arguments()):
        # Connection
        clientSocket = connect()
        # Authentication
        send_user(clientSocket)
        send_pass(clientSocket)

        # Delete specific Mail with mailNr
        delMails = delete_specific_mail(clientSocket, mailNr)
        if delMails:
            print("Mail Nr %s delted!" % mailNr)
        else:
            print("Mail could not be deleted!")
    else:
        # Connection
        clientSocket = connect()
        # Authentication
        send_user(clientSocket)
        send_pass(clientSocket)

        # Delete all Mails
        list = send_list(clientSocket)
        list = list[3:len(list)-1:2]
        #print(range(1,len(list)))
        delMails = delete_all_mails(clientSocket,range(1,len(list)+1))
        print("%d Mails delted!" % delMails)

    close_connection(clientSocket)

if __name__ == "__main__":
    main()
