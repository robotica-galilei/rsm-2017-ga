import math
import pygame
from pygame import gfxdraw

def generate_cursor(c_size, x0, y0):
    robot_cursor = [(c_size, c_size), (0, c_size), (0, 0), (c_size, 0)]
    cursor_fin = []
    for i in range(0,len(robot_cursor)):
        cursor_fin.append((robot_cursor[i][0] + x0, robot_cursor[i][1] + y0))
    return cursor_fin


def draw_pointer(draw_surface, x0,y0, x_coord, y_coord, cell_size, robot_color):
    cursor_size = cell_size * 2 / 3
    robot_pointlist = generate_cursor(cursor_size, x0 + x_coord*cell_size + cell_size/2 - cursor_size/2, y0 + y_coord*cell_size + cell_size/2 - cursor_size/2)
    pygame.draw.aalines(draw_surface, robot_color, True,  robot_pointlist)
