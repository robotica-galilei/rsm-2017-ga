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

    def parallel(self, tof = None):
        side, avg, cosalfa, senalfa, z = tof.best_side('E','O')
        side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')
        if avg2 < avg and avg2 != -1:
            side = side2
            cosalfa = cosalfa2
            senalfa = senalfa2
            avg = avg2
            z = z2
        all_m = [None, None, None, None, None, None, None, None, None, None]
        while True:
            del(all_m[0])
            measurement = tof.diff(dir = side)
            print(measurement)
            all_m.append(measurement)
            e = 0
            sum_m = 0
            for i in range(10):
                if all_m[i] != None:
                    e += 1
                    sum_m += all_m[i]
            correction = float(sum_m)/float(e)
            print(all_m)
            print(correction)
            print()

            if correction > 0:
                z = -1
            else:
                z = 1
            if ((correction < 5 and correction > -5) or (measurement < 1 and measurement > -1)):
                break

            self.setSpeeds(30*z, -30*z)


        '''
        while True:
            side, avg, cosalfa, senalfa, z = tof.best_side('E','O')
            side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')

            if avg2 < avg and avg2 != -1:
                side = side2
                cosalfa = cosalfa2
                senalfa = senalfa2
                avg = avg2
                z = z2
            print("Cosalfa: ", cosalfa)
            error=tof.error(avg, cosalfa, z)
            print("PID: ", pid.get_pid(error))
            self.setSpeeds(-40*z, 40*z)
            if cosalfa >= params.ERROR_COSALFA:
                break
        '''
        self.stop()

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
            now = tof.read_raw('N')
            avg = tof.read_fix('N')
            if now > 600 or now == -1:
                front = tof.read_raw('S')
                now = tof.read_raw('S')
                while(now-front<= 300 or (avg<30 and avg !=-1)):
                    now = tof.read_raw('S')
                    avg = tof.read_fix('N')
                    print(now)
                    if ch.is_something_touched():
                        time.sleep(0.3)
                        if ch.read('E') and ch.read('O'):
                            break
                        if ch.read('E'):
                            self.disincagna(gyro, -1, deg)
                            print("Disincagna E")
                        else:
                            self.disincagna(gyro, 1, deg)
                            print("Disincagna O")
                    gyro.update()
                    correction = deg - gyro.yawsum
                    self.setSpeeds(power - correction, power + correction)
            else:
                while(front- now<= 300 or (avg<30 and avg !=-1)):
                    now = tof.read_raw('N')
                    avg = tof.read_fix('N')
                    print(now)
                    if ch.is_something_touched():
                        time.sleep(0.3)
                        if ch.read('E') and ch.read('O'):
                            self.setSpeeds(-30,-30)
                            time.sleep(0.1)
                            self.stop()
                            break
                        if ch.read('E'):
                            self.disincagna(gyro, -1, deg)
                            print("Disincagna E")
                        else:
                            self.disincagna(gyro, 1, deg)
                            print("Disincagna O")
                    gyro.update()
                    correction = deg - gyro.yawsum
                    self.setSpeeds(power - correction, power + correction)
            print("FINECELLA")
        elif mode == 'tof_fixed':
            side, avg, cosalfa, senalfa, z = tof.best_side('E','O')
            side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')

            if avg2 < avg and avg2 != -1:
                cosalfa = cosalfa2
                senalfa = senalfa2

            N_prec = tof.n_cells(avg2, cosalfa)*z2
            N_now = N_prec

            while(N_now -  N_prec - 1 < 0):
                side, avg, cosalfa, senalfa, z = tof.best_side('E','O')
                side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')


                if avg2 < avg and avg2 != -1:
                    cosalfa = cosalfa2
                    senalfa = senalfa2

            error=tof.error(avg_eo, cosalfa, z_eo)

            if error != None:
                correction = pid.get_pid(error)

            else:
                correction = 0

            self.setSpeeds(power*(1+correction),power*(1-correction))

            N_now = z2*tof.n_cells(avg2, cosalfa)

        """
        elif mode == 'complete':
            side1, avg1, cosalfa1, senalfa1, z1 = self.best_side('E','O')
            side2, avg2, cosalfa2, senalfa2, z2 = self.best_side('N','S')
            if avg1 == -1:
                '''use gyro and time'''
                if avg2 == -1:
                    '''only gyro'''
                     pass

                else:
                    cosalfa = cosalfa2

            else
                elif avg1 < avg2:
                    cosalfa = cosalfa1

                elif avg2 <= avg1:
                    cosalfa = cosalfa2

            if :
                    parallel(cosalfa)




            print (cosalfa)



        """
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
            while(gyro.update().yawsum <= now+degrees-4):
                pass
            self.setSpeeds(-20,20)
            while(gyro.update().yawsum <= now+degrees-2):
                pass
        else:
            self.setSpeeds(40,-40)
            while(gyro.update().yawsum >= now+degrees+4):
                pass

            self.setSpeeds(20,-20)
            while(gyro.update().yawsum >= now+degrees+2):
                pass
        self.stop()

    def set_degrees(self, gyro, degrees):
        now = gyro.update().yawsum
        diff = now-degrees
        self.rotateDegrees(gyro, -diff)


    def disincagna(self, gyro, dir, deg = None): #Best name ever
        self.setSpeeds(-20,-20)
        time.sleep(0.2)
        self.rotateDegrees(gyro, 35*dir)
        self.setSpeeds(-MOTOR_DEFAULT_POWER_LINEAR, -MOTOR_DEFAULT_POWER_LINEAR)
        time.sleep(0.2)
        if deg != None:
            self.set_degrees(gyro, deg)
        else:
            self.rotateDegrees(gyro, -35*dir)
        self.setSpeeds(20,20)
        time.sleep(0.2)
