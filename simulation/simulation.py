import sensors

wall_map = [[[3,3,1,3],[1,1,3,3],[3,0,0,0],[0,0,0,0]], #THIS WILL BE CHANGED
    [[3,1,3,3],[3,1,3,1],[3,3,0,0],[0,0,0,0],], #Matrix containing walls informations, 4 chars string, starting from the left, going anti-clockwise
    [[3,1,1,1],[1,3,1,1],[1,3,2,3],[2,0,0,0]], #0 - unknown, 1 - No wall, 2 - Queued wall, 3 - Wall
    [[3,3,3,1],[3,0,0,3],[0,0,0,3],[0,0,0,0]],
    [[0,0,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]

def getWalls(x, y, orient):
    wall_list = wall_map[x][y]
    for i in range(0,orient):
        wall_list.append(wall_list[0])
        wall_lit.pop(0)
    return ''.join(wall_list)