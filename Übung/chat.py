import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("129.187.223.142", 51234))
while True:
	user = str(input("LKN Chat: "))
	username = "Hans21"
	s.sendall((username + ": " + user).encode("UTF-8"))

	
