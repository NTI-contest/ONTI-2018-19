#!/usr/bin/env python

import serial 
import time 
import os

ser=serial.Serial("/dev/ttyACM0",9600) 
ser.baudrate=9600
 
read_ser=ser.readline() 
print(read_ser)
if read_ser!='0':
    while True:
        os.system ("sudo curl -s -o /dev/null http://192.168.88.67:\
            8080/0/action/snapshot")
        time.sleep(0.5)
        os.system ("sudo scp lastsnap.jpg terfire@192.168.88.156:\ОНТИ/Test1")