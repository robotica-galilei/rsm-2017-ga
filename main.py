import Pyro4
import sys
import time
import numpy as np
import simulation.sensors as sm
import algorithms.motion_planning as mp
import algorithms.map_management as maman
try:
    import actuators.motors as motors
except ModuleNotFoundError:
    import actuators.fakemotors as motors


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
                m.rotateRight()
            elif new_dir-orientation == 3 or new_dir-orientation == -1:
                pass
                m.rotateLeft()
            orientation=new_dir
            server.setRobotOrientation(new_dir)
        m.oneCellForward()
        pos=i
        server.setRobotPosition(pos)

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

if __name__ == '__main__':
    #Global variables
    mat = np.matrix("0 0 0; 0 0 0; 0 0 0") #1x1 Matrix
    pos = (1,1) #Initial position
    home = (1,1) #Position of the initial cell
    orientation=3 #Initial orientation, generally
    unexplored_queue=[] #Queue containing all the unexplored cells
    #print(mat)

    server = Pyro4.Proxy("PYRONAME:robot.server") #Connect to server for graphical interface

    ###Initial settings to be displayed
    server.setRobotStatus("Waiting for start")
    server.setRobotPosition(pos)
    server.setVictimsNumber(0)
    server.setElapsedTime(0)
    server.setMazeMap(mat.tolist())
    server.setRobotOrientation(orientation)
    ###

    pins = pins ={'fl':'P9_14','fr':'P9_16','rl':'P8_13','rr':'P8_19','dir_fl':'gpio60','dir_fr':'gpio48','dir_rl':'gpio49','dir_rr':'gpio20'}
    m = motors.Motor(pins)
    try:
        raw_input("Continue...")
    except:
        input("Continue...")
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
