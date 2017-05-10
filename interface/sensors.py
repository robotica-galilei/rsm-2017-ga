from __future__ import division
import pygame
from pygame import gfxdraw
import sys
import math
import robot
import sensorsLayout
import Pyro4
import time

#Server connection
server = Pyro4.Proxy("PYRONAME:robot.server")    # use name server object lookup uri shortcut

#Init
pygame.init()
pygame.display.set_caption('Sensors Check') #Window caption
pygame.mouse.set_visible(False) #Hide mouse cursor
screen = pygame.display.set_mode((sensorsLayout.screen_width,sensorsLayout.screen_height)) #Add pygame.FULLSCREEN as 2nd parameter of this function to get full-screen
clock = pygame.time.Clock()
FPS = 5 #Refreshing rate of the screen
MAX_T = 480 #Match max duration, default 480 seconds

###Match parameters, changed real-time by the main program

tof=(-1,-1,-1,-1)
heat=(0,0,0,0)
toc=(0,0)

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
    check_connection()
    tof=server.getTof()
    heat=server.getHeat()
    toc=server.getToc()

    #Checking for events (Escape key, X button)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    #Window layout
    sensorsLayout.draw_layout(screen)

    robot.drawComplexRobot(screen)
    robot.drawHeatReadings(screen,(0,0,0,0))


    #RENDER
    pygame.display.update()
    clock.tick(FPS)
