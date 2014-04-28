import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("129.187.223.142", 51234))
while True:
	print (s.recv(1024))


	
