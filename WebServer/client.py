import socket
import sys

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host="192.168.178.23"
port=8075
s.connect((host,port))
s.send("USER meinName\r\nPASS meinPass\r\n".encode("UTF-8"))
while 1:
	msg = s.recv(1024).decode()
	if msg:
		print(msg)
s.close()