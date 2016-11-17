import Pyro4
import sys
import time

server = Pyro4.Proxy("PYRONAME:robot.server")    # use name server object lookup uri shortcut


wall_map = [[[3,3,1,3],[1,1,3,3],[3,0,0,0],[0,0,0,0]], #THIS WILL BE CHANGED
    [[3,1,3,3],[3,1,3,1],[3,3,0,0],[0,0,0,0],], #Matrix containing walls informations, 4 chars string, starting from the left, going anti-clockwise
    [[3,1,1,1],[1,3,1,1],[1,3,2,3],[2,0,0,0]], #0 - unknown, 1 - No wall, 2 - Queued wall, 3 - Wall
    [[3,3,3,1],[3,0,0,3],[0,0,0,3],[0,0,0,0]],
    [[0,0,0,3],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]

path = [(0,0,2),(1,0,2),(1,0,1),(1,1,1),(1,2,1),(1,2,0),(0,2,0),(0,2,1),(0,3,1),(0,3,0),(0,3,3),(0,2,3),(0,1,3),(0,1,2),(0,1,1),(0,2,1),(0,2,2),(1,2,2),(2,2,2)]


server.setRobotStatus("Waiting for start")
server.setVictimsNumber(0)
server.setWallMap(wall_map)
server.setElapsedTime(0)

time.sleep(3)


while True:
    server.setRobotStatus("Exploring")
    for i in path:
        server.setRobotPosition((i[0],i[1]))
        server.setRobotOrientation(i[2])
        time.sleep(0.5)
    server.setRobotStatus("Lack of progress")
    time.sleep(3)
