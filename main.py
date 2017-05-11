import Pyro4
import sys
import time
import importlib
import numpy as np
import algorithms.motion_planning as mp
import algorithms.map_management as maman
import threading
import logging
import config.params as params
try:
    import actuators.motors as motors
except Exception as e:
    print(e)
    logging.critical(e)
    import actuators.fakemotors as motors

class timer(threading.Thread):
    def __init__(self,threadName, server):
        threading.Thread.__init__(self)
        self.stop_flag = True
        self.threadName = threadName
        self.server = server
    def run(self):
        self.startingtime = time.time()
        while(self.stop_flag):
            time.sleep(0.5)
            try:
                self.server.setElapsedTime(int(time.time()-self.startingtime))
            except Exception:
                pass


def moveTo(path, m, t, ch, h, k, col, gyro):
    global pos
    global orientation
    global mat
    global unexplored_queue
    del path[1][0] # Delete the first element (The total distance)

    old_orientation = orientation
    old_pos = pos

    gyro.update()
    deg_pos = gyro.yawsum

    #Move forward just one cell
    if pos[0]==path[1][0][0]:
        if pos[1]>path[1][0][1]:
            new_dir=2
        else:
            new_dir=0
    else:
        if pos[0]>path[1][0][0]:
            new_dir=3
        else:
            new_dir=1
    if orientation!=new_dir:
        if abs(new_dir-orientation) == 2:
            m.rotateRight(gyro)
            try:
                server.setRobotOrientation((new_dir+1)%4)
            except Exception:
                pass
            m.rotateRight(gyro)
        elif new_dir-orientation == -3 or new_dir-orientation == 1:
            m.rotateLeft(gyro)
        elif new_dir-orientation == 3 or new_dir-orientation == -1:
            pass
            m.rotateRight(gyro)
        orientation=new_dir
        try:
            server.setRobotOrientation(new_dir)
        except Exception:
            pass

    mat = m.oneCellForward( mode = 'tof_fixed', tof = t , ch=ch, h=h, gyro=gyro, k=k, mat=mat, pos=pos, new_pos = path[1][0], deg_pos=deg_pos)
    m.parallel(t, gyro = gyro)

    pos=path[1][0]
    try:
        server.setRobotPosition(pos)
    except Exception:
        pass
    if sm.check_black(pos, col) and False: #To commentut
        m.posiziona_assi(gyro)
        if pos in unexplored_queue:
            unexplored_queue.remove(pos)
        refresh_map(sm.scanWalls((pos[0]+sim_pos[0],pos[1]+sim_pos[1]),orientation, t))
        mat[pos[0], pos[1]] = 256
        try:
            server.setMazeMap(mat)
        except Exception:
            pass
        orientation = old_orientation
        try:
            server.setRobotOrientation(new_dir)
        except Exception:
            pass
        pos = old_pos
        m.oneCellBack()
        try:
            server.setRobotPosition(pos)
        except Exception:
            pass





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
    if (nearcell not in unexplored_queue) and mat[nearcell[0]][nearcell[1]]==0 and not mat[pos[0]][pos[1]]//256 == 1: #If the cell is not queued and not explored yet
        mat[nearcell[0]][nearcell[1]] = 1 #Set as queued/explored
        unexplored_queue.append(nearcell) #Add to queue
    return mat, unexplored_queue

def refresh_map(walls):
    global mat
    global pos
    global home
    global unexplored_queue
    global sim_pos
    ##########Resize map, shift indexes, add walls and cells to queue

    if walls[0]>0 or mat[pos[0]][pos[1]-1] > 500: #Left wall
        if(mat[pos[0]][pos[1]-1] < 500):
            mat[pos[0]][pos[1]-1] = 1 #Set wall
    else:
        mat[pos[0]][pos[1]-1] = 0
        if pos[0]==1:
            mat = maman.appendTwoLinesToMatrix(mat, 1, 0)
            pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 1)
        mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]-2), unexplored_queue)


    if walls[1]>0 or mat[pos[0]+1][pos[1]] > 500: #Rear wall
        if(mat[pos[0]+1][pos[1]] < 500):
            mat[pos[0]+1][pos[1]] = 1 #Set wall
    else:
        mat[pos[0]+1][pos[1]] = 0
        if pos[1]==len(mat[0])-2:
            mat = maman.appendTwoLinesToMatrix(mat, 0, 1)

        mat, unexplored_queue = nearcellToQueue(mat, (pos[0]+2,pos[1]), unexplored_queue)


    if walls[2]>0 or mat[pos[0]][pos[1]+1] > 500: #Right wall
        if(mat[pos[0]][pos[1]+1] < 500):
            mat[pos[0]][pos[1]+1] = 1 #Set wall
    else:
        mat[pos[0]][pos[1]+1] = 0
        if pos[0]==len(mat)-2:
            mat = maman.appendTwoLinesToMatrix(mat, 1, 1)
        mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]+2), unexplored_queue)


    if walls[3]>0 or mat[pos[0]-1][pos[1]] > 500: #Front wall
        if(mat[pos[0]-1][pos[1]] < 500):
            mat[pos[0]-1][pos[1]] = 1 #Set wall
    else:
        mat[pos[0]-1][pos[1]] = 0
        if pos[1]==1:
            mat = maman.appendTwoLinesToMatrix(mat, 0, 0)
            pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 0)
        mat, unexplored_queue = nearcellToQueue(mat, (pos[0]-2,pos[1]), unexplored_queue)

def main(timer_thread, m, t, gyro, ch, h, k, col, server):

    #Global variables
    global mat; mat = [[0,0,0],[0,0,0],[0,0,0]] #1x1 Matrix
    global pos; pos = (1,1) #Initial position
    global home; home = (1,1) #Position of the initial cell
    global orientation; orientation = 3 #Initial orientation, generally
    global unexplored_queue; unexplored_queue = [] #Queue containing all the unexplored cells
    global sim_pos; sim_pos = (0,0)
    global interrupt_time
    bridge = []




    ###Initial settings to be displayed
    try:
        server.setRobotStatus("Waiting for start")
        server.setRobotPosition(pos)
        server.setVictimsNumber(0)
        server.setElapsedTime(0)
        server.setMazeMap(mat)
        server.setRobotOrientation(orientation)
    except Exception:
        pass
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
    m.parallel(tof = t, gyro =  gyro)
    while True:
        '''
        try:
            raw_input("Continue...")
        except:
            input("Continue...")
        '''
        if GPIO.event_detected(params.START_STOP_BUTTON_PIN) and time.time() - interrupt_time > 4:
            interrupt_time = time.time()
            print("Stopped by user")
            sys.exit()
        try:
            server.setRobotStatus("Exploring")
        except Exception:
            pass
        #Set current cell as explored
        mat[pos[0]][pos[1]] = 2

        #Remove current cell from unexplored cells if needed
        if pos in unexplored_queue:
            unexplored_queue.remove(pos)

        #Read sensors
        walls = sm.scanWalls((pos[0]+sim_pos[0],pos[1]+sim_pos[1]),orientation, t)
        print("Walls", walls)


        # If no part of the map is covered by another floor then the ramp can be ignored
        '''
        if(sm.check_bridge((pos[0]+sim_pos[0],pos[1]+sim_pos[1])) or sm.check_bridge(pos)):
            mat.itemset(pos, 1024)
            if sim_pos == (0,0):
                print("Rampa in salita")
                logging.info("Rampa in salita")
                if orientation == 0:
                    mat.itemset(pos[0]-1,pos[1], 512)
                elif orientation == 1:
                    mat.itemset(pos[0],pos[1]+1, 512)
                elif orientation == 2:
                    mat.itemset(pos[0]+1,pos[1], 512)
                elif orientation == 3:
                    mat.itemset(pos[0],pos[1]-1, 512)
                refresh_map(walls)
                bridge = [pos, (pos[0]+20, pos[1])]
                pos = (pos[0]+20, pos[1])
                server.setRobotPosition(pos)
                sim_pos = (-20,0)
                for i  in range(10):
                    mat = np.vstack((mat,np.zeros((2,np.shape(mat)[1]))))
                mat.itemset(pos,1024)
                if orientation == 0: #TODO invert this when racing. The robot does not teleport like in the simulation
                    mat.itemset(pos[0]-1,pos[1], 512)
                elif orientation == 1:
                    mat.itemset(pos[0],pos[1]+1, 512)
                elif orientation == 2:
                    mat.itemset(pos[0]+1,pos[1], 512)
                elif orientation == 3:
                    mat.itemset(pos[0],pos[1]-1, 512)
            else:
                print("Rampa in discesa")
                logging.info("Rampa in discesa")
                pos = (pos[0]-20, pos[1])
                server.setRobotPosition(pos)
                sim_pos = (0,0)

            #Read sensors
            walls = sm.scanWalls((pos[0]+sim_pos[0],pos[1]+sim_pos[1]),orientation, t)
            refresh_map(walls)
        else:
            refresh_map(walls)
        '''
        refresh_map(walls) #To comment when activated advanced ramp

        ##########
        try:
            server.setMazeMap(mat) #Update map
        except Exception:
            pass
        lost = False
        #Decide where to go
        if len(unexplored_queue)==0: #If there is no available cell to explore, the maze is done
            lost = False
            if pos!=home:
                try:
                    server.setRobotStatus("Done! Homing...")
                except Exception:
                    pass
                logging.info("Maze finished...")
                destination=mp.bestPath(orientation,[pos[0],pos[1]],[home],mat, bridge) #Find the best path to reach home
                if destination[0] != float('Inf'):
                    logging.info("Returning home")
                    while pos != home:
                        destination=mp.bestPath(orientation,[pos[0],pos[1]],[home],mat, bridge)
                        if destination[0] == float('Inf'):
                            lost = True
                            break
                        moveTo(destination, m, t, ch, h, k, col, gyro)
                    if lost == False:
                        k.blink()
                        time.sleep(4)
                        k.blink()
                        time.sleep(4)
                        k.blink()
                        time.sleep(4)
                else:
                    lost = True
            try:
                server.setRobotStatus("Done!")
            except Exception:
                pass
            stop_function(timer_thread,m)
            #Commented because the thread should start with the button

            try:
                raw_input("Press enter to continue")
            except:
                input("Press enter to continue")

            if lost == False:
                print("finished")
                #sys.exit()
                time.sleep(10)
                lost = True
        else:
            destination=mp.bestPath(orientation,[pos[0],pos[1]],unexplored_queue,mat, bridge) #Find the best path to reach the nearest cell

            #Move to destination
            if(destination[0] != float('Inf')):
                moveTo(destination, m, t, ch, h, k, col, gyro)
            else:
                try:
                    server.setRobotStatus('Lost')
                except Exception:
                    pass
                lost = True
        if lost == True:
            try:
                server.setRobotStatus('Lost. Roaming...')
            except Exception:
                pass
            print('Lost. Roaming...')
            logging.warning("Lost")
            mat = [[0,0,0],[0,0,0],[0,0,0]]
            pos = (1,1) #Initial position
            home = (1,1) #Position of the initial cell
            orientation = 3 #Initial orientation, generally
            unexplored_queue = [] #Queue containing all the unexplored cells
            sim_pos = (0,0)



if __name__ == '__main__':
    global interrupt_time; interrupt_time = time.time()
    logging.basicConfig(filename='log_robot.log',level=logging.DEBUG)
    if (len(sys.argv) >= 2 and sys.argv[1] == 'r') or True:
        logging.info("Starting in race mode")
        import sensors.sensors_handler as sm
        import sensors.tof as tof
        t = tof.Tof()
        t.activate_all()
        import sensors.imu as imu
        gyro = imu.Imu()
        import sensors.touch as touch
        ch = touch.Touch()
        import sensors.heat as heat
        h = heat.Heat()
        import sensors.color as color
        col = color.Color()
        import actuators.kit as kit
        k = kit.Kit()
        k.retract()
        import Adafruit_BBIO.GPIO as GPIO
    else:
        logging.info("Starting in simulation mode")
        import simulation.sensors as sm
        t = None
        gyro = None
        ch = None
        h = None
        col = None
        k = None
    try:
        server = Pyro4.Proxy("PYRONAME:robot.server") #Connect to server for graphical interface
    except Exception:
        server = None
    pins ={'fl':'P8_13','fr':'P8_19','rl':'P9_14','rr':'P9_16','dir_fl':'gpio31','dir_fr':'gpio48','dir_rl':'gpio60','dir_rr':'gpio30'}

    timer_thread = timer("Timer", server)
    timer_thread.start()
    m = motors.Motor(pins)
    print("Starting main loop")
    logging.info("Starting main loop")
    GPIO.setup(params.START_STOP_BUTTON_PIN, GPIO.IN)
    GPIO.add_event_detect(params.START_STOP_BUTTON_PIN, GPIO.RISING) #Attaching interrupt for start and stop
    m.stop()
    while True:
        while False:
            if GPIO.event_detected(params.START_STOP_BUTTON_PIN) and time.time() - interrupt_time > 0.5:
                interrupt_time = time.time()
                break
            else:
                k.blink()
                time.sleep(0.5)
        try:
            main(timer_thread=timer_thread, m=m, t=t, gyro=gyro, ch=ch, h=h, k=k, col=col, server=server)
        except KeyboardInterrupt as e:
            print("KeyboardInterrupt")
            logging.warning("KeyboardInterrupt")
            stop_function(timer=timer_thread, m=m)
            break
        except SystemExit as e:
            print("SystemExit")
            logging.warning("SystemExit")
            stop_function(timer=timer_thread, m=m)
        '''
        except Exception as e:
            logging.critical("%s", e)
            stop_function(timer=timer_thread, m=m)
            raise e
        '''
