# Panasonic PIC24F04KA200 PIRGridEye Driver

This is a Python driver for this Passive Infrared Sensor by Panasonic. The output from this sensor is a 8x8 matrix of float. The accuracy is upto 0.25 Celsius for each grid. This software is written using PySerial. 
We use the USB I2C bridge to connect the PIC24F04KA200  to the computer. The output is displayed using PIL (Python Imaging Library) as RGB. 


NOTE: The RGB is not scaled




(C) Biswaranjan Das 2014.
