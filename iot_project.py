"""
IOT Project - Networking II
Jacob Christensen
02/05/2020
"""

import socket
import RPi.GPIO as GPIO

discover = "operation: discover\r\n"
capabilities = "operation: capabilities\r\nname: Jacob's Device\r\nresources: 2\r\n[resource 1]\r\ntype: switch\r\n[resource 2]\r\ntype: lamp\r\n"

# Setup GPIO Pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
inputs = [16, 19]
GPIO.setup(inputs, GPIO.IN)
outputs = [4, 6, 12, 13, 20, 21, 26]
GPIO.setup(outputs, GPIO.OUT)
GPIO.output(outputs, GPIO.LOW)

# Send DISCOVER broadcast
mydevice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mydevice.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
mydevice.sendto(bytes(discover, 'utf-8'),('192.168.24.255', 4961))

while True :
	data, addr = mydevice.recvfrom(1024)
	data = data.decode('utf-8')
	print(data)
	# Split the response into a dictionary
	data_split = data.split("\r\n")
	data_split.pop()
	data_in = dict(d.split(": ", 1) for d in data_split)
	if(data_in["operation"] == "acknowledge") :
		print("Sending Capabilities")
		# Respond to ACKNOWLEDGE message with RESPONSE
		mydevice.sendto(bytes(capabilities,'utf-8'), addr)

