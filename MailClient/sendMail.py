import sys
from socket import *

# Get the server hostname and port as command line arguments
argv = sys.argv                      
host = argv[1]
port = argv[2]
sourceadd = argv[3]
destadd = argv[4]
subjekt = argv[5]
text = argv[6]
timeout = 1 # in second

endmsg = '\r\n.\r\n'

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)

# Port number may change according to the mail server
# clientSocket.connect((mailserver, 25))
clientSocket.connect((host, int(port)))
recv = clientSocket.recv(1024)

if recv[:3] != '220':
	print '220 reply not received from server.'

# Send HELO command and print server response.
heloCommand = 'HELO '+ sourceadd +'\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
#print recv1
if recv1[:3] != '250':
	print '250 reply not received from server.'
	
# Send MAIL FROM command and print server response.
mailfrom = 'MAIL FROM: <'+ sourceadd +'>\r\n'
clientSocket.send(mailfrom)
recv2 = clientSocket.recv(1024)
#print recv2
if recv2[:3] != '250':
	print '250 reply not received from server.'


# Send RCPT TO command and print server response. 
rcptto = 'RCPT TO: <'+destadd+'>\r\n'
clientSocket.send(rcptto)
recv3 = clientSocket.recv(1024)
#print recv3
if recv3[:3] != '250':
	print '250 reply not received from server.'

# Send DATA command and print server response. 
data = 'DATA\r\n'
clientSocket.send(data)
recv4 = clientSocket.recv(1024)
#print recv4
if recv4[:3] != '354':
	print '354 reply not received from server.'

# Send message header.
clientSocket.send('SUBJECT: '+subjekt+'\r\n')
clientSocket.send('From: <'+sourceadd+'>\r\n')
clientSocket.send('To: <'+destadd+'>\r\n')
clientSocket.send('Content-Type: text/plain; charset=ISO-8859-1\r\n')
# Send message data.
clientSocket.send('\r\n')
clientSocket.send(text)

# Message ends with a single period.
clientSocket.send(endmsg)
recv5 = clientSocket.recv(1024)
#print recv5
if recv5[:3] != '250':
	print '250 reply not received from server.'

# Send QUIT command and get server response.
quitcommand = 'QUIT\r\n'
clientSocket.send(quitcommand)
recv6 = clientSocket.recv(1024)
#print recv6
if recv6[:3] != '221':
	print '221 reply not received from server.'
