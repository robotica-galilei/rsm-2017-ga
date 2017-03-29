import Pyro4
import sys
import time
import numpy as np
import simulation.sensors as sm
import algorithms.motion_planning as mp
import algorithms.map_management as maman
import sensors.mpu6050.MPU6050_multithreading as gyrolib
import threading

import actuators.motors as motors

class timer(threading.Thread):
    def __init__(self,threadName,startingtime, server):
        threading.Thread.__init__(self)
        self.stop_flag = True
        self.threadName = threadName
        self.startingtime = startingtime
        self.server = server
    def run(self):
        while(self.stop_flag):
            time.sleep(0.5)
            self.server.setElapsedTime(int(time.time()-self.startingtime))


def moveTo(path, m):
    global pos
    global orientation
    del path[1][0]
    for i in path[1]:
        if pos[0]==i[0]:
            if pos[1]>i[1]:
                new_dir=3
            else:
                new_dir=1
        else:
            if pos[0]>i[0]:
                new_dir=0
            else:
                new_dir=2
        if orientation!=new_dir:
            if abs(new_dir-orientation) == 2:
                m.rotateRight()
                m.rotateRight()
            elif new_dir-orientation == -3 or new_dir-orientation == 1:
                m.rotateLeft()
            elif new_dir-orientation == 3 or new_dir-orientation == -1:
                pass
                m.rotateRight()
            orientation=new_dir
            server.setRobotOrientation(new_dir)
        m.oneCellForward()
        pos=i
        server.setRobotPosition(pos)


def stop_function(timer, m, gyro):
    timer.stop_flag = False
    gyro.stop_flag = False
    m.stop()

def nearcellToQueue(mat, nearcell, unexplored_queue):
    '''
    Just a function to reduce the repetition of code into the main
    @param mat
        The matrix of the maze
    @param nearcell (tuple)
        The cell to check and add
    @param unexplored_queue (list of tuples)
        The list of the cells to view (X,Y)

    Returns the updated mat and unexplored_queue
    '''
    if (nearcell not in unexplored_queue) and mat.item(nearcell)==0: #If the cell is not queued and not explored yet
        mat.itemset(nearcell,1) #Set as queued/explored
        unexplored_queue.append(nearcell) #Add to queue
    return mat, unexplored_queue


def main(timer_thread, m, server):

    #Global variables
    global mat; mat = np.matrix("0 0 0; 0 0 0; 0 0 0") #1x1 Matrix
    global pos; pos = (1,1) #Initial position
    global home; home = (1,1) #Position of the initial cell
    global orientation; orientation = 3 #Initial orientation, generally
    global unexplored_queue; unexplored_queue = [] #Queue containing all the unexplored cells
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
        walls = sm.scanWalls(pos,orientation)

        #Rectify readings on the orientation of the robot (cyclic permutation)
        for i in range(0,3-orientation):
            walls.append(walls[0])
            del walls[0]


        ##########Resize map, shift indexes, add walls and cells to queue
        if walls[0]>0: #Left wall
            mat.itemset((pos[0]-1,pos[1]),1) #Set wall
        else:
            if pos[0]==1:
                mat = maman.appendTwoLinesToMatrix(mat, 1, 0)
                pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 1)
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0]-2,pos[1]), unexplored_queue)


        if walls[1]>0: #Bottom wall
            mat.itemset((pos[0],pos[1]+1),1) #Set wall
        else:
            if pos[1]==np.shape(mat)[1]-2:
                mat = maman.appendTwoLinesToMatrix(mat, 0, 1)
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]+2), unexplored_queue)


        if walls[2]>0: #Right wall
            mat.itemset((pos[0]+1,pos[1]),1) #Set wall
        else:
            if pos[0]==np.shape(mat)[0]-2:
                mat = maman.appendTwoLinesToMatrix(mat, 1, 1)
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0]+2,pos[1]), unexplored_queue)

        if walls[3]>0: #Top wall
            mat.itemset((pos[0],pos[1]-1),1) #Set wall
        else:
            if pos[1]==1:
                mat = maman.appendTwoLinesToMatrix(mat, 0, 0)
                pos, home, unexplored_queue = maman.updatePosition(pos, home, unexplored_queue, 0)
            mat, unexplored_queue = nearcellToQueue(mat, (pos[0],pos[1]-2), unexplored_queue)
        ##########

        server.setMazeMap(mat.tolist()) #Update map

        #Decide where to go
        if len(unexplored_queue)==0: #If there is no available cell to explore, the maze is done
            if pos!=home:
                server.setRobotStatus("Done! Homing...")
                destination=mp.bestPath(orientation,[pos[0],pos[1]],[home],mat) #Find the best path to reach home
                moveTo(destination, m)
            server.setRobotStatus("Done!")
            input("Press enter to continue")
            sys.exit()

        destination=mp.bestPath(orientation,[pos[0],pos[1]],unexplored_queue,mat) #Find the best path to reach the nearest cell

        #Move to destination
        moveTo(destination, m)

        #print(dijkstra([1,1],[3,3],mat))
        #available = [[7,5],[3,1]]
        #print(best_path(1,[1,1],available,mat))


if __name__ == '__main__':

    server = Pyro4.Proxy("PYRONAME:robot.server") #Connect to server for graphical interface

    pins = pins ={'fl':'P9_14','fr':'P9_16','rl':'P8_13','rr':'P8_19','dir_fl':'gpio60','dir_fr':'gpio48','dir_rl':'gpio49','dir_rr':'gpio20'}

    timer_thread = timer("Timer", time.time(), server)
    gyro = gyrolib.GYRO("Gyro")
    m = motors.Motor(pins, gyro)
    gyro.start()

    try:
        main(timer_thread=timer_thread, m=m, server=server)
    except Exception as e:
        stop_function(timer=timer_thread, m=m, gyro=gyro)
        print(e)
