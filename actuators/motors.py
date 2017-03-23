import Adafruit_BBIO.PWM as PWM

class Motor:
    def __init__(self, fr, fl, rr, rl):
        self.pins = {'fr':fr, 'fl':fl, 'rr':rr, 'rl':rl}
        self.actual_l = 0
        self.actual_r = 0

    def setSpeedLeft(self, power):
        PWM.start(self.pins['fl'], power, 25000)
        PWM.start(self.pins['rl'], power, 25000)
        self.actual_l = power

    def setSpeedRight(self, power):
        PWM.start(self.pins['fr'], power, 25000)
        PWM.start(self.pins['rr'], power, 25000)
        self.actual_r = power

    def stopLeft(self):
        self.setSpeedLeft(0)

    def stopRight(self):
        self.setSpeedRight(0)

    def setSpeeds(self, left, right, l_power, r_power):
        self.setSpeedLeft(l_power)
        self.setSpeedRight(r_power)

    def stop(self):
        self.stopLeft()
        self.stopRight()
