import socket
import sys

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host="127.0.0.1"
port=8080
s.connect((host,port))
s.send("test".encode("UTF-8"))

s.close()