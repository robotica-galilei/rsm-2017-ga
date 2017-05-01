import sys
sys.path.append("../")
import time

import Adafruit_BBIO.PWM as PWM
import utils.GPIO as GPIO
import config.params as params
import motors_pid as pid

MOTOR_CELL_TIME     =       1.8
MOTOR_ROTATION_TIME =       1.5
MOTOR_DEFAULT_POWER_LINEAR      =       50
MOTOR_DEFAULT_POWER_ROTATION    =       40


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

        PWM.start(self.pins['fl'], abs(power), 25000)
        PWM.start(self.pins['rl'], abs(power), 25000)
        self.actual_l = power

    def setSpeedRight(self, power):
        if(power<0):
            GPIO.output(self.pins['dir_fr'],GPIO.LOW)
            GPIO.output(self.pins['dir_rr'],GPIO.LOW)
        else:
            GPIO.output(self.pins['dir_fr'],GPIO.HIGH)
            GPIO.output(self.pins['dir_rr'],GPIO.HIGH)

        PWM.start(self.pins['fr'], abs(power), 25000)
        PWM.start(self.pins['rr'], abs(power), 25000)
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

    """
    Here start the simple functions for robot motion execution
    """
    def oneCellForward(self, power= MOTOR_DEFAULT_POWER_LINEAR, wait= MOTOR_CELL_TIME, mode= 'time', ch=None, tof= None, gyro=None):
        if mode == 'time':
            self.setSpeeds(power, power)
            time.sleep(wait)
        elif mode == 'tof_raw':
            self.setSpeeds(30,30)
            front = tof.read_raw('N')
            while(front-tof.read_raw('N') <= 300):
                self.setSpeeds(power, power)
        elif mode == 'gyro':
            self.setSpeeds(30,30)
            front = tof.read_raw('N')
            gyro.update()
            deg = gyro.yawsum
            while(front-tof.read_raw('N') <= 300):
                if ch.is_something_touched():
                    time.sleep(0.3)
                    if ch.read('E') and ch.read('O'):
                        break
                    if ch.read('E'):
                        self.disincagna(gyro, -1)
                    else:
                        self.disincagna(gyro, 1)
                gyro.update()
                correction = deg - gyro.yawsum
                self.setSpeeds(power - correction, power + correction)
        elif mode == 'tof_fixed':
            front = tof.read_raw('N')
            now = tof.read_raw('N')
            while(front-now <= 300 and now > 100):
                now = tof.read_raw('N')
                error=tof.error()
                if error is not None:
                    correction = pid.get_pid(error)
                self.setSpeeds(power*(1+correction),power*(1-correction))
        self.stop()


    def oneCellBack(self, power= MOTOR_DEFAULT_POWER_LINEAR, wait= MOTOR_CELL_TIME):
        self.setSpeeds(-power, -power)
        time.sleep(wait)
        self.stop()

    def rotateRight(self, gyro, power= MOTOR_DEFAULT_POWER_ROTATION, wait= MOTOR_ROTATION_TIME):
        self.rotateDegrees(gyro=gyro, degrees=-90)
        self.stop()

    def rotateLeft(self, gyro, power= MOTOR_DEFAULT_POWER_ROTATION, wait= MOTOR_ROTATION_TIME):
        self.rotateDegrees(gyro=gyro, degrees=90)
        self.stop()

    def rotateDegrees(self, gyro, degrees):
        now = gyro.update().yawsum
        if degrees > 0:
            self.setSpeeds(-40,40)
            while(gyro.update().yawsum <= now+degrees):
                pass
        else:
            self.setSpeeds(40,-40)
            while(gyro.update().yawsum >= now+degrees):
                pass
        self.stop()

    def disincagna(self, gyro, dir): #Best name ever
        self.setSpeeds(-20,-20)
        time.sleep(0.2)
        self.rotateDegrees(gyro, 35*dir)
        self.setSpeeds(-MOTOR_DEFAULT_POWER_LINEAR, -MOTOR_DEFAULT_POWER_LINEAR)
        time.sleep(0.2)
        self.rotateDegrees(gyro, -35*dir)
        self.setSpeeds(20,20)
        time.sleep(0.2)
