import Pyro4
import sys
import time
import os
import importlib
import numpy as np
import algorithms.motion_planning as mp
import algorithms.map_management as maman
import threading
import logging
import config.params as params
import actuators.motors as motors
import motion.cell_navigation as cn

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
            if server != None:
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
            time.sleep(0.3)
        elif new_dir-orientation == -3 or new_dir-orientation == 1:
            cn.rotateLeft(m, gyro)
            orientation=new_dir
            cn.saveAllVictims(m, gyro, h.isThereSomeVideoVictim(), k, t)
            m.setSpeeds(-20,-20)
            time.sleep(0.2)
            m.stop()
            time.sleep(0.3)
        elif new_dir-orientation == 3 or new_dir-orientation == -1:
            pass
            cn.rotateRight(m, gyro)
            orientation=new_dir
            cn.saveAllVictims(m, gyro, h.isThereSomeVideoVictim(), k, t)
            m.setSpeeds(-20,-20)
            time.sleep(0.2)
            m.stop()
            time.sleep(0.3)
    orientation=new_dir


    if time.time() - gyro.last_calibrated > 20 and t.is_there_a_wall('S'):
        cn.calibrate_gyro(m, gyro)

    time.sleep(0.3)
    walls = sm.scanWalls((pos[0],pos[1],pos[2]),orientation, t)
    refresh_map(walls)
    if(not walls[orientation]):
        temp_mat = cn.oneCellForward(m= m, mode= 'new_tof', tof= t , ch= ch, h= h, gyro= gyro, k_kit= k, mat= mat, pos= pos, new_pos= path[1][0], deg_pos= deg_pos)
        pos=path[1][0]
    elif pos in unexplored_queue:
        unexplored_queue.remove(pos)
    cn.parallel(m, t, gyro = gyro)


    if col.is_cell_black(): # and False: #To comment out the False
        cn.posiziona_assi(m,gyro)
        if pos in unexplored_queue:
            unexplored_queue.remove(pos)
        mat, pos = refresh_map(sm.scanWalls((pos[0],pos[1],pos[2]),orientation, t), add = False)
        mat[pos[0]][pos[1]][pos[2]] = 256
        orientation = old_orientation
        pos = old_pos
        cn.oneCellBack(m, mode='time')





def stop_function(timer, m):
    timer.stop_flag = False
    m.stop()
    os.system("rosnode kill listener")

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
        if nearcell in unexplored_queue and mp.bestPath(orientation,pos,[nearcell],mat, bridge):
            unexplored_queue.remove(nearcell)

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
        if nearcell in unexplored_queue and mp.bestPath(orientation,pos,[nearcell],mat, bridge) == float('Inf'):
            unexplored_queue.remove(nearcell)
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
        if nearcell in unexplored_queue and mp.bestPath(orientation,pos,[nearcell],mat, bridge) == float('Inf'):
            unexplored_queue.remove(nearcell)
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
        if nearcell in unexplored_queue and mp.bestPath(orientation,pos,[nearcell],mat, bridge) == float('Inf'):
            unexplored_queue.remove(nearcell)
    else:
        mat[pos[0]][pos[1]-1][pos[2]] = 0
        if add and pos[1]==1:
            mat = maman.appendTwoLinesToMatrix(mat, 0, 0)
            pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 0)
        if add:
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]-2,pos[2]), unexplored_queue)

    return mat, pos

def main(timer_thread, m, t, gyro, ch, h, k, col, server):

    #Global variables
    global mat; mat = [[[0,0,0],[0,0,0],[0,0,0]]] #1x1 Matrix
    global pos; pos = (0,1,1) #Initial position
    global home; home = (0,1,1) #Position of the initial cell
    global orientation; orientation = 3 #Initial orientation, generally
    global unexplored_queue; unexplored_queue = [] #Queue containing all the unexplored cells
    global interrupt_time
    global bridge; bridge = []




    ###Initial settings to be displayed
    if server != None:
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
    gyro.last_calibrated = time.time()
    cn.parallel(m, tof = t, gyro =  gyro)
    while True:
        #Set current cell as explored
        mat[pos[0]][pos[1]][pos[2]] = 2
        if server != None:
            try:
                server.setMazeMap(mat) #Update map
                server.setRobotOrientation(orientation)
                server.setRobotPosition(pos)
            except:
                pass
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
        if server != None:
            try:
                server.setRobotStatus("Exploring")
            except Exception:
                pass

        #Remove current cell from unexplored cells if needed
        if pos in unexplored_queue:
            unexplored_queue.remove(pos)

        #Read sensors
        walls = sm.scanWalls(pos,orientation, t)
        print("Walls", walls)

        refresh_map(walls) #To comment when activated advanced ramp
        if server != None:
            try:
                server.setMazeMap(mat) #Update map
                server.setRobotOrientation(orientation)
                server.setRobotPosition(pos)
            except:
                pass

        ##########
        lost = False
        #Decide where to go
        if len(unexplored_queue)==0: #If there is no available cell to explore, the maze is done
            lost = False
            if pos!=home:
                if server != None:
                    try:
                        server.setRobotStatus("Done! Homing...")
                    except Exception:
                        pass
                logging.info("Maze finished...")
                destination=mp.bestPath(orientation,[pos[0],pos[1],pos[2]],[home],mat, bridge) #Find the best path to reach home
                if destination[0] != float('Inf'):
                    logging.info("Returning home")
                    while pos != home:
                        destination=mp.bestPath(orientation,[pos[0],pos[1],pos[2]],[home],mat, bridge)
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
            if server != None:
                try:
                    server.setRobotStatus("Done!")
                except Exception:
                    pass
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
                time.sleep(10)
                lost = True
        else:
            destination=mp.bestPath(orientation,[pos[0],pos[1],pos[2]],unexplored_queue,mat, bridge) #Find the best path to reach the nearest cell
            #Move to destination
            if(destination[0] != float('Inf')):
                moveTo(destination, m, t, ch, h, k, col, gyro)
            else:
                if server != None:
                    try:
                        server.setRobotStatus('Lost')
                    except Exception:
                        pass
                unexplored_queue = []

        if lost == True:
            if server != None:
                try:
                    server.setRobotStatus('Lost. Roaming...')
                except Exception:
                    pass
            print('Lost. Roaming...')
            logging.warning("Lost")
            mat = [[[0,0,0],[0,0,0],[0,0,0]]]
            pos = (0,1,1) #Initial position
            home = (0,1,1) #Position of the initial cell
            orientation = 3 #Initial orientation, generally
            unexplored_queue = [] #Queue containing all the unexplored cells



if __name__ == '__main__':
    global interrupt_time; interrupt_time = time.time()
    logging.basicConfig(filename='log_robot.log',level=logging.DEBUG)
    m = motors.Motor(params.motors_pins)
    m.stop()
    if (len(sys.argv) >= 2 and sys.argv[1] == 'r') or True:
        logging.info("Starting in race mode")
        import sensors.sensors_handler as sm
        import sensors.tof as tof
        t = tof.Tof(from_ros = True)
        #t.activate_all()
        import sensors.imu as imu
        gyro = imu.Imu()
        import sensors.touch as touch
        ch = touch.Touch()
        import sensors.heat as heat
        h = heat.Heat(from_ros = True)
        import sensors.color as color
        col = color.Color(from_ros = True)
        import actuators.kit as kit
        k = kit.Kit()
        k.retract()
        import sensors.start_button as start_button
        b = start_button.StartButton(from_ros = True)
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
    except:
        server = None
    try:
        server.ping()
    except:
        server = None

    timer_thread = timer("Timer", server)
    timer_thread.start()

    print("Starting main loop")
    logging.info("Starting main loop")


    while True:
        while b.activated == False:
            k.blink()
            time.sleep(0.4)
        time.sleep(0.2)
        b.activated = False
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
