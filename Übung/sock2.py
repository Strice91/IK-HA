import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dst = ("10.180.32.41", 7073)
sock.sendto("Super Geil!".encode("UTF-8"), dst)