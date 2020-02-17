"""
IOT Project - Networking II
Jacob Christensen
02/05/2020
"""

import socket
import RPi.GPIO as GPIO
import time

discover = "operation: discover\r\n"
capabilities = "operation: capabilities\r\nname: Jacob's Device\r\nresources: 2\r\n[resource 1]\r\ntype: switch\r\n[resource 2]\r\ntype: lamp\r\n"
acknowledge = "operation: acknowledge\r\n"
status_change_on = "operation: status change\r\ntype: switch 1\r\nstate: ON\r\n"
status_change_off = "operation: status change\r\ntype: switch 1\r\nstate: OFF\r\n"
status = 0
discovered = 0

# Setup GPIO Pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
inputs = [16, 19]
GPIO.setup(inputs, GPIO.IN)
outputs = [4, 6, 12, 13, 20, 21, 26]
GPIO.setup(outputs, GPIO.OUT)
GPIO.output(outputs, GPIO.HIGH)

while True :
	while discovered == 0:
		# Send DISCOVER broadcast
		mydevice = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		mydevice.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		mydevice.sendto(bytes(discover, 'utf-8'),('192.168.24.255', 4961))
		data, addr = mydevice.recvfrom(1024)
		data = data.decode('utf-8')
		print(data)
		# Split the response into a dictionary
		data_split = data.split("\r\n")
		data_split.pop()
		data_in = dict(d.split(": ", 1) for d in data_split)
		if(data_in["operation"] == "acknowledge") :
			discovered = 1
			print("Sending Capabilities\r\n", capabilities)
			# Respond to ACKNOWLEDGE message with RESPONSE
			mydevice.sendto(bytes(capabilities,'utf-8'), addr)

	mydevice.close()
	mydevice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mydevice.settimeout(0.5)
	mydevice.connect(addr)

	while (data != 0):
		try:
			data = mydevice.recv(1024)
		except socket.timeout:
			data = -1

		if(data > 0):
			print("Data Available")
			data = data.decode('utf-8')
			print(data)
			# Split the response into a dictionary
			data_split = data.split("\r\n")
			data_split.pop()
			data_in = dict(d.split(": ", 1) for d in data_split)
			if(data_in["operation"] == "status change") :
				print("Status changed")
				if(data_in["state"] == "ON") :
					GPIO.output([6, 12, 13], GPIO.LOW)
				else:
					GPIO.output([6, 12, 13], GPIO.HIGH)
				# Respond to STATUS CHANGE message with ACKNOWLEDGE
				mydevice.send(bytes(acknowledge,'utf-8'))
		if(GPIO.input(16) == GPIO.LOW) :
			mydevice.send(bytes(status_change_on if status == 0 else status_change_off, 'utf-8'))
			GPIO.output(4, GPIO.LOW if status == 0 else GPIO.HIGH)
			status ^= 1
			print("Switch toggled: ", status)
			time.sleep(0.25)
	mydevice.close()
	discovered = 0
