#!/usr/bin/env python3
#
# This is a NetworkTables client (eg, the DriverStation/coprocessor side).
# You need to tell it the IP address of the NetworkTables server (the
# robot or simulator).
#

# in command prompt, type
# "pip install pynput" to install pynput.
# "pip install pynetworktables" to install py network table
# "pip install pyserial" to install the serial library


import sys
import time
from networktables import NetworkTables
from pynput.keyboard import Key, Controller
# To see messages from networktables, you must setup logging
import logging
import serial
import time
from serial.tools import list_ports
import socket

port = 3620
logging.basicConfig(level=logging.DEBUG)
ip = "10.39.32.2"
NetworkTables.initialize(server=ip)

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


activePort = ""
pico = None
alreadyConnected = False


def closePort(activePort):
   global pico, alreadyConnected
   alreadyConnected = False
   activePort = ""
   pico = None
   print("serial port closed")


def openPort(port):
   global alreadyConnected, pico
   try:
      pico = serial.Serial(port)
      pico.baudrate = 115200  # set Baud rate to 115200
      pico.bytesize = 8  # Number of data bits = 8
      pico.parity = "N"  # No parity
      pico.stopbits = 1
      alreadyConnected = True
      print('serial port', port, 'opened')
   except:
      pass


def checkOnPort():
   global alreadyConnected, activePort
   serialPortList = []
   if list_ports.comports():
      for port in list_ports.comports():
         serialPortList.append(str(port).split()[0])
   if (activePort not in serialPortList) and alreadyConnected:
      closePort(activePort)
   if len(serialPortList) > 0:
      activePort = serialPortList[-1]
      if not alreadyConnected:
         openPort(activePort)


def picoWrite(data):
	global pico
	if pico != None:
		try:
			pico.write(data)
		except:
			pass


def read():
	global pico
	if pico != None:
		try:
			num = pico.in_waiting
			if num <= 0:
				return ""
			result = pico.readline()
			print(str(result))
			return result
		except:
			pass
	return ""


def valueChanged(table, key, value, isNew):
   global lastValue
   if key == "BatVolts":
      print("valueChanged: key: '%s'; value: %s; isNew: %s" %(key, value, isNew))
      if value == 0:
         # Setup so will display a disabled condition
         picoWrite(b"-1\r")
         print("Send disable")
      else:
         if value > 12.2:
            print("Send Green")
            picoWrite(b"0\r")
         elif value > 11.9:
            print("Send Yellow")
            picoWrite(b"1\r")
         else:
            print("Send RED")
            picoWrite(b"2\r")
         # Next line is for testing only
         # s.write(values[lastValue % len(values)])
         lastValue += 1
   # Count is a watch dog to make sure that the mini drive station is connected
   if key == "Count":
      print("valueChanged: key: '%s'; value: %s; isNew: %s" %(key, value, isNew))


def connectionListener(connected, info):
   print(info, "; Connected=%s" % connected)


# Codes to send to mini drive station
# 0 - red, 1 - green, 2 - blue, 3 - yellow, 4 - white
values = [b'0\r', b'1\r', b'2\r', b'3\r', b'4\r']
lastValue = 0
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
sd = NetworkTables.getTable("SmartDashboard")
sd.addEntryListener(valueChanged)
count = 0
disableCount = 0
# Get time in seconds
lastMilli = time.time()
while True:
   checkOnPort()
   if time.time() > lastMilli + 1:
      count += 1
      sd.putNumber("Disable", count)
      if count > 100:
         count = 0
      lastMilli = time.time()
   result = read()
   if 'disable' in str(result[-9:]):
      print("Send disable to robot count:", disableCount)
      message = "disable:" + str(count)
      clientSock.sendto(message.encode('utf-8'), (ip, port))
      sd.putNumber("Disable", 3932)
      disableCount += 1
      time.sleep(.1)
