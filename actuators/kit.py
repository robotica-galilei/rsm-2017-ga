import sys
sys.path.append("../")

import time
import Adafruit_BBIO.PWM as PWM
import config.params as params

class Kit:
    def __init__(self, servo_pin = params.kit_servo_pin):
        self.servo_pin = servo_pin

    def release(self):
        PWM.start(self.servo_pin, 87, 60, 1)

    def retract(self):
        PWM.start(self.servo_pin, 95, 60, 1)
        
    def release_one_kit(self):
        self.release()
        time.sleep(1)
        self.retract()
