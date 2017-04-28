import time
import Adafruit_BBIO.PWM as PWM

class Kit:
    def __init__(self, servo_pin = params.kit_servo_pin):
        self.servo_pin = servo_pin

    def release(self):
        PWM.start(self.servo_pin, 95, 60, 1)

    def hold(self):
        PWM.start(self.servo_pin, 87, 60, 1)

    def release_one_kit(self):
        PWM.start(self.servo_pin, 95, 60, 1)
        time.sleep(1)
        PWM.start(self.servo_pin, 87, 60, 1)
