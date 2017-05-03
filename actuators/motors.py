import sys
sys.path.append("../")
import time
import logging

import Adafruit_BBIO.PWM as PWM
import utils.GPIO as GPIO
import config.params as params
import config.dimensions as dim
import motors_pid as pid


MOTOR_CELL_TIME     =       2.5
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
            print("Cosalfa, senalfa: ", cosalfa, senalfa)
            error = z * senalfa
            print("PID: ", pid.get_pid(error))
            self.setSpeeds(-40*error, 40*error)
            if senalfa <= params.ERROR_SENALFA and senalfa>= -params.ERROR_SENALFA:
                break
        '''
        self.stop()

    """
    Here start the simple functions for robot motion execution
    """
    def oneCellForward(self, power= MOTOR_DEFAULT_POWER_LINEAR, wait= MOTOR_CELL_TIME, mode= 'time', ch=None, tof= None, gyro=None):
        logging.info("Going one cell forward")
        if mode == 'time':
            logging.debug("Going by time")
            self.setSpeeds(power, power)
            time.sleep(wait)

        elif mode == 'gyro':
            logging.debug("Going by gyro")
            self.setSpeeds(power, power)
            front = tof.read_fix('N')[0]
            gyro.update()
            deg = gyro.yawsum
            now = tof.read_fix('N')[0]
            avg = tof.read_fix('N')[0]
            best_dir = 'N'
            boost = 0
            if now > 600 or now == -1:
                print("Using SOUTH sensor")
                front = tof.read_fix('S')[0]
                best_dir = 'S'
                now = tof.read_fix('S')[0]
            else:
                print("Using NORTH sensor")
            started_time = time.time()
            while True:
                print("Cell difference", (now,front))
                if  (best_dir == 'N' and front-now > dim.cell_dimension) or (best_dir == 'S' and now-front > dim.cell_dimension):
                    print("Front tof has recorded cell difference", (now,front))
                    break
                if not (avg>100 or avg ==-1):
                    print("Front avg recorded wall", avg)
                    break
                if not time.time()-started_time < MOTOR_CELL_TIME+0.5:
                    print("Max time passed")
                    break
                now = tof.read_fix(best_dir)[0]
                avg = tof.read_fix('N')[0]
                print(now)
                if ch.is_something_touched():
                    time.sleep(0.3)
                    if ch.read('E') and ch.read('O'):
                        break
                    if ch.read('E'):
                        self.disincagna(gyro, -1, deg)
                    else:
                        self.disincagna(gyro, 1, deg)
                gyro.update()
                correction = deg - gyro.yawsum
                '''
                if gyro.pitch > 15:
                    if boost < 20:
                        boost += 1
                        time.sleep(0.05)
                    started_time = time.time()
                elif gyro.pitch < -15:
                    if boost < -30:
                        boost -= 1
                        time.sleep(0.05)
                    started_time = time.time()
                else:
                    if boost > 0:
                        boost -= 1
                        time.sleep(0.05)
                    elif boost < 0:
                        boost += 1
                        time.sleep(0.05)
                '''
                self.setSpeeds(power - correction + boost, power + correction + boost)


        elif mode == 'tof_fixed':
            side, avg, cosalfa, senalfa, z = tof.best_side('E','O')
            side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')

            if avg2 < avg and avg2 != -1:
                cosalfa = cosalfa2
                senalfa = senalfa2

            N_prec = tof.n_cells(avg2, cosalfa)*z2
            N_now = N_prec
            x=0

            while(N_prec == N_now):
                print("N", (N_prec, N_now))
                side, avg, cosalfa, senalfa, z = tof.best_side('E','O')
                side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')


                if avg2 < avg and avg2 != -1:
                    cosalfa = cosalfa2
                    senalfa = senalfa2

                error=tof.error(avg, cosalfa, z)

                if error != None:
                    correction = pid.get_pid(error)

                else:
                    correction = 0

                self.setSpeeds(power*(1+correction),power*(1-correction))

                distance=tof.real_distance(avg2,cosalfa)
                if(distance<=(N_prec*dim.cell_dimension)):
                    # I'm still in the same cell
                    x=0

                else:
                    if x==0:
                        x=1
                        #non sono sicuro della cella
                    if x==1:
                        x=2
                        #confermo la cella
                        logging.info('Now we are in the next cell')
                    else:
                        pass
                        #Next cell

                N_now = z2*tof.n_cells(avg2, cosalfa)
            self.parallel(tof)

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
        logging.info("Arrived in centre of the cell")
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

            start = time.time()
            self.setSpeeds(-30,30)
            while(gyro.update().yawsum <= now+degrees-2 and time.time()-start > 3):
                pass
        else:
            self.setSpeeds(40,-40)
            while(gyro.update().yawsum >= now+degrees+4):
                pass

            self.setSpeeds(30,-30)
            start = time.time()
            while gyro.update().yawsum >= now+degrees+2 and time.time()-start > 3:
                pass
        self.stop()

    def set_degrees(self, gyro, degrees):
        now = gyro.update().yawsum
        diff = now-degrees
        self.rotateDegrees(gyro, -diff)


    def disincagna(self, gyro, dir, deg = None): #Best name ever
        dir_lib = {1:'O', -1:'E'}
        logging.debug('Disincagna %s', dir_lib[dir])
        self.setSpeeds(-20,-20)
        time.sleep(0.4)
        self.rotateDegrees(gyro, 30*dir)
        self.setSpeeds(-20, -20)
        time.sleep(0.8)
        self.rotateDegrees(gyro, -60*dir)
        self.setSpeeds(20, 20)
        time.sleep(0.8)

        if deg != None:
            self.set_degrees(gyro, deg)
        else:
            self.rotateDegrees(gyro, 30*dir)
        self.setSpeeds(20,20)
        time.sleep(0.4)
