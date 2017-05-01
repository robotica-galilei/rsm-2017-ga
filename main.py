import Pyro4
import sys
import time
import numpy as np
import simulation.sensors as sm
import algorithms.motion_planning as mp
import algorithms.map_management as maman
import threading
try:
    import actuators.motors as motors
except Exception:
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
            self.server.setElapsedTime(int(time.time()-self.startingtime))


def moveTo(path, m):
    global pos
    global orientation
    global mat
    global unexplored_queue
    del path[1][0] # Delete the first element (The total distance)

    old_orientation = orientation
    old_pos = pos

    #Move forward just one cell
    if pos[0]==path[1][0][0]:
        if pos[1]>path[1][0][1]:
            new_dir=3
        else:
            new_dir=1
    else:
        if pos[0]>path[1][0][0]:
            new_dir=0
        else:
            new_dir=2
    if orientation!=new_dir:
        if abs(new_dir-orientation) == 2:
            m.rotateRight()
            server.setRobotOrientation((new_dir+1)%4)
            m.rotateRight()
        elif new_dir-orientation == -3 or new_dir-orientation == 1:
            m.rotateLeft()
        elif new_dir-orientation == 3 or new_dir-orientation == -1:
            pass
            m.rotateRight()
        orientation=new_dir
        server.setRobotOrientation(new_dir)
    m.oneCellForward()
    pos=path[1][0]
    server.setRobotPosition(pos)
    if (sm.check_black(pos)):
        if pos in unexplored_queue:
            unexplored_queue.remove(pos)
        refresh_map(sm.scanWalls((pos[0]+sim_pos[0],pos[1]+sim_pos[1]),orientation))
        mat.itemset(pos, 256)
        server.setMazeMap(mat.tolist())
        orientation = old_orientation
        server.setRobotOrientation(new_dir)
        pos = old_pos
        m.oneCellBack()
        server.setRobotPosition(pos)



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
    if (nearcell not in unexplored_queue) and mat.item(nearcell)==0 and not sm.check_black(pos): #If the cell is not queued and not explored yet
        mat.itemset(nearcell,1) #Set as queued/explored
        unexplored_queue.append(nearcell) #Add to queue
    return mat, unexplored_queue

def refresh_map(walls):
    global mat
    global pos
    global home
    global unexplored_queue
    global sim_pos
    ##########Resize map, shift indexes, add walls and cells to queue
    if walls[0]>0 or mat.item((pos[0]-1,pos[1]))>500: #Left wall
        if(mat.item((pos[0]-1,pos[1]))<500):
            mat.itemset((pos[0]-1,pos[1]),1) #Set wall
    else:
        if pos[0]==1:
            mat = maman.appendTwoLinesToMatrix(mat, 1, 0)
            pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 1)
        mat, unexplored_queue = nearcellToQueue(mat, (pos[0]-2,pos[1]), unexplored_queue)


    if walls[1]>0 or mat.item((pos[0],pos[1]+1))>500: #Bottom wall
        if(mat.item((pos[0],pos[1]+1))<500):
            mat.itemset((pos[0],pos[1]+1),1) #Set wall
    else:
        if pos[1]==np.shape(mat)[1]-2:
            mat = maman.appendTwoLinesToMatrix(mat, 0, 1)
        mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]+2), unexplored_queue)


    if walls[2]>0 or mat.item((pos[0]+1,pos[1]))>500: #Right wall
        if(mat.item((pos[0]+1,pos[1]))<500):
            mat.itemset((pos[0]+1,pos[1]),1) #Set wall
    else:
        if pos[0]==np.shape(mat)[0]-2:
            mat = maman.appendTwoLinesToMatrix(mat, 1, 1)
        mat, unexplored_queue = nearcellToQueue(mat, (pos[0]+2,pos[1]), unexplored_queue)


    if walls[3]>0 or mat.item((pos[0],pos[1]-1))>500: #Top wall
        if(mat.item((pos[0],pos[1]-1))<500):
            mat.itemset((pos[0],pos[1]-1),1) #Set wall
    else:
        if pos[1]==1:
            mat = maman.appendTwoLinesToMatrix(mat, 0, 0)
            pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 0)
        mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]-2), unexplored_queue)


def main(timer_thread, m, server):

    #Global variables
    global mat; mat = np.matrix("0 0 0; 0 0 0; 0 0 0") #1x1 Matrix
    global pos; pos = (1,1) #Initial position
    global home; home = (1,1) #Position of the initial cell
    global orientation; orientation = 3 #Initial orientation, generally
    global unexplored_queue; unexplored_queue = [] #Queue containing all the unexplored cells
    global sim_pos; sim_pos = (0,0)
    bridge = []
    #print(mat)

    ###Initial settings to be displayed
    server.setRobotStatus("Waiting for start")
    server.setRobotPosition(pos)
    server.setVictimsNumber(0)
    server.setElapsedTime(0)
    server.setMazeMap(mat.tolist())
    server.setRobotOrientation(orientation)
    ###

    try:
        raw_input("Continue...")
    except:
        input("Continue...")

    timer_thread.start()

    while True:
        server.setRobotStatus("Exploring")
        #Set current cell as explored
        mat.itemset(pos,2)

        #Remove current cell from unexplored cells if needed
        if pos in unexplored_queue:
            unexplored_queue.remove(pos)

        #Read sensors
        walls = sm.scanWalls((pos[0]+sim_pos[0],pos[1]+sim_pos[1]),orientation)


        if(sm.check_victim(pos)):
            mat.itemset(pos, 512)

        if(sm.check_bridge((pos[0]+sim_pos[0],pos[1]+sim_pos[1])) or sm.check_bridge(pos)):
            mat.itemset(pos, 1024)
            if sim_pos == (0,0):
                print("Rampa in salita")
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
                pos = (pos[0]-20, pos[1])
                server.setRobotPosition(pos)
                sim_pos = (0,0)

            #Read sensors
            walls = sm.scanWalls((pos[0]+sim_pos[0],pos[1]+sim_pos[1]),orientation)
            refresh_map(walls)
        else:
            refresh_map(walls)


        ##########

        server.setMazeMap(mat.tolist()) #Update map

        #Decide where to go
        if len(unexplored_queue)==0: #If there is no available cell to explore, the maze is done
            if pos!=home:
                server.setRobotStatus("Done! Homing...")
                destination=mp.bestPath(orientation,[pos[0],pos[1]],[home],mat, bridge) #Find the best path to reach home
                if(destination[0] != float('Inf')):
                    while pos != home:
                        destination=mp.bestPath(orientation,[pos[0],pos[1]],[home],mat, bridge)
                        moveTo(destination, m)
                else:
                    server.setRobotStatus('Lost. Roaming...')
            server.setRobotStatus("Done!")
            input("Press enter to continue")
            stop_function(timer_thread,m)
            sys.exit()
        else:
            destination=mp.bestPath(orientation,[pos[0],pos[1]],unexplored_queue,mat, bridge) #Find the best path to reach the nearest cell

            #Move to destination
            if(destination[0] != float('Inf')):
                moveTo(destination, m)
            else:
                server.setRobotStatus('Lost')



if __name__ == '__main__':

    server = Pyro4.Proxy("PYRONAME:robot.server") #Connect to server for graphical interface

    pins ={'fl':'P8_13','fr':'P8_19','rl':'P9_14','rr':'P9_16','dir_fl':'gpio31','dir_fr':'gpio48','dir_rl':'gpio60','dir_rr':'gpio30'}

    timer_thread = timer("Timer", server)
    m = motors.Motor(pins)

    try:
        main(timer_thread=timer_thread, m=m, server=server)
    except KeyboardInterrupt as e:
        stop_function(timer=timer_thread, m=m)
    #except Exception as e:
    #    print(e)
