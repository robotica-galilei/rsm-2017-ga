import numpy as np

#Matrix definition

#Maze n.1
#mat = np.matrix("0 1 0 1 0 1 0 1 0 1 0 1 0; 1 0 0 0 0 0 1 0 0 0 0 0 1; 0 1 0 1 0 0 0 0 0 0 0 0 0; 1 0 0 0 0 0 1 0 0 0 0 0 1; 0 1 0 0 0 1 0 0 0 0 0 0 0; 1 0 0 0 0 0 1 0 0 0 0 0 1; 0 0 0 1 0 1 0 0 0 0 0 0 0; 1 0 0 0 0 0 0 0 0 0 0 0 1; 0 1 0 1 0 1 0 1 0 0 0 1 0; 1 0 0 0 0 0 0 0 0 0 0 0 1; 0 1 0 1 0 1 0 1 0 1 0 1 0")

#maze n.2
#mat = np.matrix("0 1 0 1 0 1 0; 1 0 0 0 0 0 1; 0 0 0 1 0 0 0; 1 0 0 0 0 0 1; 0 0 0 1 0 0 0; 1 0 0 0 0 0 1; 0 1 0 1 0 1 0")

#maze n.3
#mat = np.matrix("0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 0.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0")

#maze n.4
#mat = np.matrix("0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0")

#maze n.5 (Do not use in public presentations: contains Nazi stuff)
#mat=np.matrix("0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0")

#maze n.6 (Do not use in public presentations: contains inappropriate words)
#mat = np.matrix("0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0")

#maze n.7
#mat = np.matrix("0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0")

#maze n.8
#mat = np.matrix("0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0")

#maze n.9
mat = np.matrix("0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 ; 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 ; 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0 1.0 0.0")

#maze
mat = np.matrix("0 1 0 ; 1 0 1 ; 0 1 0")


black = []
victim = [(5,5)]
bridge = [(5,1)]


def scanWalls(pos, orient, tof=None):
    walls=[]
    walls.append(mat.item((pos[0]-1,pos[1])))
    walls.append(mat.item((pos[0],pos[1]+1)))
    walls.append(mat.item((pos[0]+1,pos[1])))
    walls.append(mat.item((pos[0],pos[1]-1)))
    for i in range(0,(orient+1)%4):
        walls.append(walls[0])
        del walls[0]

    #Rectify readings on the orientation of the robot (cyclic permutation)
    for i in range(0,3-orient):
        walls.append(walls[0])
        del walls[0]
    return walls


def check_black(pos):
    return pos in black


def check_victim(pos):
    return pos in victim


def check_bridge(pos):
    return pos in bridge
