import Pyro4
import sys
import time
import numpy as np
import simulation.sensors as sm
import algorithms.motion_planning as mp



if __name__ == '__main__':
    #Global variables
    mat = np.matrix("0 1 0 1 0 1 0; 1 0 0 0 0 0 1; 0 1 0 1 0 0 0; 1 0 0 0 0 0 1; 0 1 0 0 0 1 0; 1 0 0 0 0 0 1; 0 0 0 1 0 1 0; 1 0 0 0 0 0 1; 0 1 0 1 0 1 0")
    pos = (1,1)
    orientation=3
    queue=[]
    print(mat)
    
    server = Pyro4.Proxy("PYRONAME:robot.server")    # use name server object lookup uri shortcut
    server.setRobotStatus("Waiting for start")
    server.setVictimsNumber(0)
    server.setMazeMap(mat.tolist())
    #print(mat.tolist())
    server.setElapsedTime(0)
    
    #Read sensors
    walls = sm.scanWalls(pos,orientation)
    #print(walls)
    
    #Rectify readings on the orientation
    for i in range(0,3-orientation):
        walls.append(walls[0])
        del walls[0]
    #print(walls)
    
    #Resize map and shift indexes
    
    
    #print(dijkstra([1,1],[3,3],mat))
    #available = [[7,5],[3,1]]
    #print(best_path(1,[1,1],available,mat))
