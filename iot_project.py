"""
IOT Project - Networking II
Jacob Christensen
02/05/2020
"""

import socket

discover = "operation: discover\r\n"
capabilities = "operation: capabilities\r\n"

# Send DISCOVER broadcast
mydevice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mydevice.sendto(bytes(discover, 'utf-8'),('192.168.24.255', 4961)


while True:
	data, addr = mydevice.recvfrom(1024)
	data.decode('utf-8')
	data_in = dict(d.split(": ", 1), for d in data.split("\r\n"))
	if(data_in["operation"] == "acknowledge") :
		mydevice.sendto(capabilities ,addr)
