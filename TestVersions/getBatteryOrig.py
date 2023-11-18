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
import serial.tools.list_ports
import socket

port = 3620
logging.basicConfig(level=logging.DEBUG)
ip = "10.39.32.2"
NetworkTables.initialize(server=ip)

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def setupSerial():
    ports = serial.tools.list_ports.comports()
    coms = []
    for p in ports:
        coms.append(p.device)
    port = coms[-1]
    print("Will use port:", port, " all ports:", coms)
    s = serial.Serial(port)
    s.baudrate = 115200  # set Baud rate to 115200
    s.bytesize = 8     # Number of data bits = 8
    s.parity   ='N'    # No parity
    s.stopbits = 1     # Number of Stop bits = 1
    return s

def read():
   num = s.in_waiting
   if num <= 0:
     return ""
   result = s.readline()
   print(str(result))
   return result


def valueChanged(table, key, value, isNew):
    global s, lastValue
    if key == "BatVolts":
        print("valueChanged: key: '%s'; value: %s; isNew: %s" %
              (key, value, isNew))
        if value == 0:
          # Setup so will display a disabled condition
          s.write(b'-1\r')
          print("Send disable")
        else:
          if value > 12.2:
             print("Send Green")
             s.write(b'0\r')
          elif value > 11.9:
             print("Send Yellow")
             s.write(b'1\r')
          else:
             print("Send RED")
             s.write(b'2\r')
          # Next line is for testing only
          # s.write(values[lastValue % len(values)])
          lastValue += 1
    # Count is a watch dog to make sure that the mini drive station is connected
    if key == "Count":
        print("valueChanged: key: '%s'; value: %s; isNew: %s" %
              (key, value, isNew))

def connectionListener(connected, info):
    print(info, "; Connected=%s" % connected)

# Codes to send to mini drive station
# 0 - red, 1 - green, 2 - blue, 3 - yellow, 4 - white
values = [b'0\r', b'1\r', b'2\r', b'3\r', b'4\r']
lastValue = 0
s = setupSerial()
NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
sd = NetworkTables.getTable("SmartDashboard")
sd.addEntryListener(valueChanged)
count = 0
disableCount = 0
# Get time in seconds
lastMilli = time.time()
while True:
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
    
  
   
