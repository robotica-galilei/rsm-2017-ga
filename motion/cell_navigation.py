import sys
sys.path.append("../")
import time
import logging
import math

import actuators.motors as motors
import config.params as params
import config.dimensions as dim
import motors_pid as pid
import sensors.sensors_handler as sm


def rotateRight(m, gyro, power= motors.MOTOR_DEFAULT_POWER_ROTATION, wait= motors.MOTOR_ROTATION_TIME):
    rotateDegrees(m, gyro=gyro, degrees=-90)

    parallel(m, gyro=gyro)
    m.stop()


def rotateLeft(m, gyro, power= motors.MOTOR_DEFAULT_POWER_ROTATION, wait= motors.MOTOR_ROTATION_TIME):
    rotateDegrees(m, gyro=gyro, degrees=90)

    parallel(m, gyro=gyro)
    m.stop()


def rotateDegrees(m, gyro, degrees):
    now = gyro.update().yawsum
    if degrees > 1:
        m.setSpeeds(-60,60)
        while(gyro.update().yawsum <= now+degrees-5):
            pass

        start = time.time()
        m.setSpeeds(-30,30)
        while(gyro.update().yawsum <= now+degrees-2 and time.time()-start > 3):
            pass
    elif degrees < -1:
        m.setSpeeds(60,-60)
        while(gyro.update().yawsum >= now+degrees+5):
            pass

        m.setSpeeds(30,-30)
        start = time.time()
        while gyro.update().yawsum >= now+degrees+2 and time.time()-start > 3:
            pass
    m.stop()

    """
    if
    """


def set_degrees(m, gyro, degrees):
    now = gyro.update().yawsum
    diff = (now-degrees)%360
    rotateDegrees(m, gyro, -diff)


def disincagna(m, gyro, dir, deg = None, largo = True): #Best name everf

    to_do = 20
    if largo:
        to_do = 30
    dir_lib = {1:'O', -1:'E'}
    logging.debug('Disincagna %s', dir_lib[dir])
    if largo:
        m.setSpeeds(-20,-20)
        time.sleep(0.4)
    posiziona_assi(m, gyro)
    rotateDegrees(m, gyro, to_do*dir)
    m.setSpeeds(-20, -20)
    time.sleep(1)
    rotateDegrees(m, gyro, -(2*to_do)*dir)

    m.setSpeeds(20, 20)
    time.sleep(0.8)

    if deg != None and False:
        set_degrees(m, gyro, deg)
    else:
        rotateDegrees(m, gyro, to_do*dir)
    if largo:
        m.setSpeeds(20,20)
    time.sleep(0.4)


def parallel(m, tof = None, times = 1, gyro = None, deg = None, slow = False):
    '''
    if deg!= None:
        m.set_degrees(gyro, deg)
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

            m.setSpeeds((50-slow*20)*z, -(50-slow*20)*z)
        gyro.update()
        if abs(good_angle-gyro.yawsum) > 10:
            set_degrees(gyro,good_angle)

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
        m.setSpeeds(-40*error, 40*error)
        if senalfa <= params.ERROR_SENALFA and senalfa>= -params.ERROR_SENALFA:
            break
    '''
    posiziona_assi(m, gyro)

    m.stop()


def posiziona_assi(m, gyro):
    gyro.update()
    starting_deg = gyro.starting_deg
    starting_deg = starting_deg % 90
    now = gyro.yawsum % 90
    if abs(starting_deg-now) <=45:
        to_rotate = starting_deg-now
    else:
        to_rotate = (starting_deg-now)%90
    if abs(to_rotate) > 1:
        rotateDegrees(m, gyro, to_rotate)



"""
Here start the simple functions for robot motion execution
"""
def oneCellForward(m, power= motors.MOTOR_DEFAULT_POWER_LINEAR, wait= motors.MOTOR_CELL_TIME, mode= 'time', ch=None, tof= None, gyro=None, h=None, k_kit = None, mat = None, pos = None, new_pos = None, deg_pos=None):
    logging.info("Going one cell forward")

    if mode == 'wall':
        m.setSpeeds(power,power)
        while(tof.read_raw('N') > 90):
            for i in range(4):
                tof.read_raw('S')

    elif mode == 'time':
        print("Sto per partire")
        started_time = time.time()
        gyro.update()
        starting_deg = gyro.yawsum
        while time.time()-started_time < motors.MOTOR_CELL_TIME: #or (avg2 >= dim.MIN_DISTANCE): #While the number of cells is not changed or the distance from a wall is too low
            m.setSpeeds(motors.MOTOR_DEFAULT_POWER_LINEAR,motors.MOTOR_DEFAULT_POWER_LINEAR)
            gyro.update()
            if(abs(starting_deg-gyro.yawsum) > 10):
                #Got stuck
                if(starting_deg-gyro.yawsum > 0):
                    disincagna(m, gyro, -1, deg= starting_deg)
                else:
                    disincagna(m, gyro, 1, deg= starting_deg)
                first_slow_down = True
                parallel(m, tof, gyro=gyro)
                starting_deg = gyro.yawsum
                started_time = time.time() - 0.2
            '''
            gyro.update()
            if gyro.pitch > 18: #Up
                m.setSpeeds(-30,-30)
                time.sleep(1)
                m.setSpeeds(70,70)
                time.sleep(0.6)
                gyro.update()
                while(gyro.pitch > 18):
                    m.setSpeeds(70 + gyro.roll, 70 - gyro.roll)
                    gyro.update()
                time.sleep(0.2)
                m.stop()
                break
            if gyro.pitch < -6: #Down
                m.setSpeeds(40,40)
                time.sleep(0.05)
                m.setSpeeds(30,30)
                time.sleep(0.05)
                m.setSpeeds(22,22)
                time.sleep(0.05)
                m.setSpeeds(18,18)
                time.sleep(0.05)
                m.setSpeeds(15,15)
                time.sleep(0.1)
                gyro.update()
                while(gyro.pitch < -6):
                    gyro.update()
                    m.setSpeeds(25 - gyro.roll, 25 + gyro.roll)
                time.sleep(1)
                m.stop()
                break
            victims = sm.check_victim(pos,h)
            print("Victims: ", victims)
            if (victims[0]): #and time.time()-h.last_read>5):
                time_before_victims = time.time()
                if mat.item(pos)//512 == 1 and sm.are_there_visual_victims_in_the_list(victims[1]): #If i've seen the victims but not the visual (at least not all of them)
                    mat.itemset(pos, 1024, only_visual = True)
                    saveAllVictims(m, gyro, victims, k, tof)
                elif mat.item(pos)//512 == 0: #First time i see victims here
                    mat.itemset(pos, 512)
                    saveAllVictims(m, gyro, victims, k, tof)

            if ch.is_something_touched():
                if ch.read('E'):
                    m.setSpeeds(70,30)
                else:
                    m.setSpeeds(30,70)
                time.sleep(0.2)
                if ch.read('E') and ch.read('O'):
                    gyro.update()
                    gyro.starting_deg = gyro.yawsum
                    break
                    print("Letti tutti")
                elif ch.read('E'):
                    disincagna(m, gyro, -1, deg)
                else:
                    disincagna(m, gyro, 1, deg)

            N_now = z2*tof.n_cells(avg2, cosalfa, k=dim.cell_long)
            '''
            pass
        print("Ho finito il ciclo, merde")
        parallel(m, tof, gyro=gyro)

    elif mode == 'gyro':
        logging.debug("Going by gyro")
        m.setSpeeds(power, power)
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
            #disincagna(m, gyro, -1, largo=0)
            #parallel(m, tof,times =2, gyro=gyro, deg=deg_pos)
        elif avg_o < 20:
            logging.info("Disincagna TOF O")
            #disincagna(m, gyro, 1, largo=0)
            #parallel(m, tof,times =2, gyro=gyro, deg=deg_pos)

        if not a_tempo:
            started_time = time.time()
            while True:
                #side1, avg1, cosalfa1, senalfa1, z1 = tof.best_side('E','O')
                #side2, avg2, cosalfa2, senalfa2, z2 = tof.best_side('N','S')
                #print("Cell difference", (now,front))
                victims = sm.check_victim(pos,h)
                print("Victims, ", victims)
                if (victims[0]): #and time.time()-h.last_read>5):
                    time_before_victims = time.time()
                    if mat.item(pos)//512 == 1: #If i've seen the victims but not the visual
                        mat.itemset(pos, 1024)
                        saveAllVictims(m, gyro, victims, k, tof)
                    elif mat.item(pos)//512 == 0: #First time i see victims here
                        mat.itemset(pos, 512)
                        saveAllVictims(m, gyro, victims, k, tof)
                    #m.setSpeeds(50,50)
                    #time.sleep(0.2)
                    #m.stop()
                    h.last_read = time.time()
                    started_time += time.time() - time_before_victims
                avg = tof.read_fix('N')[0]
                if gyro.pitch < 20 and gyro.pitch > -20:
                    time_passed = time.time()-started_time
                    if  (now_north != -1 and north != -1 and north < 900 and north-now_north > dim.cell_dimension_gyro) or (now_south != -1 and south != -1 and south < 900 and now_south-south > dim.cell_dimension_gyro) and time_passed > motors.MOTOR_MIN_CELL_TIME:
                        now_north = tof.read_fix('N')[0]
                        now_south = tof.read_fix('S')[0]
                        if  (now_north != -1 and north != -1 and north < 900 and north-now_north > dim.cell_dimension_gyro) or (now_south != -1 and south != -1 and south < 900 and now_south-south > dim.cell_dimension_gyro) and time_passed > motors.MOTOR_MIN_CELL_TIME:
                            print("Tof has recorded cell difference")
                            print(north,now_north)
                            print(south,now_south)
                            break
                    if avg < 100 and avg != -1:
                        print("Front avg recorded wall")
                        break
                    if not time.time()-started_time < motors.MOTOR_CELL_TIME:
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
                        disincagna(m, gyro, -1, deg)
                    else:
                        disincagna(m, gyro, 1, deg)
                    started_time += time.time() - time_before_victims

                gyro.update()
                correction = deg - gyro.yawsum

                if gyro.pitch > 18:
                    m.setSpeeds(-30,-30)
                    time.sleep(1)
                    m.setSpeeds(70,70)
                    time.sleep(0.6)
                    gyro.update()
                    while(gyro.pitch > 18):
                        m.setSpeeds(70 + gyro.roll, 70 - gyro.roll)
                        gyro.update()
                if gyro.pitch < -6:
                    m.setSpeeds(40,40)
                    time.sleep(0.05)
                    m.setSpeeds(30,30)
                    time.sleep(0.05)
                    m.setSpeeds(22,22)
                    time.sleep(0.05)
                    m.setSpeeds(18,18)
                    time.sleep(0.05)
                    m.setSpeeds(15,15)
                    time.sleep(0.1)
                    gyro.update()
                    while(gyro.pitch < -6):
                        gyro.update()
                        m.setSpeeds(25 - gyro.roll, 25 + gyro.roll)

                m.setSpeeds(power - correction, power + correction )
        else:
            m.setSpeeds(motors.MOTOR_DEFAULT_POWER_LINEAR, motors.MOTOR_DEFAULT_POWER_LINEAR)
            time.sleep(motors.MOTOR_CELL_TIME)
            m.stop()

    elif mode == 'new_tof':
        precision = 15
        side, avg, k = tof.best_side('N','S') #Find the most accurate side between front and rear
        if (side == 'S' and (avg == -1 or avg > 600)) or (side == 'N' and avg == -1):
            oneCellForward(m, mode='time', gyro=gyro)
        else:
            N_prec = tof.n_cells_avg(avg) #N_cells before the movement
            N_now = N_prec
            is_in_center = tof.is_in_cell_center(avg, precision = precision)
            side_c, avg_c, k_c = tof.best_side('E','O') #Find the most accurate side between right and left to calculate the correction
            correction = dim.cell_dimension/2 - avg_c - ((tof.n_cells_avg(avg_c)-1)*dim.cell_dimension + dim.robot_width/2)
            correction *= 0.05
            if correction > 2:
                correction = 2
            elif correction < -2:
                correction = -2
            rotateDegrees(m, gyro, -correction*k_c)
            gyro.update()
            starting_deg = gyro.yawsum
            first_slow_down = True
            avg_N = tof.read_fix('N')
            avg_N_prec = avg_N
            started_slow = 0
            started_time = time.time()
            print("Moving using %s", side)
            while ((((N_now == N_prec or not is_in_center) and abs(tof.n_cells_avg(avg+k*(dim.cell_dimension/2-precision))- N_prec) <= 1 )  or (side == 'N' and avg_N > 35 and avg_N_prec < 450)) and (avg_N > 30 or avg_N == -1) or time.time()-started_time < 0.8) and time.time()-started_time < 6:
                #print(N_now, N_prec, abs(tof.n_cells_avg(avg+k*(dim.cell_dimension/2-precision))- N_prec))
                if N_now != N_prec and (time.time()-started_slow < 3 or started_slow == 0):
                    m.setSpeeds(motors.MOTOR_PRECISION_POWER_LINEAR, motors.MOTOR_PRECISION_POWER_LINEAR)
                    if first_slow_down:
                        parallel(m, tof, gyro=gyro)
                        starting_deg = gyro.yawsum
                        started_slow = time.time()
                        first_slow_down = False
                elif time.time()-started_slow < 3 or started_slow == 0:
                    m.setSpeeds(motors.MOTOR_DEFAULT_POWER_LINEAR, motors.MOTOR_DEFAULT_POWER_LINEAR)
                else:
                    m.setSpeeds(-60, -60)
                    time.sleep(0.4)
                    m.setSpeeds(80,80)
                    time.sleep(0.65)
                    started_slow = 0

                gyro.update()
                if(abs(starting_deg-gyro.yawsum) > 10):
                    #Got stuck
                    if(starting_deg-gyro.yawsum > 0):
                        disincagna(m, gyro, -1, deg= starting_deg)
                        started_time = time.time()
                        started_slow = 0
                    else:
                        disincagna(m, gyro, 1, deg= starting_deg)
                        started_time = time.time()
                        started_slow = 0
                    first_slow_down = True
                    parallel(m, tof, gyro=gyro)
                    starting_deg = gyro.yawsum

                avg = tof.read_fix(side)
                avg_N = tof.read_fix('N')
                #print('C: ', correction)
                N_now = tof.n_cells_avg(avg)
                is_in_center = tof.is_in_cell_center(avg, precision = precision)
                #print('N: ', N_prec, N_now)

                if gyro.pitch < -12: #Up
                    m.setSpeeds(-30,-30)
                    time.sleep(1)
                    m.setSpeeds(70,70)
                    time.sleep(0.6)
                    gyro.update()
                    while(gyro.pitch < -12):
                        side_c, avg_c, k_c = tof.best_side('E','O') #Find the most accurate side between right and left to calculate the correction
                        correction = dim.cell_dimension/2 - avg_c - ((tof.n_cells_avg(avg_c)-1)*dim.cell_dimension + dim.robot_width/2)
                        correction *= 0.1
                        if correction > 2:
                            correction = 2
                        elif correction < -2:
                            correction = -2
                        m.setSpeeds(65 - gyro.roll + correction*k_c, 65 + gyro.roll - correction*k_c, l_coeff = 20, r_coeff = 20)
                        gyro.update()
                    m.setSpeeds(50,50)
                    time.sleep(0.4)
                    started_time = time.time()
                    started_slow = 0
                if gyro.pitch > 8: #Down
                    m.setSpeeds(40,40, l_coeff = -20, r_coeff = -20)
                    time.sleep(0.05)
                    m.setSpeeds(30,30, l_coeff = -10, r_coeff = -10)
                    time.sleep(0.05)
                    m.setSpeeds(22,22, l_coeff = -7, r_coeff = -7)
                    time.sleep(0.05)
                    m.setSpeeds(18,18, l_coeff = -5, r_coeff = -5)
                    time.sleep(0.05)
                    m.setSpeeds(15,15, l_coeff = -3, r_coeff = -3)
                    time.sleep(0.1)
                    m.setSpeeds(30,30, l_coeff = -5, r_coeff = -5)
                    time.sleep(0.1)
                    gyro.update()
                    while(gyro.pitch > 8):
                        gyro.update()
                        side_c, avg_c, k_c = tof.best_side('E','O') #Find the most accurate side between right and left to calculate the correction
                        correction = dim.cell_dimension/2 - avg_c - ((tof.n_cells_avg(avg_c)-1)*dim.cell_dimension + dim.robot_width/2)
                        correction *= 0.1
                        if correction > 2:
                            correction = 2
                        elif correction < -2:
                            correction = -2
                        m.setSpeeds(35 + gyro.roll + correction*k_c, 35 - gyro.roll - correction*k_c)
                        print("ROLL: ",  gyro.roll)
                        print("CORR: ", correction*k_c)
                    m.setSpeeds(40,40)
                    time.sleep(0.5)
                    started_time = time.time()
                    started_slow = 0

            print(N_now, N_prec, abs(tof.n_cells_avg(avg+(dim.cell_dimension/2-precision))- N_prec))
            parallel(m, tof, gyro=gyro)
        victims = sm.check_victim(h)
        print("HeatVictims: ", h.isThereSomeVictim())
        print("VideoVictims: ", h.isThereSomeVideoVictim())
        print("Time passed: ", time.time() - h.last_victim)
        print("Last saved passed: ", time.time() - h.last_saved)
        #saveAllVictims(m, gyro, h.isThereSomeVideoVictim, k_kit, tof)
        if (time.time() - h.last_victim < 0.8 and time.time() - h.last_saved > 1.2): #and time.time()-h.last_read>5):
            print("SAVING")
            time_before_victims = time.time()
            saveAllVictims(m, gyro, h.victims, k_kit, tof)
            h.last_saved = time.time()
            '''
            if mat.item(pos)//512 == 1: #If i've seen the victims but not the visual
                #mat.itemset(pos, 1024)
                saveAllVictims(m, gyro, victims, k, tof)
            elif mat.item(pos)//512 == 0: #First time i see victims here
                #mat.itemset(pos, 512)
                saveAllVictims(m, gyro, victims, k, tof)
            '''
        elif h.last_victim - h.last_saved > 2 and time.time() - h.last_victim < 2.1:
            oneCellBack(m, mode='time')
            saveAllVictims(m, gyro, h.victims, k_kit, tof)
            k_kit.blink()
            time.sleep(1)
            oneCellForward(m, mode='time', gyro=gyro)

        saveAllVictims(m, gyro, h.isThereSomeVideoVictim(), k_kit, tof)

    logging.info("Arrived in centre of the cell")
    m.stop()
    time.sleep(0.3)
    return mat

def saveAllVictims(m, gyro, victims, k, tof, only_visual = False):
    m.stop()

    turn = 1

    if 'N' in victims[1] and not only_visual and tof.is_there_a_wall('N'):
        k.release_one_kit()
    if 'UE' in victims[1] or 'UO' in victims[1]:
        k.blink()
        time.sleep(1)
    if (('E' in victims[1]  and not only_visual) or 'HE' in victims[1] or 'SE' in victims[1]) and tof.is_there_a_wall('E'):
        for i in range(turn):
            rotateRight(m, gyro)
        if 'E' in victims[1] or 'HE' in victims[1] or 'SE' in victims[1]:
            k.release_one_kit()
            if 'HE' in victims[1]:
                time.sleep(1)
                k.release_one_kit()
        else:
            k.blink()
        turn = 1
    else:
        turn += 1
    if 'S' in victims[1]  and not only_visual and tof.is_there_a_wall('S'):
        for i in range(turn):
            rotateRight(m, gyro)
        k.release_one_kit()
        turn = 1
    else:
        turn += 1
    if (('O' in victims[1]  and not only_visual) or 'HO' in victims[1] or 'SO' in victims[1]) and tof.is_there_a_wall('O'):
        if turn != 3:
            for i in range(turn):
                rotateRight(m, gyro)
        else:
            rotateLeft(m, gyro)
        if 'O' in victims[1] or 'HO' in victims[1] or 'SO' in victims[1]:
            k.release_one_kit()
            if 'HO' in victims[1]:
                time.sleep(1)
                k.release_one_kit()
        else:
            k.blink()
        turn = 1
    else:
        turn += 1

    if(turn < 4):
        for i in range(turn):
            rotateRight(m, gyro)


def oneCellBack(m, mode= 'time', power= motors.MOTOR_DEFAULT_POWER_LINEAR, wait= motors.MOTOR_CELL_TIME, tof=None):
    if mode == 'wall':
        m.setSpeeds(-power,-power)
        while(tof.read_raw('S') > 90):
            for i in range(4):
                tof.read_raw('S')
    elif mode == 'time':
        m.setSpeeds(-50, -50)
        time.sleep(1.2)
    m.stop()


def calibrate_gyro(m, gyro= None):
    m.setSpeeds(-50,-50)
    time.sleep(0.7)
    m.setSpeeds(10,-70)
    time.sleep(0.2)
    m.setSpeeds(-70,10)
    time.sleep(0.2)
    m.setSpeeds(-20,-70)
    time.sleep(0.2)
    m.setSpeeds(-70,-20)
    time.sleep(0.2)
    m.setSpeeds(-50,-50)
    time.sleep(0.2)
    m.stop()

    gyro.update()
    gyro.starting_deg = gyro.yawsum

    m.setSpeeds(30,30)
    time.sleep(0.5)
    parallel(m, gyro=gyro)
