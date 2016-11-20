import Pyro4
import sys
import time
import numpy as np
import simulation.sensors as sm
import algorithms.motion_planning as mp


def moveTo(path):
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
            orientation=new_dir
            time.sleep(0.5)
        server.setRobotOrientation(new_dir)
        time.sleep(0.5)
        pos=i
        server.setRobotPosition(pos)

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
                mat = np.vstack((np.zeros((2,np.shape(mat)[1])),mat)) #Add 2 columns to the left
                pos = (pos[0]+2,pos[1]) #Shift robot position
                home = (home[0]+2,home[1]) #Shift home position
                for i in range(0,len(unexplored_queue)):
                    unexplored_queue[i]=(unexplored_queue[i][0]+2,unexplored_queue[i][1]) #Shift queued cells position
            nearcell = (pos[0]-2,pos[1]) #Define adjacent cell position
            if (nearcell not in unexplored_queue) and mat.item(nearcell)==0: #If the cell is not queued and not explored yet
                mat.itemset(nearcell,1) #Set as queued
                unexplored_queue.append(nearcell) #Add to queue


        if walls[1]>0: #Bottom wall
            mat.itemset((pos[0],pos[1]+1),1) #Set wall
        else:
            if pos[1]==np.shape(mat)[1]-2:
                mat = np.hstack((mat,np.zeros((np.shape(mat)[0],2)))) #Add 2 rows to the bottom
            nearcell = (pos[0],pos[1]+2) #Define adjacent cell position
            if (nearcell not in unexplored_queue) and mat.item(nearcell)==0: #If the cell is not queued and not explored yet
                mat.itemset(nearcell,1) #Set as queued
                unexplored_queue.append(nearcell) #Add to queue

        if walls[2]>0: #Right wall
            mat.itemset((pos[0]+1,pos[1]),1) #Set wall
        else:
            if pos[0]==np.shape(mat)[0]-2:
                mat = np.vstack((mat,np.zeros((2,np.shape(mat)[1])))) #Add 2 columns to the right
            nearcell = (pos[0]+2,pos[1]) #Define adjacent cell position
            if (nearcell not in unexplored_queue) and mat.item(nearcell)==0: #If the cell is not queued and not explored yet
                mat.itemset(nearcell,1) #Set as queued
                unexplored_queue.append(nearcell) #Add to queue

        if walls[3]>0: #Top wall
            mat.itemset((pos[0],pos[1]-1),1) #Set wall
        else:
            if pos[1]==1:
                mat = np.hstack((np.zeros((np.shape(mat)[0],2)),mat)) #Add 2 rows to the top
                pos = (pos[0],pos[1]+2) #Shift robot position
                home = (home[0],home[1]+2) #Shift home position
                for i in range(0,len(unexplored_queue)):
                    unexplored_queue[i]=(unexplored_queue[i][0],unexplored_queue[i][1]+2) #Shift queued cells position
            nearcell = (pos[0],pos[1]-2) #Define adjacent cell position
            if (nearcell not in unexplored_queue) and mat.item(nearcell)==0: #If the cell is not queued and not explored yet
                mat.itemset(nearcell,1) #Set as queued
                unexplored_queue.append(nearcell) #Add to queue
        ##########
        
        server.setMazeMap(mat.tolist()) #Update map
        
        #Decide where to go
        if len(unexplored_queue)==0: #If there is no available cell to explore, the maze is done
            if pos!=home:
                server.setRobotStatus("Done! Homing...")
                destination=mp.bestPath(orientation,[pos[0],pos[1]],[home],mat) #Find the best path to reach home 
                moveTo(destination)
            server.setRobotStatus("Done!")
            input("Press enter to continue")
            sys.exit()
                
        destination=mp.bestPath(orientation,[pos[0],pos[1]],unexplored_queue,mat) #Find the best path to reach the nearest cell
        
        #Move to destination
        moveTo(destination)
        
        #print(dijkstra([1,1],[3,3],mat))
        #available = [[7,5],[3,1]]
        #print(best_path(1,[1,1],available,mat))
