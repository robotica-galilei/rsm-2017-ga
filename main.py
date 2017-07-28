import rospy
import sys
import time
import os
import pickle
from std_msgs.msg import String
import algorithms.motion_planning as mp
import algorithms.map_management as maman
import threading
import config.params as params
import actuators.motors as motors
#import actuators.ledmatrix.matrix as ledmatrix
import motion.cell_navigation as cn
import sensors.sensors_handler as sm
import sensors.tof as tof
import sensors.imu as imu
import sensors.touch as touch
import sensors.heat as heat
import sensors.color as color
import actuators.kit as kit
import sensors.start_button as start_button

class timer(threading.Thread):
    def __init__(self,threadName, pub):
        threading.Thread.__init__(self)
        self.stop_flag = True
        self.threadName = threadName
        self.pub = pub
    def run(self):
        self.startingtime = time.time()
        while(self.stop_flag):
            time.sleep(0.5)
            if pub != None:
                try:
                    self.pub.publish("tim:" + str(int(time.time()-self.startingtime)))
                except Exception:
                    pass

def publish_robot_info(pub, mat = None, orientation = None, pos = None, time = None, status = None):
    if pub != None:
        if mat != None:
            pub.publish("map:" + pickle.dumps(mat).decode("utf-8"))#Update map
        if orientation != None:
            pub.publish("ori:" + str(orientation))
        if pos != None:
            pub.publish("pos:" + pickle.dumps(pos).decode("utf-8"))
        if time != None:
            pub.publish("tim:" + str(time))
        if status != None:
            pub.publish("sta:" + str(status))

def moveTo(path, m, t, ch, h, k, col, gyro):
    global pos
    global orientation
    global mat
    global unexplored_queue
    global home
    del path[1][0] # Delete the first element (The cell where the robot is)

    old_orientation = orientation
    old_pos = pos

    gyro.update()
    deg_pos = gyro.yawsum
    #Move forward just one cell
    if pos[1]==path[1][0][1]:
        if pos[2]>path[1][0][2]:
            new_dir=0
        else:
            new_dir=2
    else:
        if pos[1]>path[1][0][1]:
            new_dir=3
        else:
            new_dir=1
    if orientation!=new_dir:
        if abs(new_dir-orientation) == 2:
            cn.rotateRight(m, gyro)
            orientation-=1
            if orientation < 0:
                orientation = 3
            cn.saveAllVictims(m, gyro, h.isThereSomeVideoVictim(), k, t)
            cn.rotateRight(m, gyro)
            orientation=new_dir
        elif new_dir-orientation == -3 or new_dir-orientation == 1:
            cn.rotateLeft(m, gyro)
            orientation=new_dir
            cn.saveAllVictims(m, gyro, h.isThereSomeVideoVictim(), k, t)
            m.setSpeeds(-20,-20)
            time.sleep(0.2)
            m.stop()
        elif new_dir-orientation == 3 or new_dir-orientation == -1:
            cn.rotateRight(m, gyro)
            orientation=new_dir
            cn.saveAllVictims(m, gyro, h.isThereSomeVideoVictim(), k, t)
            m.setSpeeds(-20,-20)
            time.sleep(0.2)
            m.stop()

        #Wait new measurement after robot rotation
        check_time = False
        check_time_N = False
        check_time_S = False
        while not check_time:
            if time.time() - t.time_last('N') < 0.2:
                check_time_N = True
            if time.time() - t.time_last('S') < 0.2:
                check_time_S = True
            if check_time_N and check_time_S:
                check_time = True

    orientation=new_dir
    publish_robot_info(pub, orientation=orientation)


    if time.time() - gyro.last_calibrated > 20 and t.is_there_a_wall('S'):
        cn.calibrate_gyro(m, gyro)

    time.sleep(0.3)
    walls = sm.scanWalls((pos[0],pos[1],pos[2]),orientation, t)
    refresh_map(walls)
    if(not walls[orientation]):
        temp_mat, temp_pos, nav_error = cn.oneCellForward(m= m, mode= 'new_tof', tof= t , ch= ch, h= h, gyro= gyro, k_kit= k, col=col, mat= mat, pos= pos, new_pos= path[1][0], deg_pos= deg_pos)
        #pos=path[1][0]
        if nav_error and path[1][0] in unexplored_queue:
            rospy.loginfo("LOG: Nav Error, aborting deleting from route")
            unexplored_queue.remove(path[1][0])
        mat = temp_mat
        pos = temp_pos
    elif path[1][0] in unexplored_queue:
        rospy.loginfo("LOG: Cannot reach next cell, aborting deleting from route")
        unexplored_queue.remove(path[1][0])
        mat[path[1][0][0]][path[1][0][1]][path[1][0][2]] = 0
    if (t.read_raw('E') < 30 and t.read_raw('E') != -1) or (t.read_raw('O') > 100 and t.is_there_a_wall('O') and (t.read_raw('E') > 300 or t.read_raw('E') == -1)):
            cn.disincagna(m, gyro, -1, coeff=0.5)
    if (t.read_raw('O') < 30 and t.read_raw('O') != -1) or (t.read_raw('E') > 100 and t.is_there_a_wall('E') and (t.read_raw('O') > 300 or t.read_raw('O') == -1)):
            cn.disincagna(m, gyro, 1, coeff=0.5)
    #cn.parallel(m, t, gyro = gyro)
    a = col.is_cell_silver()
    if a[0]:
        #saveNavigationCheckpoint(mat, pos, home, unexplored_queue)
        rospy.loginfo("LOG: CHECKPOINT")
        mat[pos[0]][pos[1]][pos[2]] = 128
    else:
        rospy.loginfo("LOG: No silver %s", a[1])


def saveNavigationCheckpoint(mat, pos, home, unexplored_queue):
    with open('/root/rsm-2017-ga/checkpoint.pickle', 'wb') as handle:
        pickle.dump((mat, pos, home, unexplored_queue, time.time()), handle, protocol=pickle.HIGHEST_PROTOCOL)


def getLastNavigationCheckpoint():
    with open('/root/rsm-2017-ga/checkpoint.pickle', 'rb') as handle:
        return pickle.load(handle)


def stop_function(timer, m):
    timer.stop_flag = False
    m.stop()

def nearcellToQueue(mat, nearcell, unexplored_queue):
    '''
    Just a function to reduce the repetition of code into the main
    @param m
        The matrix of the maze
    @param nearcell (tuple)
        The cell to check and add
    @param unexplored_queue (list of tuples)
        The list of the cells to view (X,Y)

    Returns the updated mat and unexplored_queue
    '''
    if (nearcell not in unexplored_queue) and mat[nearcell[0]][nearcell[1]][nearcell[2]]==0 and not mat[pos[0]][pos[1]][pos[2]]//256 == 1: #If the cell is not queued and not explored yet
        mat[nearcell[0]][nearcell[1]][nearcell[2]] = 1 #Set as queued/explored
        unexplored_queue.append(nearcell) #Add to queue
    return mat, unexplored_queue

def refresh_map(walls, add = True):
    global mat
    global pos
    global home
    global unexplored_queue
    global sim_pos
    ##########Resize map, shift indexes, add walls and cells to queue

    nearcell = (pos[0],pos[1],pos[2]-2)
    if walls[0]>0 or mat[pos[0]][pos[1]][pos[2]-1] > 500: #Left wall
        if(mat[pos[0]][pos[1]][pos[2]-1] < 500):
            mat[pos[0]][pos[1]][pos[2]-1] = 1 #Set wall
        if nearcell in unexplored_queue and mp.bestPath(orientation,pos,[nearcell],mat, bridge)[0] == float('Inf'):
            unexplored_queue.remove(nearcell)
            if mat[nearcell[0]][nearcell[1]][nearcell[2]] == 1:
                mat[nearcell[0]][nearcell[1]][nearcell[2]] = 0
    else:
        mat[pos[0]][pos[1]][pos[2]-1] = 0
        if add and pos[2]==1:
            mat = maman.appendTwoLinesToMatrix(mat, 1, 0)
            pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 1)
        if add:
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1],pos[2]-2), unexplored_queue)


    nearcell = (pos[0],pos[1]+2,pos[2])
    if walls[1]>0 or mat[pos[0]][pos[1]+1][pos[2]] > 500: #Rear wall
        if(mat[pos[0]][pos[1]+1][pos[2]] < 500):
            mat[pos[0]][pos[1]+1][pos[2]] = 1 #Set wall
        if nearcell in unexplored_queue and mp.bestPath(orientation,pos,[nearcell],mat, bridge)[0] == float('Inf'):
            unexplored_queue.remove(nearcell)
            if mat[nearcell[0]][nearcell[1]][nearcell[2]] == 1:
                mat[nearcell[0]][nearcell[1]][nearcell[2]] = 0
    else:
        mat[pos[0]][pos[1]+1][pos[2]] = 0
        if add and pos[1]==len(mat[0])-2:
            mat = maman.appendTwoLinesToMatrix(mat, 0, 1)
        if add:
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]+2,pos[2]), unexplored_queue)


    nearcell = (pos[0],pos[1],pos[2]+2)
    if walls[2]>0 or mat[pos[0]][pos[1]][pos[2]+1] > 500: #Right wall
        if(mat[pos[0]][pos[1]][pos[2]+1] < 500):
            mat[pos[0]][pos[1]][pos[2]+1] = 1 #Set wall
        if nearcell in unexplored_queue and mp.bestPath(orientation,pos,[nearcell],mat, bridge)[0] == float('Inf'):
            unexplored_queue.remove(nearcell)
            if mat[nearcell[0]][nearcell[1]][nearcell[2]] == 1:
                mat[nearcell[0]][nearcell[1]][nearcell[2]] = 0
    else:
        mat[pos[0]][pos[1]][pos[2]+1] = 0
        if add and pos[2]==len(mat[0][0])-2:
            mat = maman.appendTwoLinesToMatrix(mat, 1, 1)
        if add:
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1],pos[2]+2), unexplored_queue)


    nearcell = (pos[0],pos[1]-2,pos[2])
    if walls[3]>0 or mat[pos[0]][pos[1]-1][pos[2]] > 500: #Front wall
        if(mat[pos[0]][pos[1]-1][pos[2]] < 500):
            mat[pos[0]][pos[1]-1][pos[2]] = 1 #Set wall
        if nearcell in unexplored_queue and mp.bestPath(orientation,pos,[nearcell],mat, bridge)[0] == float('Inf'):
            unexplored_queue.remove(nearcell)
            if mat[nearcell[0]][nearcell[1]][nearcell[2]] == 1:
                mat[nearcell[0]][nearcell[1]][nearcell[2]] = 0
    else:
        mat[pos[0]][pos[1]-1][pos[2]] = 0
        if add and pos[1]==1:
            mat = maman.appendTwoLinesToMatrix(mat, 0, 0)
            pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 0)
        if add:
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]-2,pos[2]), unexplored_queue)

    return mat, pos

def main(timer_thread, m, t, gyro, ch, h, k, col, pub):

    #Global variables
    global mat; mat = [[[0,0,0],[0,0,0],[0,0,0]]] #1x1 Matrix
    global pos; pos = (0,1,1) #Initial position
    global home; home = (0,1,1) #Position of the initial cell
    global orientation; orientation = 3 #Initial orientation, generally
    global unexplored_queue; unexplored_queue = [] #Queue containing all the unexplored cells
    global interrupt_time
    global bridge; bridge = []




    ###Initial settings to be displayed
    if pub != None:
        publish_robot_info(pub=pub, mat=mat, orientation=orientation, pos=pos, time=0, status="Waiting for start")
    ###

    #Commented because the thread should start with the button
    '''
    try:
        raw_input("Continue...")
    except:
        input("Continue...")
    '''


    gyro.update()
    gyro.starting_deg = gyro.yawsum
    gyro.last_calibrated = time.time()
    #cn.parallel(m, tof = t, gyro =  gyro) #Useless at beginning

    rospy.loginfo("LOG: Starting while cycle")
    while True:
        #Set current cell as explored
        if mat[pos[0]][pos[1]][pos[2]] < 2:
            mat[pos[0]][pos[1]][pos[2]] = 2

        if pub != None:
            publish_robot_info(pub=pub, mat=mat, orientation=orientation, pos=pos)
        '''
        try:
            raw_input("Continue...")
        except:
            input("Continue...")
        '''

        '''
        if GPIO.event_detected(params.START_STOP_BUTTON_PIN) and time.time() - interrupt_time > 4:
            interrupt_time = time.time()
            print("Stopped by user")
            sys.exit()
        '''
        if pub != None:
            publish_robot_info(pub, status="Exploring")

        publish_robot_info(pub, mat=mat, orientation=orientation, pos=pos)

        #Remove current cell from unexplored cells if needed
        if pos in unexplored_queue:
            unexplored_queue.remove(pos)

        #Read sensors
        walls = sm.scanWalls(pos,orientation, t)
        rospy.loginfo("LOG: Walls: %s", walls)
        print("Walls", walls)

        refresh_map(walls) #To comment when activated advanced ramp
        if pub != None:
            publish_robot_info(pub=pub, mat=mat, orientation=orientation, pos=pos)
        ##########
        lost = False
        #Decide where to go
        if len(unexplored_queue)==0: #If there is no available cell to explore, the maze is done
            lost = False
            if pos!=home:
                if pub != None:
                    publish_robot_info(pub, status="Done! Homing...")
                rospy.loginfo("LOG: Maze finished...")
                destination=mp.bestPath(orientation,[pos[0],pos[1],pos[2]],[home],mat, bridge) #Find the best path to reach home
                if destination[0] != float('Inf'):
                    rospy.loginfo("LOG: Returning home")
                    while pos != home:
                        publish_robot_info(pub, mat=mat, orientation=orientation, pos=pos)
                        destination=mp.bestPath(orientation,[pos[0],pos[1],pos[2]],[home],mat, bridge)
                        if destination[0] == float('Inf'):
                            lost = True
                            break
                        moveTo(destination, m, t, ch, h, k, col, gyro)
                    if lost == False:
                        k.blink()
                        time.sleep(3)
                        k.blink()
                        time.sleep(3)
                        k.blink()
                        time.sleep(3)
                else:
                    lost = True
            if pub != None:
                publish_robot_info(pub, status="Done!")
            stop_function(timer_thread,m)
            #Commented because the thread should start with the button
            '''
            try:
                raw_input("Press enter to continue")
            except:
                input("Press enter to continue")
            '''

            if lost == False:
                print("finished")
                #sys.exit()
                time.sleep(2)
                lost = True
        else:
            rospy.logdebug("LOG: unexplored_queue: %s", unexplored_queue)
            destination=mp.bestPath(orientation,[pos[0],pos[1],pos[2]],unexplored_queue,mat, bridge) #Find the best path to reach the nearest cell
            #Move to destination
            if(destination[0] != float('Inf')):
                moveTo(destination, m, t, ch, h, k, col, gyro)
            else:
                if pub != None:
                    publish_robot_info(pub, status="Lost")
                unexplored_queue = []

        if lost == True:
            if pub != None:
                publish_robot_info(pub, status="Lost. Roaming...")
            print('Lost. Roaming...')
            rospy.logwarn("Lost")
            mat = [[[0,0,0],[0,0,0],[0,0,0]]]
            pos = (0,1,1) #Initial position
            home = (0,1,1) #Position of the initial cell
            orientation = 3 #Initial orientation, generally
            unexplored_queue = [] #Queue containing all the unexplored cells



if __name__ == '__main__':
    rospy.init_node('robot', log_level=rospy.DEBUG)
    rospy.loginfo("LOG: ----------BOOT----------")
    rospy.loginfo("LOG: Finished library import")
    pub = rospy.Publisher('navigation', String, queue_size=1) #Connect to server for graphical interface
    publish_robot_info(pub, status="Boot completed", time=0)
    global interrupt_time; interrupt_time = time.time()
    m = motors.Motor(params.motors_pins)
    m.stop()
    t = tof.Tof(from_ros = True)
    #t.activate_all()
    gyro = imu.Imu(from_ros = True)
    ch = touch.Touch()
    h = heat.Heat(from_ros = True)
    col = color.Color(from_ros = True)
    k = kit.Kit()
    k.retract()
    b = start_button.StartButton(from_ros = True)


    rospy.loginfo("LOG: Starting timer thread")

    timer_thread = timer("Timer", pub)

    print("Starting main loop")

    bypass_start_button = False

    while True:
        rospy.loginfo("LOG: Waiting for start")
        publish_robot_info(pub, status="Waiting for start")
        while b.activated == False and not bypass_start_button:
            k.blink()
            time.sleep(0.4)
        time.sleep(0.2)
        b.activated = False
        rospy.loginfo("LOG: Starting main")
        try:
            timer_thread.start()
            main(timer_thread=timer_thread, m=m, t=t, gyro=gyro, ch=ch, h=h, k=k, col=col, pub=pub)
        except KeyboardInterrupt as e:
            print("KeyboardInterrupt")
            stop_function(timer=timer_thread, m=m)
            break
        except SystemExit as e:
            print("SystemExit")
            stop_function(timer=timer_thread, m=m)

        except Exception as e:
            stop_function(timer=timer_thread, m=m)
            for i in range(4)
                k.blink()
                time.sleep(0.3)
            bypass_start_button = True
            #raise e
