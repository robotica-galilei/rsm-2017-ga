import sys
sys.path.append("../")

import time
import Adafruit_BBIO.PWM as PWM
import config.params as params
import led

class Kit:
    def __init__(self, servo_pin = params.kit_servo_pin):
        self.servo_pin = servo_pin
        self.l = led.Led()

    def release(self):
        PWM.start(self.servo_pin, 87, 60, 1)
        self.l.blink()

    def retract(self):
        PWM.start(self.servo_pin, 95, 60, 1)

    def release_one_kit(self):
        self.release()
        self.l.blink()
        time.sleep(1)
        self.retract()

    def blink(self):
        self.l.blink()

    def release_n_kits(self, n_kit = 2):
        if n_kit > 2:
            print ('ERROR RELEASING KITS')
            n_kit = 2

        for i in range[n_kit]:
            self.release_one_kit()
            time.sleep(1);
