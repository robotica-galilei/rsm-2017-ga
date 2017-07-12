from __future__ import division
import pygame
from pygame import gfxdraw
import sys
import math
import robot
import layout
import mapper
import rospy
import pickle
from std_msgs.msg import String
import time

#Server connection
def callback(data):
    global maze_map
    global robot_orientation
    global z_pos
    global y_pos
    global x_pos
    global robot_status
    global elapsed_time

    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    tag, val = data.data.split(':')
    print(tag, val)
    if tag == "map":
        maze_map = pickle.loads(val.encode("utf-8"))[0]
        allah = [[0 for j in range(len(maze_map))] for i in range(len(maze_map[0]))]
        for i in range(len(maze_map)):
            for j in range(len(maze_map[0])):
                allah[j][i] = maze_map[i][j]

        maze_map = allah
    elif tag == "ori":
        robot_orientation = int(val)
    elif tag == "pos":
        z_pos, y_pos, x_pos = pickle.loads(val.encode("utf-8"))
    elif tag == "tim":
        elapsed_time = int(val)
    elif tag == "sta":
        robot_status = val

#Init
pygame.init()
pygame.display.set_caption('Rescue Maze') #Window caption
pygame.mouse.set_visible(False) #Hide mouse cursor
screen = pygame.display.set_mode((layout.screen_width,layout.screen_height)) #Add pygame.FULLSCREEN as 2nd parameter of this function to get full-screen
clock = pygame.time.Clock()
FPS = 5 #Refreshing rate of the screen
MAX_T = 480 #Match max duration, default 480 seconds

###Match parameters, changed real-time by the main program
rospy.init_node('interface', anonymous=True)
rospy.Subscriber("navigation", String, callback)
robot_status = 'Not connected' #Can be 'Exploring', 'Lost' or whatever you want
robot_orientation = 0 #The orientation of the robot, integer number from 0 to 3
x_pos = 0 ##Robot coords in the matrix
y_pos = 0 ##
z_pos = 0
n_victims = 0 #Useless, simply shows on the screen the number of victims found
elapsed_time = 0
maze_map = [[0,0,0],[0,0,0],[0,0,0]]

###End of match parameters

#Test connection
def check_connection():
    try:
        server.ping()
    except Exception as e:
        print(e)
        import errorscreen
        errorscreen.show_error(screen)
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        sys.exit()


while True:
    #Retrieve data from server
    #check_connection()
    '''
    z_pos, y_pos, x_pos = server.getRobotPosition()
    robot_orientation = server.getRobotOrientation()
    robot_status = server.getRobotStatus()
    n_victims = server.getVictimsNumber()
    elapsed_time = server.getElapsedTime()
    maze_map = server.getMazeMap()[0]
    '''
    print(x_pos, y_pos)

    #Checking for events (Escape key, X button)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    #Window layout
    layout.draw_layout(screen, robot_status, n_victims, elapsed_time, MAX_T)

    #The map
    if(mapper.draw_map(screen, maze_map)==1):
        #The robot
        robot.draw_robot(screen, mapper.map_x_start, mapper.map_y_start, (x_pos-1)/2, (y_pos-1)/2, mapper.cell_size, robot_orientation, layout.light_blue)


    #RENDER
    pygame.display.update()
    clock.tick(FPS)
