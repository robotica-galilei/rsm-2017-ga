import Pyro4
import sys
import time
import numpy as np
import simulation.sensors as sm
import algorithms.motion_planning as mp


def moveTo(path):
    global pos
    global orientation
    for i in path[1]:
        if i!=pos:
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
    mat = np.matrix("0 0 0; 0 0 0; 0 0 0")
    pos = (1,1)
    home = (1,1)
    orientation=3
    unexplored_queue=[]
    print(mat)
    
    server = Pyro4.Proxy("PYRONAME:robot.server")    # use name server object lookup uri shortcut
    server.setRobotStatus("Waiting for start")
    server.setRobotPosition(pos)
    server.setVictimsNumber(0)
    server.setElapsedTime(0)
    
    server.setMazeMap(mat.tolist())
    server.setRobotOrientation(orientation)
    input("Continue...")
    while True:
        #Read sensors
        walls = sm.scanWalls(pos,orientation)
        mat.itemset(pos,2)
        if pos in unexplored_queue:
            unexplored_queue.remove(pos)
        #print(walls)

        #Rectify readings on the orientation
        for i in range(0,3-orientation):
            walls.append(walls[0])
            del walls[0]
        #print(walls)

        #Resize map, shift indexes, add walls and cells to queue
        if walls[0]>0:
            mat.itemset((pos[0]-1,pos[1]),1)
        else:
            if pos[0]==1:
                mat = np.vstack((np.zeros((2,np.shape(mat)[1])),mat))
                pos = (pos[0]+2,pos[1])
                home = (home[0]+2,home[1])
                for i in range(0,len(unexplored_queue)):
                    unexplored_queue[i]=(unexplored_queue[i][0]+2,unexplored_queue[i][1])
            nearcell = (pos[0]-2,pos[1])
            if (nearcell not in unexplored_queue) and mat.item(nearcell)==0:
                mat.itemset(nearcell,1)
                unexplored_queue.append(nearcell)


        if walls[1]>0:
            mat.itemset((pos[0],pos[1]+1),1)
        else:
            if pos[1]==np.shape(mat)[1]-2:
                mat = np.hstack((mat,np.zeros((np.shape(mat)[0],2))))
            nearcell = (pos[0],pos[1]+2)
            if (nearcell not in unexplored_queue) and mat.item(nearcell)==0:
                mat.itemset(nearcell,1)
                unexplored_queue.append(nearcell)

        if walls[2]>0:
            mat.itemset((pos[0]+1,pos[1]),1)
        else:
            if pos[0]==np.shape(mat)[0]-2:
                mat = np.vstack((mat,np.zeros((2,np.shape(mat)[1]))))
            nearcell = (pos[0]+2,pos[1])
            if (nearcell not in unexplored_queue) and mat.item(nearcell)==0:
                mat.itemset(nearcell,1)
                unexplored_queue.append(nearcell)

        if walls[3]>0:
            mat.itemset((pos[0],pos[1]-1),1)
        else:
            if pos[1]==1:
                mat = np.hstack((np.zeros((np.shape(mat)[0],2)),mat))
                pos = (pos[0],pos[1]+2)
                home = (home[0],home[1]+2)
                for i in range(0,len(unexplored_queue)):
                    unexplored_queue[i]=(unexplored_queue[i][0],unexplored_queue[i][1]+2)
            nearcell = (pos[0],pos[1]-2)
            if (nearcell not in unexplored_queue) and mat.item(nearcell)==0:
                mat.itemset(nearcell,1)
                unexplored_queue.append(nearcell)

        server.setMazeMap(mat.tolist())
        #print(mat,unexplored_queue)
        
        #Best path
        if len(unexplored_queue)==0:
            destination=mp.bestPath(orientation,[pos[0],pos[1]],[home],mat)
            moveTo(destination)
            sys.exit()
                
        destination=mp.bestPath(orientation,[pos[0],pos[1]],unexplored_queue,mat)
        print(destination)
        
        #Move to destination
        moveTo(destination)
        
        #print(dijkstra([1,1],[3,3],mat))
        #available = [[7,5],[3,1]]
        #print(best_path(1,[1,1],available,mat))
