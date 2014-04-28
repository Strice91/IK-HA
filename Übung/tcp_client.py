import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("129.187.223.142", 8000))
s.sendall("GET /helloworld.txt HTTP/1.1\r\n\r\n".encode("UTF-8"))
print (s.recv(1024))