import sys
sys.path.append("../")
import time
import logging

import Adafruit_BBIO.PWM as PWM
import utils.GPIO as GPIO
import config.params as params
import config.dimensions as dim
import motors_pid as pid
import sensors.sensors_handler as sm


MOTOR_CELL_TIME     =       1.6
MOTOR_MIN_CELL_TIME     =       1.3
MOTOR_ROTATION_TIME =       1.5
MOTOR_DEFAULT_POWER_LINEAR      =       50
MOTOR_DEFAULT_POWER_ROTATION    =       60


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

            self.setSpeeds(MOTOR_DEFAULT_POWER_ROTATION*z, -MOTOR_DEFAULT_POWER_ROTATION*z)


        """
        def parallel(self, senalfa_prec, tof=None)


            while True:
                side, avg, cosalfa, senalfa,s_dif, z = tof.best_side('E','O')
                side2, avg2, cosalfa2, senalfa2,s_dif2, z2 = tof.best_side('N','S')

                if avg2 < avg and avg2 != -1:
                    side = side2
                    cosalfa = cosalfa2
                    senalfa = senalfa2
                    avg = avg2
                    z = z2

                if s_dif<=2 and s_dif2<=2
                error = z * math.sin(math.radius(senalfa))
                logging.INFO("Cosalfa, senalfa: ", cosalfa, senalfa)
                error = z * senalfa
                correzione = pid.get_pid(params.PID_p_ROTATION, params.PID_i_ROTATION, params.PID_d_ROTATION, error = error)
                self.setSpeeds(-MOTOR_DEFAULT_POWER_ROTATION*correzione, MOTOR_DEFAULT_POWER_ROTATION*)
                if senalfa <= params.ERROR_SENALFA and senalfa>= -params.ERROR_SENALFA:
                    break
        """
            self.stop()

        """
    Here start the simple functions for robot motion execution
    """
    def oneCellForward(self, power= MOTOR_DEFAULT_POWER_LINEAR, wait= MOTOR_CELL_TIME, mode= 'time', ch=None, tof= None, gyro=None, h=None, mat = None):
        logging.info("Going one cell forward")
        if mode == 'time':
            avg = now
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
            best_dir = 'N'
            boost = 0
            a_tempo = False
            if now > 750 or now == -1:
                front = tof.read_fix('S')[0]
                if front > 750 or front == -1:
                    a_tempo = True
                print("Using SOUTH sensor")
                best_dir = 'S'
                now = front
            else:
                print("Using NORTH sensor")
            started_time = time.time()
            mat.itemset(pos, 512)
            if not a_tempo:
                while True:
                    print("Cell difference", (now,front))
                    victims = sm.check_victim(pos,h)
                    if (victims[0]):
                        time_before_victims = time.time()
                        m.saveAllVictims(h)
                        started_time += time.time() - time_before_victims
                    now = tof.read_fix(best_dir)[0]
                    avg = tof.read_fix('N')[0]
                    if gyro.pitch < 15 and gyro.pitch > -15:
                        if  (best_dir == 'N' and front-now > dim.cell_dimension) or (best_dir == 'S' and now-front > dim.cell_dimension):
                            print("Front tof has recorded cell difference", (now,front))
                            break
                        if not (avg>100 or avg ==-1):
                            print("Front avg recorded wall", avg)
                            break
                        if not time.time()-started_time < MOTOR_CELL_TIME+0.3:
                            print("Max time passed")
                            break

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

                    if gyro.pitch > 15:
                        self.setSpeeds(-30,-30)
                        time.sleep(1)
                        self.setSpeeds(70,70)
                        time.sleep(0.6)
                        gyro.update()
                        while(gyro.pitch > 15):
                            self.setSpeeds(70 + gyro.roll, 70 - gyro.roll)
                            gyro.update()

                    self.setSpeeds(power - correction, power + correction )
            else:
                self.setSpeeds(MOTOR_DEFAULT_POWER_LINEAR, MOTOR_DEFAULT_POWER_LINEAR)
                time.sleep(MOTOR_CELL_TIME)
                self.stop()




        elif mode == 'tof_fixed':

            #### now it should be a wall follower
            side, avg, cosalfa, senalfa,s_div, z = tof.best_side('E','O')
            side2, avg2, cosalfa2, senalfa2, s_div2, z2 = tof.best_side('N','S')
            gyro.update()
            deg=gyro.yawsum()

            if avg2 < avg and avg2 != -1:
                cosalfa = cosalfa2
                senalfa = senalfa2

            if s_div2 < 2 and s_div1 < 2:
                time.sleep(0.05)
                gyro.update()
                grad=gyro.yawsum()
                cosalfa = math.cos(math.radians(deg-grad))

#            N_prec = tof.n_cells(avg2, cosalfa, k = dim.cell_long)*z2
#            N_now = N_prec
#            x=0

            while (True):
#            while(N_prec <= N_now or x!=4):
                print("N", N_prec, N_now)
                side, avg, cosalfa, senalfa, z = tof.best_side('E','O')
                avg2, cosalfa2, senalfa2, s_div2=read_fix(side2)


                if avg2 < avg and s_div2==3:
                    cosalfa = cosalfa2
                    senalfa = senalfa2

                if s_div2 <= 2 and s_div1 <= 2:
                    gyro.update()
                    grad=gyro.yawsum()
                    cosalfa = math.cos(math.radians(deg-grad))



                error=tof.error(avg, cosalfa, z)

                logging.info("avg, cosalfa = "avg, cosalfa)
                logging.info("error = ", error)

                if error != None:
                    correction = pid.get_pid(error)

                else:
                    correction = 0

                logging.info("correction = ", correction)
                self.setSpeeds(power*(1+correction),power*(1-correction))
"""
                distance=tof.real_distance(avg2,cosalfa)
                if(z2 * distance<=(N_prec*dim.cell_long) and x != 3):
                    # I'm still in the same cell
                    x=0

                else:
                    if x==0:
                        x=1
                        #not really sure about in which cell I am
                    if x==1:
                        x=2
                        #yes, I am sure about this shit
                        logging.info('Now we are in the next cell')
                    else:
                        x=3
                        #Next cell
                        if N_prec== -1:
                            x=4
                            #stop
                N_now = z2*tof.n_cells(avg2, cosalfa)
"""




        self.parallel()
        logging.info("Arrived in centre of the cell")
        self.stop()
        return mat


    def saveAllVictims(self, h, k):
        turn = 1
        if 'N' in victims[1]:
            k.release_one_kit()
        if 'E' in victims[1]:
            for i in range(turn):
                self.rotateRight(gyro)
            k.release_one_kit()
            turn = 1
        else:
            turn += 1
        if 'S' in victims[1]:
            for i in range(turn):
                self.rotateRight(gyro)
            k.release_one_kit()
            turn = 1
        else:
            turn += 1
        if 'O' in victims[1]:
            if turn != 3:
                for i in range(turn):
                    self.rotateRight(gyro)
            else:
                self.rotateLeft(gyro)
            k.release_one_kit()
            turn = 1
        else:
            turn += 1

        if(turn < 4):
            for i in range(turn):
                self.rotateRight(gyro)



    def oneCellBack(self, power= MOTOR_DEFAULT_POWER_LINEAR, wait= MOTOR_CELL_TIME):
        self.setSpeeds(-power, -power)
        time.sleep(wait)
        self.stop()

    def rotateRight(self, gyro, power= MOTOR_DEFAULT_POWER_ROTATION, wait= MOTOR_ROTATION_TIME):
        self.rotateDegrees(gyro=gyro, degrees=-90)

        self.parallel()
        self.stop()

    def rotateLeft(self, gyro, power= MOTOR_DEFAULT_POWER_ROTATION, wait= MOTOR_ROTATION_TIME):
        self.rotateDegrees(gyro=gyro, degrees=90)

        self.parallel()
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

            self.setSpeeds(30,-30)
            start = time.time()
            while gyro.update().yawsum >= now+degrees+2 and time.time()-start > 3:
                pass
        self.stop()

        """
        if
        """

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
