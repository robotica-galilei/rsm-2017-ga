import numpy as np

#Matrix definition

#Maze n.1
#mat = np.matrix("0 1 0 1 0 1 0 1 0 1 0 1 0; 1 0 0 0 0 0 1 0 0 0 0 0 1; 0 1 0 1 0 0 0 0 0 0 0 0 0; 1 0 0 0 0 0 1 0 0 0 0 0 1; 0 1 0 0 0 1 0 0 0 0 0 0 0; 1 0 0 0 0 0 1 0 0 0 0 0 1; 0 0 0 1 0 1 0 0 0 0 0 0 0; 1 0 0 0 0 0 0 0 0 0 0 0 1; 0 1 0 1 0 1 0 1 0 0 0 1 0; 1 0 0 0 0 0 0 0 0 0 0 0 1; 0 1 0 1 0 1 0 1 0 1 0 1 0")

#maze n.2
#mat = np.matrix("0 1 0 1 0 1 0; 1 0 0 0 0 0 1; 0 0 0 1 0 0 0; 1 0 0 0 0 0 1; 0 0 0 1 0 0 0; 1 0 0 0 0 0 1; 0 1 0 1 0 1 0")

#maze n.3
mat = np.matrix("0.0 1.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 0.0 0.0 1.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 1.0 0.0 1.0 0.0 ; 1.0 0.0 1.0 0.0 0.0 0.0 1.0 ; 0.0 0.0 0.0 0.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 1.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 0.0 0.0 ; 1.0 0.0 0.0 0.0 0.0 0.0 1.0 ; 0.0 1.0 0.0 1.0 0.0 1.0 0.0")

def scanWalls(pos, orient):
    walls=[]
    walls.append(mat.item((pos[0]-1,pos[1])))
    walls.append(mat.item((pos[0],pos[1]+1)))
    walls.append(mat.item((pos[0]+1,pos[1])))
    walls.append(mat.item((pos[0],pos[1]-1)))
    for i in range(0,(orient+1)%4):
        walls.append(walls[0])
        del walls[0]
    return walls