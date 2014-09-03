"""
Author: Biswaranjan Das
WSU Pullman, WA.

PANASONIC GRIDEYE BREAKOUT BOARD WITH PIC24F04KA200 Microcontroller
Interfacing with x86,x64,ARM based machines with Python 2.7.

Dependencies:
	PySerial
	Python Imaging Library (can be substituted for pygame, opencv, tkinter)

"""

#headers and imports.
from __future__ import print_function
from serial import *
import atexit
from threading import Thread
import sys
from struct import unpack
import Image


#load 8px,8px image with white background.
img = Image.new( 'RGB', (8,8), "white") 
pixels = img.load()
fl = open('data.dat', 'a')

#global variables to keep track of event frame.
count=0


"""
input parameters: ser -> serial device in usage. by
this time, we have enabled the timer. Processing info.

output : no returns. saves image from PIR to gg#.jpg for all # in int.

"""
def receiving(ser):
    global count
    while(True):
		try:
			ser.read()
			ser.read()
			ser.read()
			lsb=ser.read()
			msb=ser.read()
			therm=int((ord(msb)<<8)+ord(lsb))
			celTherm=therm*0.0625
			count+=1
			print("AVG TEMP: "+str(celTherm))
			for i in range(64):
				try:
					lsb=ser.read()
					msb=ser.read()
					temp=int((ord(msb)<<8)+ord(lsb))
					while (temp>2047):
						temp = 2048-temp
					celcius=0.25*temp
					if (celcius>0):
						fl.write(str(celcius))
						fl.write(",")
						print(celcius)
					else:
						return
					if(int(celcius)>int(celTherm)):
						pixels[7-(i%8),7-(i/8)]=(200,0,0)
					elif(int(celcius)<int(celTherm)):
						pixels[7-(i%8),7-(i/8)]=(0,0,200)
					else:
						pixels[7-(i%8),7-(i/8)]=(0,100,0)
				except Exception, e:
					e.args += (color,temp,)
					raise
			newim = img.resize((500,500), Image.ANTIALIAS)
			newim.save('gg'+str(count)+'.jpg')
			fl.write("\n\n\n")
		except Exception, e:
			ser.open()
			ser.write('~')
			ser.write('~')
			ser.write('*')
			pass
    pass
		
def exitSafe(ser):
	try:
		ser.write('~')
		ser.close();
		fl.close()
	except:
		pass


"""
main function. 
no input/output.

config serial device : with baudrate=115200,Data=8Bits,Timeout=0.1

"""
if __name__ ==  '__main__':
    ser = Serial(
        port='/dev/ttyUSB0',
        baudrate=115200,
        bytesize=EIGHTBITS,
        parity=PARITY_NONE,
        stopbits=STOPBITS_ONE,
        timeout=0.1,
        rtscts=0,
        xonxoff=0
    )
    
    #close to make sure we have no trouble opening.
    ser.close()
    
    #open serial device.
    ser.open()
    
    #write '~' to close if the timer is pre-enabled.
    ser.write('~')
    
    #write '*' to enable timer.
    ser.write('*')

	#dynamic thread to process received data.
    Thread(target=receiving, args=(ser,)).start()
    atexit.register(exitSafe, ser)
    
