import sys
sys.path.append("../")
import time

import config.params as params
import utils.GPIO as GPIO

class Led:
    def __init__(self, pin= params.LED_PIN):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def blink(self, delay= params.LED_BLINK_DELAY):
        '''
        Blink the Led
        '''
        self.on()
        time.sleep(delay)
        self.off()


    def on(self):
        '''
        Turn on the Led
        '''
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        '''
        Turn off the Led
        '''
        GPIO.output(self.pin, GPIO.LOW)
