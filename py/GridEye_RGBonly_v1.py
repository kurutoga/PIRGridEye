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
from serial import *
import atexit
from threading import Thread
from struct import unpack
import Image


#load 8px,8px image with white background.
img = Image.new( 'RGB', (8,8), "white") 
pixels = img.load()

#global variables to keep track of event frame.
count=0


"""
input parameters: ser -> serial device in usage. by
this time, we have enabled the timer. Processing info.

output : no returns. saves image from PIR to gg#.jpg for all # in int.

"""
def receiving(ser):
    global count
    while True:

        #read the first 5 bytes. {42,42,42,ThermistorL,ThermistorH}
        ser.read(5)	
        
        #increment out frame count. we are ready to stream.
        count+=1
        
        #range=8*8=64. for each we separate low bytes, print to image.
        for i in range(64):
            try:
                buf1 = ser.read()
                vg= unpack('B', buf1)
                #this will read high byte. to be ignored.
                buf1 = ser.read()
                
                #vg[0] has the temperature value in F. 
                if(int(vg[0])<80):
                    color=(0,0,vg[0])
                elif(int(vg[0])>80 and int(vg[0])<100):
                    color=((vg[0]-80)*50/20,(100-vg[0])*255/20,0)
                else:
                    color=((100-vg[0])*255/20,(vg[0]-100)*50/20,0)
                pixels[7-(i%8),7-(i/8)]=color
            except:
                print()
        
        #pprint for images basically. resizing antialias to 500x500
        #from 8x8
        newim = img.resize((500,500), Image.ANTIALIAS)
        newim.save('gg'+str(count)+'.jpg')
        
"""
input parameters: ser -> serial device in usage.
output : N/A

This function executes when we exit/terminate our python script.
This will make sure that out serial device (PIC24F04KA200) is not 
continuing to run after we terminate the appication. Write a '~'!!
"""
def exitSafe(ser):
	try:
		ser.write('~')
		ser.close();
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
    
    #function to make sure we have a termination procedure in place.
	atexit.register(exitSafe, ser)
