def scanWalls(pos, orient, tof):
    walls=[]
    walls.append(tof.is_there_a_wall('N'))
    walls.append(tof.is_there_a_wall('E'))
    walls.append(tof.is_there_a_wall('S'))
    walls.append(tof.is_there_a_wall('O'))

    #Rectify readings on the orientation of the robot (cyclic permutation)
    for i in range(0,3-orient):
        walls.append(walls[0])
        del walls[0]


def check_black(pos):
    return False

def check_victim(pos):
    return False

def check_bridge(pos):
    return False
