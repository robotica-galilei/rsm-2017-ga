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

    def release_n_kits(self, n_kit = 2):
        if n_kit > 2:
            print ('ERROR RELEASING KITS')

        else:
            for i in range[n_kit]:
                self.release_one_kit()
                time.sleep(1);
