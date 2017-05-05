import sys
sys.path.append("../")

import utils.GPIO as GPIO
import config.params as params
import serial

name_meaning=[None,'U','S','H']
position_meaning=[None,'Incoming','Center','Passed']

class visualVictim:
    def __init__(self, serialport = '/dev/ttyO5'):
        self.ser = serial.Serial(port = serialport, baudrate=115200)
        self.ser.close()
        self.ser.open()

    def readVictim(self):
        self.ser.flushInput()
        val=str(self.ser.readline())
        print (val)
        bit_readings=list(val)
        print (bit_readings)
        processed_readings=[]
        for i in range(4):
            processed_readings.append(int(bit_readings[2*i])*2+int(bit_readings[2*i+1]))
        print(processed_readings)
        self.victims_found=[]
        self.victims_found.append((name_meaning[processed_readings[0]],position_meaning[processed_readings[1]]))
        self.victims_found.append((name_meaning[processed_readings[2]],position_meaning[processed_readings[3]]))
        return self
