import sys
sys.path.append("../")

import utils.GPIO as GPIO
import config.params as params

class Touch:
    def __init__(self, pins = params.touch_pins):
        self.pins = pins
        GPIO.setup(self.pins['E'], 'in')
        GPIO.setup(self.pins['O'], 'in')

    def is_something_touched(self):
        return self.read('E') or self.read('O')

    def read(self, dir):
        return GPIO.input(self.pins[dir])
