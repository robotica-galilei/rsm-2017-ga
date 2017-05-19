import sys
sys.path.append("../")
import time
import logging
import math

import Adafruit_BBIO.PWM as PWM
import utils.GPIO as GPIO
import config.params as params
import config.dimensions as dim
import motors_pid as pid
import sensors.sensors_handler as sm


MOTOR_CELL_TIME     =       1.3
MOTOR_MIN_CELL_TIME     =       0.4
MOTOR_ROTATION_TIME =       1.5
MOTOR_DEFAULT_POWER_LINEAR      =       50
MOTOR_PRECISION_POWER_LINEAR      =       25
MOTOR_DEFAULT_POWER_ROTATION    =       70


class Motor:
    def __init__(self, pins = params.motors_pins):
        """
        pins are provided by a dictionary formatted like:
        {
            'fr':fr,
            'fl':fl,
            'rr':rr,
            'rl':rl,
            'dir_fr':dir_fr,
            'dir_fl':dir_fl,
            'dir_rr':dir_rr,
            'dir_rl':dir_rl
        }
        """
        GPIO.setup(pins['dir_fr'], GPIO.OUT)
        GPIO.setup(pins['dir_fl'], GPIO.OUT)
        GPIO.setup(pins['dir_rr'], GPIO.OUT)
        GPIO.setup(pins['dir_rl'], GPIO.OUT)

        self.pins = pins
        self.actual_l = 0
        self.actual_r = 0

    def setSpeedLeft(self, power):
        if(power<0):
            GPIO.output(self.pins['dir_fl'],GPIO.LOW)
            GPIO.output(self.pins['dir_rl'],GPIO.LOW)
        else:
            GPIO.output(self.pins['dir_fl'],GPIO.HIGH)
            GPIO.output(self.pins['dir_rl'],GPIO.HIGH)

        power = abs(power)
        if power > 100:
            power = 100
        PWM.start(self.pins['fl'], power, 25000)
        PWM.start(self.pins['rl'], power, 25000)
        self.actual_l = power

    def setSpeedRight(self, power):
        if(power<0):
            GPIO.output(self.pins['dir_fr'],GPIO.LOW)
            GPIO.output(self.pins['dir_rr'],GPIO.LOW)
        else:
            GPIO.output(self.pins['dir_fr'],GPIO.HIGH)
            GPIO.output(self.pins['dir_rr'],GPIO.HIGH)

        power = abs(power)
        if power > 100:
            power = 100
        PWM.start(self.pins['fr'], power, 25000)
        PWM.start(self.pins['rr'], power, 25000)
        self.actual_r = power

    def stopLeft(self):
        self.setSpeedLeft(0)

    def stopRight(self):
        self.setSpeedRight(0)

    def setSpeeds(self, l_power, r_power):
        self.setSpeedLeft(l_power)
        self.setSpeedRight(r_power)

    def stop(self):
        self.stopLeft()
        self.stopRight()
