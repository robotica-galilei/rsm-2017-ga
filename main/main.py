import Pyro4
import sys
import time

server = Pyro4.Proxy("PYRONAME:robot.server")    # use name server object lookup uri shortcut

path = [(0,0,2),(1,0,2),(1,0,1),(1,1,1),(1,2,1),(1,2,0),(0,2,0),(0,2,1),(0,3,1),(0,3,0),(0,3,3),(0,2,3),(0,1,3),(0,1,2),(0,1,1),(0,2,1),(0,2,2),(1,2,2),(2,2,2)]

while True:
	time.sleep(3)
	for i in path:
		server.setRobotPosition((i[0],i[1]))
		server.setRobotOrientation(i[2])
		time.sleep(0.5)
