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
nowall_color = (150, 150, 150)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
blue = (0, 0, 255)
light_blue = (102, 178, 255)

#Settings
screen_width = 800
screen_height = 480
margin = 20
div_factor = 0.7
divider = screen_width*div_factor
info_offset = -20

def render_text(message, foreground_color, background_color, font=None):
    if font is None:
        font = standard_font
    return font.render(message, True, foreground_color, background_color)

def draw_layout(draw_surface, inc_mode):
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
    pygame.draw.rect(draw_surface, panel_color, (divider, 0, screen_width-divider, screen_height))
    pygame.draw.line(draw_surface, divider_color , (divider, 0), (divider,screen_height), 4)
    
    #status_label
    label1 = render_text('Maze', white, panel_color, big_font)
    l1w, l1h = label1.get_size()
    draw_surface.blit(label1,((divider+screen_width)/2 - l1w/2, screen_height/7 -l1h/2))
    label2 = render_text("Designer", white, panel_color, big_font)
    l2w, l2h = label2.get_size()
    draw_surface.blit(label2,((divider+screen_width)/2 - l2w/2, screen_height*2/7 -l2h/2 + info_offset))
    
    #status_label
    label3 = render_text('Sizing' if inc_mode==1 else "Editing", green if inc_mode==1 else red, panel_color, big_font)
    l3w, l3h = label3.get_size()
    draw_surface.blit(label3,((divider+screen_width)/2 - l3w/2, screen_height*3/7 -l3h/2))
    label4 = render_text("mode", white, panel_color, standard_font)
    l4w, l4h = label4.get_size()
    draw_surface.blit(label4,((divider+screen_width)/2 - l4w/2, screen_height*4/7 -l4h/2 + info_offset))

    #Borders
    pygame.draw.line(draw_surface, map_margin_color, (margin, margin), (divider-margin, margin), 1)
    pygame.draw.line(draw_surface, map_margin_color, (divider-margin, margin), (divider-margin, screen_height-margin), 1)
    pygame.draw.line(draw_surface, map_margin_color, (margin, margin), (margin, screen_height-margin), 1)
    pygame.draw.line(draw_surface, map_margin_color, (margin, screen_height-margin), (divider-margin, screen_height-margin), 1)
