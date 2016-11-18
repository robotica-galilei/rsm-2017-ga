import Pyro4
import numpy as np

### THIS SERVER IS USED ONLY TO TRANSMIT DATA TO THE GRAPHICAL INTERFACE AND TO RETRIEVE PROXIMITY SENSORS DATA ###

#Global variables
x_pos=0
y_pos=0
orientation=0
robot_status="Unknown"
victims_number=0
elapsed_time=0

maze_map=[]

@Pyro4.expose
class server(object):
    def ping(self):
        return "Pong"

    def getRobotPosition(self):
        return (x_pos, y_pos)

    def setRobotPosition(self, coords):
        global x_pos
        global y_pos
        if len(coords) < 2:
            print(coords)
            return -1
        else:
            x_pos, y_pos = coords
            return 0

    def getRobotOrientation(self):
        return orientation

    def setRobotOrientation(self, orient):
        global orientation
        orientation=orient
        return 0

    def getRobotStatus(self):
        return robot_status

    def setRobotStatus(self, status_string):
        global robot_status
        robot_status=status_string
        return 0

    def getElapsedTime(self):
        return elapsed_time

    def setElapsedTime(self, e_time):
        global elapsed_time
        elapsed_time = e_time
        return 0

    def getVictimsNumber(self):
        return victims_number

    def setVictimsNumber(self, v_num):
        global victims_number
        victims_number=v_num
        return 0

    def getMazeMap(self):
        return maze_map

    def setMazeMap(self, w_map):
        global maze_map
        maze_map=w_map
        return 0


daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(server)   # register the greeting maker as a Pyro object
ns.register("robot.server", uri)   # register the object with a name in the name server

print("Server ready.")
daemon.requestLoop()
