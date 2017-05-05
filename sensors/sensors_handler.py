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
    is_there_h, victim_list_h = h.isThereSomeVictim()
    try:
        is_there_v, victim_list_v = h.isThereSomeVideoVictim()
    except Exception:
        is_there_v = False; victim_list_v = [] #TODO comment when implementing video victims
    is_there = is_there_h or is_there_v
    victim_list = []
    victim_list.extend(victim_list_h)
    victim_list.extend(victim_list_v)
    return is_there, victim_list

def are_there_visual_victims_in_the_list(victims):
    return 'HE' in victims or 'SE' in victims or 'UE' in victims or 'HO' in victims or 'SO' in victims or 'UO' in victims

def check_bridge(pos):
    return False
