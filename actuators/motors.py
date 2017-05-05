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


MOTOR_CELL_TIME     =       1.0
MOTOR_MIN_CELL_TIME     =       0.4
MOTOR_ROTATION_TIME =       1.5
MOTOR_DEFAULT_POWER_LINEAR      =       50
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

    def parallel(self, tof = None, times = 1, gyro = None, deg = None, slow = False):
        '''
        if deg!= None:
            self.set_degrees(gyro, deg)
        gyro.update()
        good_angle = gyro.yawsum
        for i in range(times):
            side, avg, cosalfa, senalfa, z = tof.best_side('E','O')
            side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')
            if avg > 60 and avg2 > 60:
                break
            if avg2 < avg and avg2 != -1:
                side = side2
                cosalfa = cosalfa2
                senalfa = senalfa2
                avg = avg2
                z = z2
            all_m = [None, None, None, None, None, None, None, None, None, None]
            time_start = time.time()
            while True:
                if time.time()-time_start < 2 and slow:
                    break
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

                self.setSpeeds((50-slow*20)*z, -(50-slow*20)*z)
            gyro.update()
            if abs(good_angle-gyro.yawsum) > 10:
                self.set_degrees(gyro,good_angle)

        '''
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
        self.posiziona_assi(gyro)

        self.stop()

    def posiziona_assi(self, gyro):
        gyro.update()
        starting_deg = gyro.starting_deg
        starting_deg = starting_deg % 90
        now = gyro.yawsum % 90
        if abs(starting_deg-now) <=45:
            to_rotate = starting_deg-now
        else:
            to_rotate = (starting_deg-now)%90
        self.rotateDegrees(gyro, to_rotate)

    def fora_parallel(self, senalfa_prec, tof=None):
            while True:
                side, avg, cosalfa, senalfa,s_dif, z = tof.best_side('E','O')
                side2, avg2, cosalfa2, senalfa2,s_dif2, z2 = tof.best_side('N','S')

                if avg2 < avg and avg2 != -1:
                    side = side2
                    cosalfa = cosalfa2
                    senalfa = senalfa2
                    avg = avg2
                    z = z2

                if s_dif<=2 and s_dif2<=2:
                    senalfa = math.sin(math.radius(senalfa))
                error = z * senalfa
                correzione = pid.get_pid(params.PID_p_ROTATION, params.PID_i_ROTATION, params.PID_d_ROTATION, error = error)
                self.setSpeeds(-MOTOR_DEFAULT_POWER_ROTATION*correzione, MOTOR_DEFAULT_POWER_ROTATION*correzione)
                if senalfa <= params.ERROR_SENALFA and senalfa>= -params.ERROR_SENALFA:
                    break

            self.stop()
    """
    Here start the simple functions for robot motion execution
    """
    def oneCellForward(self, power= MOTOR_DEFAULT_POWER_LINEAR, wait= MOTOR_CELL_TIME, mode= 'time', ch=None, tof= None, gyro=None, h=None, k = None, mat = None, pos = None, deg_pos=None):
        logging.info("Going one cell forward")
        if mode == 'time':
            avg = now
            logging.debug("Going by time")
            self.setSpeeds(power, power)
            time.sleep(wait)

        elif mode == 'gyro':
            logging.debug("Going by gyro")
            self.setSpeeds(power, power)
            north = tof.read_fix('N')[0]
            south = tof.read_fix('S')[0]
            now_north = north
            now_south = south
            gyro.update()
            deg = gyro.yawsum
            boost = 0
            a_tempo = False

            avg_e = tof.read_fix('E')[0]
            avg_o = tof.read_fix('O')[0]

            if avg_e < 20:
                logging.info("Disincagna TOF E")
                self.disincagna(gyro, -1, largo=0)
                #self.parallel(tof,times =2, gyro=gyro, deg=deg_pos)
            elif avg_o < 20:
                logging.info("Disincagna TOF O")
                self.disincagna(gyro, 1, largo=0)
                #self.parallel(tof,times =2, gyro=gyro, deg=deg_pos)

            if not a_tempo:
                started_time = time.time()
                while True:
                    side1, avg1, cosalfa1, senalfa1, z1 = tof.best_side('E','O')
                    side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')
                    #print("Cell difference", (now,front))
                    victims = sm.check_victim(pos,h)
                    print("Victims, ", victims)
                    if (victims[0]): #and time.time()-h.last_read>5):
                        time_before_victims = time.time()
                        if mat.item(pos)//512 == 1; #If i've seen the victims but not the visual
                            mat.itemset(pos, 1024)
                            self.saveAllVictims(gyro, victims, k)
                        else if mat.item(pos)//512 == 0: #First time i see victims here
                            mat.itemset(pos, 512)
                            self.saveAllVictims(gyro, victims, k)
                        #self.setSpeeds(50,50)
                        #time.sleep(0.2)
                        #self.stop()
                        h.last_read = time.time()
                        started_time += time.time() - time_before_victims
                    avg = tof.read_fix('N')[0]
                    if gyro.pitch < 20 and gyro.pitch > -20:
                        time_passed = time.time()-started_time
                        if  (now_north != -1 and north != -1 and north < 900 and north-now_north > dim.cell_dimension) or (now_south != -1 and south != -1 and south < 900 and now_south-south > dim.cell_dimension) and time_passed > MOTOR_MIN_CELL_TIME:
                            now_north = tof.read_fix('N')[0]
                            now_south = tof.read_fix('S')[0]
                            if  (now_north != -1 and north != -1 and north < 900 and north-now_north > dim.cell_dimension) or (now_south != -1 and south != -1 and south < 900 and now_south-south > dim.cell_dimension) and time_passed > MOTOR_MIN_CELL_TIME:
                                print("Tof has recorded cell difference")
                                print(north,now_north)
                                print(south,now_south)
                                break
                        if avg < 100 and avg != -1:
                            print("Front avg recorded wall")
                            break
                        if not time.time()-started_time < MOTOR_CELL_TIME:
                            print("Max time passed")
                            break
                        now_north = tof.read_fix('N')[0]
                        now_south = tof.read_fix('S')[0]

                    if ch.is_something_touched():
                        time.sleep(0.3)
                        if ch.read('E') and ch.read('O'):
                            break
                        time_before_victims = time.time()
                        if ch.read('E'):
                            self.disincagna(gyro, -1, deg)
                        else:
                            self.disincagna(gyro, 1, deg)
                        started_time += time.time() - time_before_victims

                    gyro.update()
                    correction = deg - gyro.yawsum

                    if gyro.pitch > 18:
                        self.setSpeeds(-30,-30)
                        time.sleep(1)
                        self.setSpeeds(70,70)
                        time.sleep(0.6)
                        gyro.update()
                        while(gyro.pitch > 18):
                            self.setSpeeds(70 + gyro.roll, 70 - gyro.roll)
                            gyro.update()
                    if gyro.pitch < -6:
                        self.setSpeeds(40,40)
                        time.sleep(0.05)
                        self.setSpeeds(30,30)
                        time.sleep(0.05)
                        self.setSpeeds(22,22)
                        time.sleep(0.05)
                        self.setSpeeds(18,18)
                        time.sleep(0.05)
                        self.setSpeeds(15,15)
                        time.sleep(0.1)
                        gyro.update()
                        while(gyro.pitch < -6):
                            gyro.update()
                            self.setSpeeds(25 - gyro.roll, 25 + gyro.roll)

                    self.setSpeeds(power - correction, power + correction )
            else:
                self.setSpeeds(MOTOR_DEFAULT_POWER_LINEAR, MOTOR_DEFAULT_POWER_LINEAR)
                time.sleep(MOTOR_CELL_TIME)
                self.stop()




        elif mode == 'tof_fixed':

            #### now it should be a wall follower
            side, avg, cosalfa, senalfa, s_div, z = tof.best_side('E','O')
            side2, avg2, cosalfa2, senalfa2, s_div2, z2 = tof.best_side('N','S') #Find the mostaccurate side
            gyro.update()
            deg=gyro.yawsum

            if avg2 < avg and avg2 != -1:
                cosalfa = cosalfa2
                senalfa = senalfa2

            if s_div2 < 2 and s_div < 2:
                time.sleep(0.05)
                gyro.update()
                grad=gyro.yawsum
                cosalfa = math.cos(math.radians(deg-grad))

            N_prec = tof.n_cells(avg2, cosalfa, k = dim.cell_long)*z2 #N_cells before the movement
            N_now = N_prec
            x=0

            #while (True):
            while(N_prec >= N_now): #While the number of cells is not changed
                print("N", N_prec, N_now)
                side, avg, cosalfa, senalfa, s_div, z = tof.best_side('E','O')
                avg2, cosalfa2, senalfa2, s_div2 = tof.read_fix(side2)


                if avg2 < avg and s_div2==3:
                    cosalfa = cosalfa2
                    senalfa = senalfa2

                if s_div2 <= 2 and s_div <= 2:
                    gyro.update()
                    grad=gyro.yawsum
                    cosalfa = math.cos(math.radians(deg-grad))



                error=tof.error(avg, cosalfa, z)


                if error != None:
                    correction = pid.get_pid(error)

                else:
                    correction = 0

                self.setSpeeds(power*(1+correction),power*(1-correction))

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

                #Ramp
                gyro.update()
                if gyro.pitch > 18: #Up
                    self.setSpeeds(-30,-30)
                    time.sleep(1)
                    self.setSpeeds(70,70)
                    time.sleep(0.6)
                    gyro.update()
                    while(gyro.pitch > 18):
                        self.setSpeeds(70 + gyro.roll, 70 - gyro.roll)
                        gyro.update()
                    time.sleep(0.2)
                    self.stop()
                    break
                if gyro.pitch < -6: #Down
                    self.setSpeeds(40,40)
                    time.sleep(0.05)
                    self.setSpeeds(30,30)
                    time.sleep(0.05)
                    self.setSpeeds(22,22)
                    time.sleep(0.05)
                    self.setSpeeds(18,18)
                    time.sleep(0.05)
                    self.setSpeeds(15,15)
                    time.sleep(0.1)
                    gyro.update()
                    while(gyro.pitch < -6):
                        gyro.update()
                        self.setSpeeds(25 - gyro.roll, 25 + gyro.roll)
                    time.sleep(1)
                    self.stop()
                    break

                #Check victims
                victims = sm.check_victim(pos,h)
                print("Victims: ", victims)
                if (victims[0]): #and time.time()-h.last_read>5):
                    time_before_victims = time.time()
                    if mat.item(pos)//512 == 1 and sm.are_there_visual_victims_in_the_list(victims[1]); #If i've seen the victims but not the visual (at least not all of them)
                        mat.itemset(pos, 1024, only_visual == True)
                        self.saveAllVictims(gyro, victims, k)
                    else if mat.item(pos)//512 == 0: #First time i see victims here
                        mat.itemset(pos, 512)
                        self.saveAllVictims(gyro, victims, k)

                N_now = z2*tof.n_cells(avg2, cosalfa, k=dim.cell_long)
            self.parallel(tof, gyro=gyro)

        logging.info("Arrived in centre of the cell")
        self.stop()
        return mat


    def saveAllVictims(self, gyro, victims, k, only_visual = False):
        self.stop()
        turn = 1
        if 'N' in victims[1] and not only_visual:
            k.release_one_kit()
        if 'E' in victims[1]  and not only_visual) or 'HE' in victims[1] or 'SE' in victims[1] or 'UE' in victims[1]:
            for i in range(turn):
                self.rotateRight(gyro)
            if 'E' in victims[1] or 'HE' in victims[1] or 'SE' in victims[1]:
                k.release_one_kit()
                if 'HE' in victims[1]:
                    k.release_one_kit()
            else:
                k.blink()
            turn = 1
        else:
            turn += 1
        if 'S' in victims[1]  and not only_visual:
            for i in range(turn):
                self.rotateRight(gyro)
            k.release_one_kit()
            turn = 1
        else:
            turn += 1
        if ('O' in victims[1]  and not only_visual) or 'HO' in victims[1] or 'SO' in victims[1] or 'UO' in victims[1]:
            if turn != 3:
                for i in range(turn):
                    self.rotateRight(gyro)
            else:
                self.rotateLeft(gyro)
            if 'O' in victims[1] or 'HO' in victims[1] or 'SO' in victims[1]:
                k.release_one_kit()
                if 'HO' in victims[1]:
                    k.release_one_kit()
            else:
                k.blink()
            turn = 1
        else:
            turn += 1

        if(turn < 4):
            for i in range(turn):
                self.rotateRight(gyro)



    def oneCellBack(self, power= MOTOR_DEFAULT_POWER_LINEAR, wait= MOTOR_CELL_TIME):
        self.setSpeeds(-50, -50)
        time.sleep(1.2)
        self.stop()

    def rotateRight(self, gyro, power= MOTOR_DEFAULT_POWER_ROTATION, wait= MOTOR_ROTATION_TIME):
        self.rotateDegrees(gyro=gyro, degrees=-90)

        self.parallel(gyro)
        self.stop()

    def rotateLeft(self, gyro, power= MOTOR_DEFAULT_POWER_ROTATION, wait= MOTOR_ROTATION_TIME):
        self.rotateDegrees(gyro=gyro, degrees=90)

        self.parallel(gyro)
        self.stop()

    def rotateDegrees(self, gyro, degrees):
        now = gyro.update().yawsum
        if degrees > 0:
            self.setSpeeds(-60,60)
            while(gyro.update().yawsum <= now+degrees-5):
                pass

            start = time.time()
            self.setSpeeds(-30,30)
            while(gyro.update().yawsum <= now+degrees-2 and time.time()-start > 3):
                pass
        else:
            self.setSpeeds(60,-60)
            while(gyro.update().yawsum >= now+degrees+5):
                pass

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
        diff = (now-degrees)%360
        self.rotateDegrees(gyro, -diff)


    def disincagna(self, gyro, dir, deg = None, largo = True): #Best name everf
        pass
        '''
        to_do = 20
        if largo:
            to_do = 30
        dir_lib = {1:'O', -1:'E'}
        logging.debug('Disincagna %s', dir_lib[dir])
        if largo:
            self.setSpeeds(-20,-20)
            time.sleep(0.4)
        self.rotateDegrees(gyro, to_do*dir)
        self.setSpeeds(-20, -20)
        time.sleep(1)
        self.rotateDegrees(gyro, -(2*to_do)*dir)

        self.setSpeeds(20, 20)
        time.sleep(0.8)

        if deg != None:
            self.set_degrees(gyro, deg)
        else:
            self.rotateDegrees(gyro, to_do*dir)
        if largo:
            self.setSpeeds(20,20)
        time.sleep(0.4)
        '''
