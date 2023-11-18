import socket
import sys

ip = "10.39.32.1"
port = 5005
print("Create Socket")
# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
print("Socket created")
server_address = (ip, port)
s.bind(server_address)
print("Do Ctrl+c to exit the program !!")
message = b"Hello"
s.sendto(message, server_address)

while True:
    print("####### Server is listening #######")
    data, address = s.recvfrom(5005)
    print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")
    send_data = input("Type some text to send => ")
    s.sendto(send_data.encode('utf-8'), address)
    print("\n\n 1. Server sent : ", send_data,"\n\n")