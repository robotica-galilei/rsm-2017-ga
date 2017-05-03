def scanWalls(pos, orient, tof = None):
    walls=[]
    walls.append(tof.is_there_a_wall('O'))
    walls.append(tof.is_there_a_wall('S'))
    walls.append(tof.is_there_a_wall('E'))
    walls.append(tof.is_there_a_wall('N'))

    #Rectify readings on the orientation of the robot (cyclic permutation)
    for i in range(0,3-orient):
        walls.append(walls[0])
        del walls[0]
    return walls


def check_black(pos, col = None):
    return col.is_cell_black()

def check_victim(pos, h = None):
    return h.isThereSomeVictim()[0]

def check_bridge(pos):
    return False
