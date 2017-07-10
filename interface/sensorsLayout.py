from __future__ import division
import pygame

#Fonts
pygame.init()
standard_font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 50)

#Colors
panel_color = (50, 50, 50)
divider_color = (100, 100, 100)
map_margin_color = (250, 250, 250)
grid_color = (200, 200, 200)
nowall_color = (250, 250, 250)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
blue = (0, 0, 255)
light_blue = (102, 178, 255)
silver = (211,211,211)
almost_black = (15, 15, 15)
light_green = (153, 255, 204)

#Settings
screen_width = 1200
screen_height = 1200
margin = 20
divider = screen_height/2

def render_text(message, foreground_color, background_color, font=None):
    if font is None:
        font = standard_font
    return font.render(message, True, foreground_color, background_color)

def draw_layout(draw_surface):
    global div_factor
    global divider

    #Settings check
    if screen_width < 200:
        print ("Screen too small")
        pygame.quit()
        sys.exit()

    if (1 - div_factor)*screen_width < 180:
        div_factor=(screen_width-180)/screen_width
        divider = screen_width*div_factor
        #print (div_factor)

    #base
    draw_surface.fill(white)
    pygame.draw.line(draw_surface, divider_color , (divider, 0), (divider,screen_height), 4)
