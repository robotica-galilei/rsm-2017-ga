import sys
sys.path.append("../")

import utils.GPIO as GPIO
import config.params as params

name_meaning=[None,'U','S','H']
position_meaning=[None,'Incoming','Center','Passed']

class visualVictim:
    def __init__(self, pins = params.victim_pins):
        self.pins = pins
        for i in self.pins:
            GPIO.setup(i, 'in')

    def readVictim(self):
        bit_readings=[]
        for i in range(8):
            bit_readings.append(GPIO.input(self.pins[i]))
        processed_readings=[]
        for i in range(4):
            processed_readings.append(int(str(bit_readings[2*i])+str(bit_readings[2*i+1]),2))
        self.victims_found=[]
        self.victims_found.append((name_meaning[processed_readings[0]],position_meaning[processed_readings[1]]))
        self.victims_found.append((name_meaning[processed_readings[2]],position_meaning[processed_readings[3]]))
        return self
