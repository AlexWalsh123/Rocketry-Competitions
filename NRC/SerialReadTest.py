import serial
import time

#ser1 = serial.Serial("COM3", 9600)
ser2 = serial.Serial("COM4", 9600)
ser2.flushInput()

while True:
     #cc=str(ser1.readline())
     #print("COM3")
     #print(cc[2:][:-5])

     cc2=str(ser2.readline())
     #print("COM4")
     print(cc2[2:][:-5])


     #print("#########################")
