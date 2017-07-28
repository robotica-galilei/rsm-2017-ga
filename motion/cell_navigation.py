import sys
sys.path.append("../")
import time
import rospy
import config.params as params
import config.dimensions as dim
import sensors.sensors_handler as sm


def rotateRight(m, gyro, power= params.MOTOR_DEFAULT_POWER_ROTATION, wait= params.MOTOR_ROTATION_TIME):
    rotateDegrees(m, gyro=gyro, degrees=-90)

    parallel(m, gyro=gyro)
    m.stop()


def rotateLeft(m, gyro, power= params.MOTOR_DEFAULT_POWER_ROTATION, wait= params.MOTOR_ROTATION_TIME):
    rotateDegrees(m, gyro=gyro, degrees=90)

    parallel(m, gyro=gyro)
    m.stop()


def rotateDegrees(m, gyro, degrees):
    now = gyro.get_yawsum()
    if degrees > 1:
        m.setSpeeds(-80,80)
        time.sleep(0.005)
        if degrees > 7:
            while gyro.get_yawsum() <= now+degrees-7:
                pass

        m.setSpeeds(-40,40)
        start = time.time()
        while gyro.get_yawsum() <= now+degrees-4 and time.time()-start < 0.7:
            pass

        start = time.time()
        m.setSpeeds(-30,30)
        while(gyro.get_yawsum() <= now+degrees-1 and time.time()-start < 0.3):
            pass
    elif degrees < -1:
        m.setSpeeds(80,-80)
        time.sleep(0.005)
        if degrees < -7:
            while gyro.get_yawsum() >= now+degrees+7:
                pass

        m.setSpeeds(40,-40)
        start = time.time()
        while gyro.get_yawsum() >= now+degrees+4 and time.time()-start < 0.7:
            pass

        m.setSpeeds(30,-30)
        start = time.time()
        while gyro.get_yawsum() >= now+degrees+1 and time.time()-start < 0.3:
            pass
    m.stop()


def set_degrees(m, gyro, degrees):
    now = gyro.get_yawsum()
    diff = (now-degrees)%360
    rotateDegrees(m, gyro, -diff)


def disincagna(m, gyro, dir, coeff = 1, deg = None, largo = True): #Best name everf

    to_do = round(20*coeff)

    dir_lib = {1:'O', -1:'E'}
    rospy.loginfo("LOG: Disincagna %s", dir_lib[dir])

    if largo:
        m.setSpeeds(-40,-40)
        time.sleep(0.2)
    posiziona_assi(m, gyro)
    rotateDegrees(m, gyro, to_do*dir)
    m.setSpeeds(-20, -20)
    time.sleep(0.8*coeff)
    rotateDegrees(m, gyro, -(2*to_do)*dir)

    m.setSpeeds(20, 20)
    time.sleep(0.4*coeff)

    if deg != None and False:
        set_degrees(m, gyro, deg)
    else:
        rotateDegrees(m, gyro, to_do*dir)
    if largo:
        m.setSpeeds(40,40)
        time.sleep(0.2)
    m.stop()


def parallel(m, tof = None, times = 1, gyro = None, deg = None, slow = False):
    """
    Move the robot parallel to the walls
    """
    print("Parallel")
    gyro
    before = gyro.get_yawsum()

    posiziona_assi(m, gyro)

    gyro
    after = gyro.get_yawsum()
    print("END Parallel")
    if(abs(before-after)>45):
        rospy.logfatal("LOG: WTF happened! Wrong rotation. Some shit with cosmic radiation happened")
        rospy.logfatal("LOG: %s", (before, after, gyro.starting_deg))
    m.stop()


def posiziona_assi(m, gyro):
    """
    Move the robot parallel to the walls using the gyro
    """
    starting_deg = gyro.starting_deg
    starting_deg = int(starting_deg)%90
    now = int(gyro.get_yawsum())%90
    if abs(starting_deg-now) <=45:
        to_rotate = starting_deg-now
    else:
        to_rotate = int(starting_deg-now)%90
    if to_rotate > 45:
        to_rotate -= 90
    if to_rotate < -45:
        to_rotate +=90

    if abs(to_rotate) > 1:
        rotateDegrees(m, gyro, to_rotate)



"""
Here start the simple functions for robot motion execution
"""
def oneCellForward(m, power= params.MOTOR_DEFAULT_POWER_LINEAR, wait= params.MOTOR_CELL_TIME, mode= 'time', ch=None, tof= None, gyro=None, h=None, k_kit = None, col = None, mat = None, pos = None, new_pos = None, deg_pos=None):
    rospy.loginfo("LOG: Going one cell forward")
    nav_error = False #Change to True if some navigation error happens and causes the robot to go back to previus position

    if mode == 'wall':
        m.setSpeeds(power,power)
        while(tof.read_raw('N') > 90):
            for i in range(4):
                tof.read_raw('S')

    elif mode == 'time':
        print("Sto per partire")
        started_time = time.time()
        starting_deg = gyro.get_yawsum()
        while time.time()-started_time < params.MOTOR_CELL_TIME: #or (avg2 >= dim.MIN_DISTANCE): #While the number of cells is not changed or the distance from a wall is too low
            m.setSpeeds(params.MOTOR_DEFAULT_POWER_LINEAR,params.MOTOR_DEFAULT_POWER_LINEAR)
            if(abs(starting_deg-gyro.get_yawsum()) > 5):
                rospy.loginfo("LOG: Disincagna")
                #Got stuck
                time_already_passed = time.time() - started_time
                if(starting_deg-gyro.get_yawsum() > 0):
                    disincagna(m, gyro, -1, deg= starting_deg)
                    started_time = time.time() - time_already_passed
                else:
                    disincagna(m, gyro, 1, deg= starting_deg)
                    started_time = time.time() - time_already_passed
                first_slow_down = True
                parallel(m, tof, gyro=gyro)
                starting_deg = gyro.get_yawsum()

            rospy.logdebug("LOG: Checking ramp")
            if gyro.pitch < -12: #Up
                rospy.loginfo("LOG: Ramp UP")
                m.setSpeeds(-30,-30)
                time.sleep(1)
                m.setSpeeds(70,70)
                time.sleep(0.6)
                while(gyro.pitch < -12):
                    side_c, avg_c, k_c = tof.best_side('E','O') #Find the most accurate side between right and left to calculate the correction
                    correction = dim.cell_dimension/2 - avg_c - ((tof.n_cells_avg(avg_c)-1)*dim.cell_dimension + dim.robot_width/2)
                    correction *= 0.1
                    if correction > 2:
                        correction = 2
                    elif correction < -2:
                        correction = -2
                    m.setSpeeds(65 - gyro.roll + correction*k_c, 65 + gyro.roll - correction*k_c, l_coeff = 20, r_coeff = 20)
                    gyro
                m.setSpeeds(50,50)
                time.sleep(0.4)
                started_time = time.time()
            if gyro.pitch > 8: #Down
                rospy.loginfo("LOG: Ramp Down")
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
                while(gyro.pitch > 8):
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
            rospy.logdebug("LOG: Checking Black cell")

            try: #Checking black cell
                if col.is_cell_black():
                    mat[new_pos[0]][new_pos[1]][new_pos[2]] = 256
                    nav_error = True
                    oneCellBack(m, mode='time', wait=params.MOTOR_CELL_TIME*0.8)
                    break
            except Exception as e:
                rospy.logerr("LOG: ERROR reading black cell")
                rospy.logerr(e)

            #Checking victims
            try:
                if (time.time() - h.last_victim < 0.8 and time.time() - h.last_saved > 1.2): #and time.time()-h.last_read>5):
                    time_already_passed = time.time() - started_time
                    rospy.loginfo("LOG: Saving heat victims")
                    time_before_victims = time.time()
                    saveAllVictims(m, gyro, h.victims, k_kit, tof)
                    mat[pos[0]][pos[1]][pos[2]] = 512
                    started_time = time.time() - time_already_passed
                    h.last_saved = time.time()
            except:
                pass
            rospy.logdebug("LOG: Finished cycle")
        print("Ho finito il ciclo, merde")
        parallel(m, tof, gyro=gyro)

    elif mode == 'new_tof':
        precision = 15
        side, avg, k = tof.best_side('N','S') #Find the most accurate side between front and rear
        if (side == 'S' and (avg == -1 or avg > 600)) or (side == 'N' and avg == -1):
            rospy.logdebug("LOG: Going by time")
            oneCellForward(m= m, mode= 'time', tof= tof , ch= ch, h= h, gyro= gyro, k_kit= k_kit, col=col, mat= mat, pos= pos, new_pos=new_pos, deg_pos= deg_pos)
        else:
            rospy.logdebug("LOG: Going using normal mode")
            N_prec = tof.n_cells_avg(avg) #N_cells before the movement
            N_now = N_prec
            is_in_center = tof.is_in_cell_center(avg, precision = precision)
            side_c, avg_c, k_c = tof.best_side('E','O') #Find the most accurate side between right and left to calculate the correction
            correction = dim.cell_dimension/2 - avg_c - ((tof.n_cells_avg(avg_c)-1)*dim.cell_dimension + dim.robot_width/2)
            correction *= 0.05
            if correction > 4:
                correction = 4
            elif correction < -4:
                correction = -4
            rotateDegrees(m, gyro, -correction*k_c)
            starting_deg = gyro.get_yawsum()
            first_slow_down = True
            avg_N = tof.read_fix('N')
            avg_N_prec = avg_N
            started_slow = 0
            actual_speed = 0
            prediction = 0
            started_time = time.time()
            rospy.loginfo("LOG: Moving using %s", side)


            while (time.time()-started_time < 6 and
                ((((N_now == N_prec or not is_in_center) and abs(tof.n_cells_avg(avg + prediction + k*(dim.cell_dimension/2-precision))- N_prec) <= 1 ) or
                (side == 'N' and avg_N-abs(prediction) > 65 and avg_N_prec-abs(prediction) < 450)) and (avg_N-abs(prediction) > 50 or avg_N == -1) or
                time.time()-started_time < 0.6)):

                rospy.logdebug("LOG: Calculating speed")
                #print(N_now, N_prec, abs(tof.n_cells_avg(avg+k*(dim.cell_dimension/2-precision))- N_prec))
                if N_now != N_prec and (time.time()-started_slow < 4 or started_slow == 0):
                    m.setSpeeds(params.MOTOR_PRECISION_POWER_LINEAR, params.MOTOR_PRECISION_POWER_LINEAR)
                    actual_speed = params.MOTOR_PRECISION_POWER_LINEAR
                    if first_slow_down:
                        #parallel(m, tof, gyro=gyro)
                        starting_deg = gyro.get_yawsum()
                        started_slow = time.time()
                        first_slow_down = False
                elif time.time()-started_slow < 3 or started_slow == 0:
                    m.setSpeeds(params.MOTOR_DEFAULT_POWER_LINEAR, params.MOTOR_DEFAULT_POWER_LINEAR)
                    actual_speed = params.MOTOR_DEFAULT_POWER_LINEAR
                else:
                    rospy.loginfo("LOG: Stuck on bumper")
                    m.setSpeeds(-60, -60)
                    time.sleep(0.4)
                    m.setSpeeds(80,80)
                    time.sleep(0.65)
                    started_slow = 0
                    m.setSpeeds(20,20)

                rospy.logdebug("LOG: Reading gyro")
                rospy.logdebug("LOG: Gyro OK")
                if(abs(starting_deg-gyro.get_yawsum()) > 10):
                    rospy.loginfo("LOG: Disincagna")
                    #Got stuck
                    if(starting_deg-gyro.get_yawsum() > 0):
                        disincagna(m, gyro, -1, deg= starting_deg)
                        started_time = time.time()
                        started_slow = 0
                    else:
                        disincagna(m, gyro, 1, deg= starting_deg)
                        started_time = time.time()
                        started_slow = 0
                    first_slow_down = True
                    parallel(m, tof, gyro=gyro)
                    starting_deg = gyro.get_yawsum()

                avg = tof.read_fix(side)
                avg_N = tof.read_fix('N')
                prediction = (time.time()-tof.last_time[side])*1000*0.005*actual_speed #0.005mm per unit per millisecond
                if side == 'N':
                    prediction *=-1
                #print('C: ', correction)
                N_now = tof.n_cells_avg(avg + prediction)
                is_in_center = tof.is_in_cell_center(avg + prediction, precision = precision)
                #print('N: ', N_prec, N_now)
                rospy.logdebug("LOG: Checking ramp")
                if gyro.pitch < -12: #Up
                    rospy.loginfo("LOG: Ramp UP")
                    m.setSpeeds(-30,-30)
                    time.sleep(1)
                    m.setSpeeds(70,70)
                    time.sleep(0.6)
                    gyro
                    while(gyro.pitch < -12):
                        side_c, avg_c, k_c = tof.best_side('E','O') #Find the most accurate side between right and left to calculate the correction
                        correction = dim.cell_dimension/2 - avg_c - ((tof.n_cells_avg(avg_c)-1)*dim.cell_dimension + dim.robot_width/2)
                        correction *= 0.1
                        if correction > 2:
                            correction = 2
                        elif correction < -2:
                            correction = -2
                        m.setSpeeds(65 - gyro.roll + correction*k_c, 65 + gyro.roll - correction*k_c, l_coeff = 20, r_coeff = 20)
                    m.setSpeeds(50,50)
                    time.sleep(0.4)
                    started_time = time.time() - 0.5
                    started_slow = 0
                if gyro.pitch > 8: #Down
                    rospy.loginfo("LOG: Ramp Down")
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
                    while(gyro.pitch > 8):
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
                    started_time = time.time()-0.5
                    started_slow = 0
                rospy.logdebug("LOG: Checking Black cell")

                try: #Checking black cell
                    if col.is_cell_black():
                        mat[new_pos[0]][new_pos[1]][new_pos[2]] = 256
                        nav_error = True
                        oneCellBack(m, mode='time', wait=params.MOTOR_CELL_TIME*0.8)
                        break
                except:
                    rospy.logerr("LOG: ERROR reading black cell")

                #Checking victims
                if (time.time() - h.last_victim < 0.8 and time.time() - h.last_saved > 1.2): #and time.time()-h.last_read>5):
                    time_already_passed = time.time() - started_time
                    rospy.loginfo("LOG: Saving heat victims")
                    time_before_victims = time.time()
                    saveAllVictims(m, gyro, h.victims, k_kit, tof)
                    mat[pos[0]][pos[1]][pos[2]] = 512
                    started_time = time.time()-time_already_passed
                    started_slow = 0
                    h.last_saved = time.time()

                rospy.logdebug("LOG: Finished cycle")


            m.stop()
            time.sleep(0.2)
            '''
            rospy.logdebug("LOG: precision test")
            rospy.logdebug("LOG: precision 50 - " + str(tof.is_in_cell_center(tof.read_fix(side), precision = 50)))
            rospy.logdebug("LOG: precision 40 - " + str(tof.is_in_cell_center(tof.read_fix(side), precision = 40)))
            rospy.logdebug("LOG: precision 30 - " + str(tof.is_in_cell_center(tof.read_fix(side), precision = 30)))
            rospy.logdebug("LOG: precision 20 - " + str(tof.is_in_cell_center(tof.read_fix(side), precision = 20)))
            rospy.logdebug("LOG: precision 10 - " + str(tof.is_in_cell_center(tof.read_fix(side), precision = 10)))
            rospy.logdebug("LOG: precision 5 - " + str(tof.is_in_cell_center(tof.read_fix(side), precision = 5)))
            '''
            side, avg, k = tof.best_side('N','S') #Find the most accurate side between front and rear
            if avg < 750 and avg != -1:
                to_step_back = 0
                for i in range(25,56,5):
                    if not tof.is_in_cell_center(avg, precision = i):
                        to_step_back = precision
                stepBack(m, 0.01*to_step_back)
                print(N_now, N_prec, abs(tof.n_cells_avg(avg+(dim.cell_dimension/2-precision))- N_prec))
                parallel(m, tof, gyro=gyro)

        if abs(gyro.get_pitch()) > 5:
            time.sleep(0.3)
        m.stop()
        #time.sleep(0.3)
        rospy.logdebug("LOG: Starting checking video victims")
        #victims = sm.check_victim(h)
        #print("HeatVictims: ", h.isThereSomeVictim())
        #print("VideoVictims: ", h.isThereSomeVideoVictim())
        #print("Time passed: ", time.time() - h.last_victim)
        #print("Last saved passed: ", time.time() - h.last_saved)
        #saveAllVictims(m, gyro, h.isThereSomeVideoVictim, k_kit, tof)

        saveAllVictims(m, gyro, h.isThereSomeVideoVictim(), k_kit, tof)

    if not nav_error:
        pos = new_pos
    return mat, pos, nav_error

def saveAllVictims(m, gyro, victims, k, tof, only_visual = False):
    m.stop()

    turn = 1
    if victims[0] == True:
        rospy.loginfo("LOG: Victims: %s", victims[1])
    if 'N' in victims[1] and not only_visual and tof.is_there_a_wall('N'):
        k.release_one_kit()
    if 'UE' in victims[1] and tof.is_there_a_wall('E') or 'UO' in victims[1] and tof.is_there_a_wall('O'):
        k.blink()
        time.sleep(0.5)
        k.blink()
        time.sleep(0.5)
        k.blink()
        time.sleep(0.5)
        k.blink()
        time.sleep(0.5)
    if (('E' in victims[1]  and not only_visual) or 'HE' in victims[1] or 'SE' in victims[1]) and tof.is_there_a_wall('E'):
        for i in range(turn):
            rotateRight(m, gyro)
        if 'E' in victims[1] or 'HE' in victims[1] or 'SE' in victims[1]:
            m.setSpeeds(-30,-30)
            time.sleep(0.2)
            m.stop()
            k.release_one_kit()
            if 'HE' in victims[1]:
                time.sleep(1)
                k.release_one_kit()
            time.sleep(0.2)
            m.setSpeeds(30,30)
            time.sleep(0.2)
            m.stop()
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
            m.setSpeeds(-30,-30)
            time.sleep(0.2)
            m.stop()
            k.release_one_kit()
            if 'HO' in victims[1]:
                time.sleep(1)
                k.release_one_kit()
            time.sleep(0.2)
            m.setSpeeds(30,30)
            time.sleep(0.2)
            m.stop()
        else:
            k.blink()
        turn = 1
    else:
        turn += 1

    if(turn == 3):
        rotateLeft(m, gyro)
    elif(turn < 4):
        for i in range(turn):
            rotateRight(m, gyro)
    if victims[0] == True:
        m.setSpeeds(40,40)
        time.sleep(0.3)
    m.stop()


def oneCellBack(m, mode= 'time', power= params.MOTOR_DEFAULT_POWER_LINEAR, wait= params.MOTOR_CELL_TIME, tof=None):
    rospy.loginfo("LOG: Going one cell backward")
    if mode == 'wall':
        m.setSpeeds(-power,-power)
        while(tof.read_raw('S') > 90):
            for i in range(4):
                tof.read_raw('S')
    elif mode == 'time':
        m.setSpeeds(-50, -50)
        time.sleep(wait)
    m.stop()

def stepBack(m, wait = 0.3):
    rospy.loginfo("LOG: StepBack alignment")
    m.setSpeeds(-30,-30)
    time.sleep(wait)
    m.stop()


def calibrate_gyro(m, gyro= None):
    rospy.loginfo("LOG: Calibrating Gyro")
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

    gyro.starting_deg = gyro.get_yawsum()
    gyro.last_calibrated = time.time()

    m.setSpeeds(30,30)
    time.sleep(0.35)

    #parallel(m, gyro=gyro)
