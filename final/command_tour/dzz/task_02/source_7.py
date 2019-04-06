import serial 
import time 

ser=serial.Serial("/dev/ttyACM0",9600) 
ser.baudrate=9600
 
read_ser=ser.readline() 
print(read_ser)