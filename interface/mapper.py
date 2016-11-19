import layout
import pygame
from pygame import gfxdraw

min_cell_size = 30 #pixels
max_cell_size = 100 #pixels
max_map_width = int(layout.divider-layout.margin*2) #pixels
max_map_height = int(layout.screen_height-layout.margin*2) #pixels
map_x_start=0
map_y_start=0
cell_size=0
n_lines = 0

def render_text(message, foreground_color, background_color, font=None):
    if font is None:
        font = standard_font
    return font.render(message, True, foreground_color, background_color)

def draw_line(draw_surface, line_color, start_point, end_point, line_thickness, dashed=0):
    global n_lines
    n_lines += 1
    if(dashed==0):
        pygame.draw.line(draw_surface, line_color, start_point, end_point, line_thickness)
    else:
        if start_point[0]!=end_point[0] and start_point[1]!=end_point[1]:
            print("Can not draw oblique dashed lines")
            return 0;
        elif start_point[0]!=end_point[0]:
            for i in range(start_point[0], end_point[0],1):
                if i % 8 == 0:
                    pygame.draw.line(draw_surface, line_color, (i, start_point[1]), (i+4, start_point[1]), line_thickness)
        else:
            for i in range(start_point[1], end_point[1],1):
                if i % 8 == 0:
                    pygame.draw.line(draw_surface, line_color, (start_point[0], i), (start_point[0], i+4), line_thickness)

def draw_cell(draw_surface, x0, y0, x, y, cell_size, wall_map):
    wall_color = [layout.grid_color, layout.grid_color, layout.grid_color, layout.grid_color]
    wall_thickness = [1,1,1,1]
    wall_dashed = [0,0,0,0]

    wall_start_points = [(int(x0 + x*cell_size), int(y0 + y*cell_size) + 4),
                         (int(x0 + x*cell_size) + 4, int(y0 + (y+1)*cell_size)),
                         (int(x0 + (x+1)*cell_size), int(y0 + y*cell_size) + 4),
                         (int(x0 + x*cell_size) + 4, int(y0 + y*cell_size))]
    wall_end_points = [(int(x0 + x*cell_size), int(y0 + (y+1)*cell_size) - 4),
                       (int(x0 + (x+1)*cell_size) - 4, int(y0 + (y+1)*cell_size)),
                       (int(x0+ (x+1)*cell_size), int(y0 + (y+1)*cell_size) - 4),
                       (int(x0 + (x+1)*cell_size) - 4, int(y0 + y*cell_size))]
    print(x, y)
    walls=[]
    walls.append(3 if wall_map[2*x][2*y+1]==1 else 1)
    walls.append(3 if wall_map[2*x+1][2*y+2]==1 else 1)
    walls.append(3 if wall_map[2*x+2][2*y+1]==1 else 1)
    walls.append(3 if wall_map[2*x+1][2*y]==1 else 1)
    #print(walls)
    for i in range(0,4):
        if walls[i]==1:
            wall_color[i]=layout.nowall_color
            wall_thickness[i]=1
        if walls[i]==2:
            wall_color[i]=layout.black
            wall_dashed[i]=1
            wall_thickness[i]=4
        elif walls[i]==3:
            wall_color[i]=layout.black
            wall_thickness[i]=5
            if i==0 or i==2:
                wall_start_points[i]=(wall_start_points[i][0],wall_start_points[i][1]-6)
                wall_end_points[i]=(wall_end_points[i][0],wall_end_points[i][1]+6)
            else:
                wall_start_points[i]=(wall_start_points[i][0]-6,wall_start_points[i][1])
                wall_end_points[i]=(wall_end_points[i][0]+6,wall_end_points[i][1])



    #Walls
    for i in range(0,4):
        if (x==0 and i==0) or (y==0 and i==3) or i==2 or i==1:
            draw_line(draw_surface, wall_color[i], wall_start_points[i], wall_end_points[i], wall_thickness[i], wall_dashed[i])

    #Circles
    check = wall_map[2*x+1][2*y+1] 
    if check>0:
        pygame.gfxdraw.aacircle(draw_surface, int(x0 + x*cell_size + cell_size/2), int(y0 + y*cell_size + cell_size/2), int(cell_size/8),layout.blue if check==1 else layout.green)
        pygame.gfxdraw.filled_circle(draw_surface, int(x0 + x*cell_size + cell_size/2), int(y0 + y*cell_size + cell_size/2), int(cell_size/8),layout.blue if check==1 else layout.green)



def draw_map(draw_surface, wall_map):
    if len(wall_map)%2==0 or len(wall_map[0])%2==0:
        print("Invalid map dimensions.")
        return -1
    
    if len(wall_map) == 0:
        label_empty = render_text('Nothing to render', layout.red, layout.white , layout.big_font)
        lemw, lemh = label_empty.get_size()
        draw_surface.blit(label_empty,(layout.divider/2 - lemw/2, layout.screen_height/2 -lemh/2))
        return -1

    x_cells = (len(wall_map)-1)/2
    y_cells = (len(wall_map[0])-1)/2
    print(x_cells,y_cells)
    cell_width = max_map_width/x_cells
    cell_height = max_map_height/y_cells
    if min(cell_width, cell_height) < min_cell_size:
        label_error = render_text('Map too big', layout.red, layout.white, layout.big_font)
        lew, leh = label_error.get_size()
        draw_surface.blit(label_error,(layout.divider/2 - lew/2, layout.screen_height/2 -leh/2))
        return -1
    else:
        global map_x_start
        global map_y_start
        global cell_size
        cell_size = min(cell_width, cell_height)
        #print (cell_size)
        if cell_size > max_cell_size: cell_size = max_cell_size
        map_width = cell_size * x_cells
        map_height = cell_size * y_cells
        map_x_start = layout.divider/2 - map_width/2
        map_y_start = layout.screen_height/2 - map_height/2
        global n_lines
        n_lines=0
        for i in range(0,y_cells):
            for j in range(0,x_cells):
                #Draw single cell
                draw_cell(draw_surface, map_x_start, map_y_start, j, i, cell_size,wall_map)
        print(n_lines)
        return 1
