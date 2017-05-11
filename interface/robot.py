import math
import pygame
import sensorsLayout
from pygame import gfxdraw

def rotate_point(origin, point, angle):
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def generate_cursor(c_size, c_orient, x0, y0):
    robot_cursor = [(c_size, c_size), (0, int(c_size/2)), (c_size, 0), (int(c_size*3/4), int(c_size/2)), (c_size, c_size)]
    cursor_rot = []
    for i in robot_cursor:
        cursor_rot.append(rotate_point((int(c_size/2), int(c_size/2)),i,-c_orient*math.pi/2))
    cursor_fin = []
    for i in range(0,len(robot_cursor)):
        cursor_fin.append((cursor_rot[i][0] + x0, cursor_rot[i][1] + y0))
    return cursor_fin

def generate_complexRobot(c_size,x0,y0):
    c_size2=int(c_size*2/3)
    c_size3=int(c_size/3)
    robot_cursor = [(c_size, c_size), (0, c_size), (0, 0), (c_size,0), (c_size, c_size)]
    robot_mask = [(0,c_size2),(0,c_size3),(c_size3,0),(c_size2,0),(c_size,c_size3),(c_size,c_size2),(c_size2,c_size),(c_size3,c_size),(0,c_size2)]
    finCur=[(i[0]+x0,i[1]+y0) for i in robot_cursor]
    finMask=[(i[0]+x0,i[1]+y0) for i in robot_mask]
    return (finCur,finMask)

def draw_robot(draw_surface, x0,y0, x_coord, y_coord, cell_size, orientation, robot_color):
    cursor_size = cell_size * 2 / 3
    robot_pointlist = generate_cursor(cursor_size, orientation, x0 + x_coord*cell_size + cell_size/2 - cursor_size/2, y0 + y_coord*cell_size + cell_size/2 - cursor_size/2)
    pygame.gfxdraw.aapolygon(draw_surface, robot_pointlist, robot_color)
    pygame.gfxdraw.filled_polygon(draw_surface, robot_pointlist, robot_color)

def drawComplexRobot(draw_surface):
    rob_size = sensorsLayout.divider/4
    robot_pointlist = generate_complexRobot(rob_size, sensorsLayout.divider/2 - rob_size/2, sensorsLayout.screen_height/2 - rob_size/2)
    pygame.gfxdraw.aapolygon(draw_surface, robot_pointlist[0],sensorsLayout.grid_color)
    pygame.gfxdraw.filled_polygon(draw_surface, robot_pointlist[0], sensorsLayout.grid_color)
    pygame.gfxdraw.aapolygon(draw_surface, robot_pointlist[1],sensorsLayout.light_green)
    pygame.gfxdraw.filled_polygon(draw_surface, robot_pointlist[1], sensorsLayout.light_green)

def drawTofReadings(draw_surface,tofReadings):
    pass

def tempToColor(temperature):
    return(int(temperature*255),0,255-int(temperature*255))

def drawHeatReadings(draw_surface,heatReadings):
    temp_interval=(20,40)
    heatReadings=[max(temp_interval[0],i) for i in heatReadings]
    heatReadings=[min(temp_interval[1],i) for i in heatReadings]
    cones=[]
    #EAST Cone
    east_pointlist=[(0,int(sensorsLayout.divider*2/3)),(0,int(sensorsLayout.divider/3)),(int(sensorsLayout.divider*3/8),int(sensorsLayout.screen_height/2)),(0,int(sensorsLayout.divider*2/3))]
    east_color=tempToColor((heatReadings[0]-temp_interval[0])/(temp_interval[1]-temp_interval[0]))
    cones.append((east_pointlist,east_color))

    #SOUTH Cone
    south_pointlist=[(int(sensorsLayout.divider*2/3),sensorsLayout.screen_height),(int(sensorsLayout.divider/3),sensorsLayout.screen_height),(int(sensorsLayout.divider/2),int(sensorsLayout.screen_height*5/8)),(int(sensorsLayout.divider*2/3),sensorsLayout.screen_height)]
    south_color=tempToColor((heatReadings[1]-temp_interval[0])/(temp_interval[1]-temp_interval[0]))
    cones.append((south_pointlist,south_color))

    #WEST Cone
    west_pointlist=[(sensorsLayout.divider,int(sensorsLayout.screen_height/3)),(sensorsLayout.divider,int(sensorsLayout.screen_height*2/3)),(int(sensorsLayout.screen_height*5/8),int(sensorsLayout.screen_height/2)),(sensorsLayout.divider,int(sensorsLayout.divider/3))]
    west_color=tempToColor((heatReadings[2]-temp_interval[0])/(temp_interval[1]-temp_interval[0]))
    cones.append((west_pointlist,west_color))

    #NORTH Cone
    north_pointlist=[(int(sensorsLayout.divider/3),0),(int(sensorsLayout.divider*2/3),0),(int(sensorsLayout.divider/2),int(sensorsLayout.screen_height*3/8)),(int(sensorsLayout.divider/3),0)]
    north_color=tempToColor((heatReadings[3]-temp_interval[0])/(temp_interval[1]-temp_interval[0]))
    cones.append((north_pointlist,north_color))

    print (cones)
    #draw
    for i in cones:
        print (type(i))
        pygame.gfxdraw.aapolygon(draw_surface, i[0],i[1])
        pygame.gfxdraw.filled_polygon(draw_surface, i[0], i[1])
