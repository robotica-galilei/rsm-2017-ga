from __future__ import division
__author__ = 'Daniele Gottardini'


import pygame
from pygame import gfxdraw
import sys
import math

#Robot cursor
def rotate(origin, point, angle):
	ox, oy = origin
	px, py = point
	qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
	qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
	return qx, qy

def generate_cursor(c_size, c_orient, x0, y0):
	robot_cursor = [(c_size, c_size), (0, int(c_size/2)), (c_size, 0), (int(c_size*3/4), int(c_size/2)), (c_size, c_size)]
	cursor_rot = []	
	for i in robot_cursor:
		cursor_rot.append(rotate((int(c_size/2), int(c_size/2)),i,-c_orient*math.pi/2))
	cursor_fin = []
	for i in range(0,len(robot_cursor)):
		cursor_fin.append((cursor_rot[i][0] + x0, cursor_rot[i][1] + y0))
	return cursor_fin

#Colors
panel_color = (50, 50, 50)
divider_color = (100, 100, 100)
map_margin_color = (150, 150, 150)
grid_color = (200, 200, 200)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
blue = (0, 0, 255)
light_blue = (102, 178, 255)

#Settings
MAX_T = 480
screen_width = 800
screen_height = 480
if screen_width < 200:
	print ("Screen too small")
	pygame.quit()
	sys.exit()
margin = 20
div_factor = 0.7
if (1 - div_factor)*screen_width < 180:
	div_factor=(screen_width-180)/screen_width
	print (div_factor)
divider = screen_width*div_factor
info_offset = -20
min_cell_size = 30 #pixels
max_cell_size = 100 #pixels
max_map_width = int(divider-margin*2) #pixels
max_map_height = int(screen_height-margin*2) #pixels

#init
pygame.init()
pygame.display.set_caption('Rescue Maze')
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
FPS = 5

#GLOBAL PARAMETERS
robot_status = 'Exploring'
robot_orientation = 1
x_pos = 1
y_pos = 1
n_victims = 0
start_time = pygame.time.get_ticks()
x_cells=3
y_cells=3
wall_map = [['2202','0022','2000'],
	['0012','1110','1000'],
	['0000','0001','0000']]
node_map = [[2,2,0],
	[1,2,1],
	[0,1,0]]
	

#Fonts
standard_font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 50)

def draw_robot(x0,y0, x_coord, y_coord, cell_size, orientation):
	cursor_size = cell_size * 2 / 3
	robot_pointlist = generate_cursor(cursor_size, orientation, x0 + x_coord*cell_size + cell_size/2 - cursor_size/2, y0 + y_coord*cell_size + cell_size/2 - cursor_size/2)
	#print (robot_pointlist)
	pygame.gfxdraw.filled_polygon(screen, robot_pointlist, light_blue)
	pygame.gfxdraw.aapolygon(screen, robot_pointlist, light_blue)

def draw_line(draw_surface, line_color, start_point, end_point, line_thickness, dashed=0):
	if(dashed==0):
		pygame.draw.line(draw_surface, line_color, start_point, end_point, line_thickness)
	else:
		if start_point[0]!=end_point[0] and start_point[1]!=end_point[1]:
			print ("Can not draw oblique dashed lines")
			return 0;
		elif start_point[0]!=end_point[0]:
			for i in range(start_point[0], end_point[0], 1):
				if i % 8 == 0:
					pygame.draw.line(draw_surface, line_color, (i, start_point[1]), (i+4, start_point[1]), line_thickness)
		else:
			for i in range(start_point[1], end_point[1], 1):
				if i % 8 == 0:
					pygame.draw.line(draw_surface, line_color, (start_point[0], i), (start_point[0], i+4), line_thickness)

def draw_cell(x0, y0, x, y, cell_size, walls, check):
	wall_list = list(walls)
	wall_color = [grid_color, grid_color, grid_color, grid_color]
	wall_thickness = [1,1,1,1]
	wall_dashed = [0,0,0,0]
	for i in range(0,4):
		if wall_list[i]=='1':
			wall_color[i]=blue
			wall_dashed[i]=1
			wall_thickness[i]=4
		elif wall_list[i]=='2':
			wall_color[i]=black
			wall_thickness[i]=5

	#Walls
	draw_line(screen, wall_color[0], (int(x0 + x*cell_size), int(y0 + y*cell_size)), (int(x0 + x*cell_size), int(y0 + (y+1)*cell_size)), wall_thickness[0], wall_dashed[0])
	draw_line(screen, wall_color[1], (int(x0 + x*cell_size), int(y0 + (y+1)*cell_size)), (int(x0 + (x+1)*cell_size), int(y0 + (y+1)*cell_size)), wall_thickness[1], wall_dashed[1])
	draw_line(screen, wall_color[2], (int(x0+ (x+1)*cell_size), int(y0 + y*cell_size)), (int(x0 + (x+1)*cell_size), int(y0 + (y+1)*cell_size)), wall_thickness[2], wall_dashed[2])
	draw_line(screen, wall_color[3], (int(x0 + x*cell_size), int(y0 + y*cell_size)), (int(x0 + (x+1)*cell_size), int(y0 + y*cell_size)), wall_thickness[3], wall_dashed[3])
	
	#Circles
	if check>0:
		pygame.gfxdraw.filled_circle(screen, int(x0 + x*cell_size + cell_size/2), int(y0 + y*cell_size + cell_size/2), int(cell_size/8),blue if check==1 else green)
		pygame.gfxdraw.aacircle(screen, int(x0 + x*cell_size + cell_size/2), int(y0 + y*cell_size + cell_size/2), int(cell_size/8),blue if check==1 else green)

def render_text(message, foreground_color, background_color, font=None):
	if font is None:
		font = standard_font
	return font.render(message, True, foreground_color, background_color)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			pygame.quit()
			sys.exit()
	
	#base
	screen.fill(white)
	pygame.draw.rect(screen, panel_color, (divider, 0, screen_width-divider, screen_height))
	pygame.draw.line(screen, divider_color , (divider, 0), (divider,screen_height), 4)
	
	#status_label
	label1 = render_text('Status', white, panel_color, big_font)
	l1w, l1h = label1.get_size()
	screen.blit(label1,((divider+screen_width)/2 - l1w/2, screen_height/7 -l1h/2))
	label2 = render_text(robot_status, green if robot_status != 'Lost' else red, panel_color, standard_font)
	l2w, l2h = label2.get_size()
	screen.blit(label2,((divider+screen_width)/2 - l2w/2, screen_height*2/7 -l2h/2 + info_offset))

	#victims_label
	label3 = render_text('Victims', white, panel_color, big_font)
	l3w, l3h = label3.get_size()
	screen.blit(label3,((divider+screen_width)/2 - l3w/2, screen_height*3/7 -l3h/2))
	label4 = render_text(str(n_victims), green, panel_color, big_font)
	l4w, l4h = label4.get_size()
	screen.blit(label4,((divider+screen_width)/2 - l4w/2, screen_height*4/7 -l4h/2 + info_offset))

	#time_label
	label5 = render_text('Time', white, panel_color, big_font)
	l5w, l5h = label5.get_size()
	screen.blit(label5,((divider+screen_width)/2 - l5w/2, screen_height*5/7 -l5h/2))
	elapsed_time = (pygame.time.get_ticks() - start_time)/1000
	elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
	if elapsed_time < MAX_T -60:
		timer_color = green
	elif elapsed_time < MAX_T:
		timer_color = orange
	else:
		timer_color = red	
	label6 = render_text(str(int(elapsed_minutes)) + ":" + str("%02d" % int(elapsed_seconds)), timer_color, panel_color, big_font)
	l6w, l6h = label6.get_size()
	screen.blit(label6,((divider+screen_width)/2 - l6w/2, screen_height*6/7 -l6h/2 + info_offset))
	

	#THE MAP

	#Borders
	pygame.draw.line(screen, map_margin_color, (margin, margin), (divider-margin, margin), 1)
	pygame.draw.line(screen, map_margin_color, (divider-margin, margin), (divider-margin, screen_height-margin), 1)
	pygame.draw.line(screen, map_margin_color, (margin, margin), (margin, screen_height-margin), 1)
	pygame.draw.line(screen, map_margin_color, (margin, screen_height-margin), (divider-margin, screen_height-margin), 1)

	#Cells
	cell_width = max_map_width/x_cells
	cell_height = max_map_height/y_cells
	if min(cell_width, cell_height) < min_cell_size:
		label_error = render_text('Map too big for rendering', red, black, big_font)
		lew, leh = label_error.get_size()
		screen.blit(label_error,(divider/2 - lew/2, screen_height/2 -leh/2))
	else:
		cell_size = min(cell_width, cell_height)
		#print (cell_size)
		if cell_size > max_cell_size: cell_size = max_cell_size
		map_width = cell_size * x_cells
		map_height = cell_size * y_cells
		map_x_start = divider/2 - map_width/2
		map_y_start = screen_height/2 - map_height/2
		for i in range(0,y_cells):
			for j in range(0,x_cells):
				#Draw single cell
				draw_cell(map_x_start, map_y_start, j, i, cell_size,wall_map[i][j],node_map[i][j])
		draw_robot(map_x_start, map_y_start, x_pos, y_pos, cell_size, robot_orientation)
				
		
	#RENDER
	pygame.display.update()
	clock.tick(FPS)
