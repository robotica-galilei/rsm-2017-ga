from __future__ import division
import pygame
from pygame import gfxdraw
import sys
import math
import layout
import selected
import mapper
import time
import numpy as np

#Init
pygame.init()
pygame.display.set_caption('Rescue Maze') #Window caption
pygame.mouse.set_visible(False) #Hide mouse cursor
screen = pygame.display.set_mode((layout.screen_width,layout.screen_height)) #Add pygame.FULLSCREEN as 2nd parameter of this function to get full-screen
clock = pygame.time.Clock()
FPS = 10 #Refreshing rate of the screen
MAX_T = 480 #Match max duration, default 480 seconds

###Match parameters, changed real-time by the main program

def saveMaze():
    mat=""
    for i in range(0,np.shape(maze_map)[0]):
        for j in range(0,np.shape(maze_map)[1]):
            mat += str(maze_map.item((i,j))) + " "
        if i<np.shape(maze_map)[0]-1:
            mat += "; "
    print(mat)

maze_map = np.matrix("0 0 0; 0 0 0; 0 0 0")
expansion_mode=1
pos=(1,1)

while True:
    #Checking for events (Escape key, X button)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            print("Key pressed")
            if event.key==32:
                if expansion_mode==0:
                    expansion_mode=1
                else:
                    expansion_mode=0
            elif event.key==13:
                saveMaze()
            if expansion_mode==0:
                if event.key==119:
                    if pos[1] > 1:
                        pos=(pos[0],pos[1]-2)
                elif event.key==115:
                    if pos[1] < np.shape(maze_map)[1]-2:
                        pos=(pos[0],pos[1]+2)
                elif event.key==100:
                    if pos[0] < np.shape(maze_map)[0]-2:
                        pos=(pos[0]+2,pos[1])
                elif event.key==97:
                    if pos[0] > 1:
                        pos=(pos[0]-2,pos[1])
                elif event.key==274:
                    wall_pos=(pos[0],pos[1]+1)
                    if maze_map.item(wall_pos)==0:
                        maze_map.itemset(wall_pos,1)
                    else:
                        maze_map.itemset(wall_pos,0)
                elif event.key==276:
                    wall_pos=(pos[0]-1,pos[1])
                    if maze_map.item(wall_pos)==0:
                        maze_map.itemset(wall_pos,1)
                    else:
                        maze_map.itemset(wall_pos,0)
                elif event.key==275:
                    wall_pos=(pos[0]+1,pos[1])
                    if maze_map.item(wall_pos)==0:
                        maze_map.itemset(wall_pos,1)
                    else:
                        maze_map.itemset(wall_pos,0)
                elif event.key==273:
                    wall_pos=(pos[0],pos[1]-1)
                    if maze_map.item(wall_pos)==0:
                        maze_map.itemset(wall_pos,1)
                    else:
                        maze_map.itemset(wall_pos,0)
                else:
                    print(event.key)
            else:
                if event.key==261 or event.key==115:
                    maze_map = np.hstack((maze_map,np.zeros((np.shape(maze_map)[0],2))))
                elif event.key==260 or event.key==97:
                    maze_map = np.vstack((np.zeros((2,np.shape(maze_map)[1])),maze_map))
                    pos = (pos[0]+2,pos[1])
                elif event.key==262 or event.key==100:
                    wall_pos=(pos[0]+1,pos[1])
                    maze_map = np.vstack((maze_map,np.zeros((2,np.shape(maze_map)[1]))))
                elif event.key==264 or event.key==119:
                    maze_map = np.hstack((np.zeros((np.shape(maze_map)[0],2)),maze_map))
                    pos = (pos[0],pos[1]+2)
                else:
                    print(event.key)


    #print(pos)

    #Window layout
    layout.draw_layout(screen,expansion_mode)

    #The map
    if(mapper.draw_map(screen, maze_map.tolist())==1) and expansion_mode==0:
        selected.draw_pointer(screen, mapper.map_x_start, mapper.map_y_start, (pos[0]-1)/2, (pos[1]-1)/2, mapper.cell_size, layout.light_blue)


    #RENDER
    pygame.display.update()
    clock.tick(FPS)
