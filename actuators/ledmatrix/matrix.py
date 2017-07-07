from __future__ import division
import time
import maps
from PIL import Image
from PIL import ImageDraw
from Adafruit_LED_Backpack import BicolorMatrix8x8
display = BicolorMatrix8x8.BicolorMatrix8x8()
display.begin()
colors=[BicolorMatrix8x8.RED, BicolorMatrix8x8.GREEN, BicolorMatrix8x8.YELLOW]


def flash(n_blink=2,freq=4):
    period=1
    if freq>0:
        period=1/freq
    for i in range(n_blink):
        display.clear()
        for x in range(8):
            for y in range(8):
                display.set_pixel(x,y,colors[0])
        display.write_display()
        time.sleep(period/2)
        display.clear()
        display.write_display()
        time.sleep(period/2)


def drawMap(map,color):
    c=colors[color]
    display.clear()
    for y in range(8):
        row=list(map[y])
        print(row)
        for x in range(8):
            if row[x]=='1':
                display.set_pixel(x, y, c)
    display.write_display()

def drawWall(n,color=1):
    c=colors[color]
    walls=[((0,0),(0,7)),((0,7),(7,7)),((7,7),(0,7)),((0,7),(0,0))]
    selected_wall=walls[n]
    for y in range(selected_wall[1][0],selected_wall[1][1]+1):
        for x in range(selected_wall[0][0],selected_wall[0][1]+1):
            display.set_pixel(x,y,c)
    display.write_display()

def sigTime(minutes):
    if minutes<0 or minutes >8:
        return -1
    display.clear()
    display.write_display()
    drawMap(maps.numbers[minutes],(0 if minutes<=2 else 2) if minutes<=4 else 1)

def sigLost():
    display.clear()
    display.write_display()
    drawMap(maps.lost,0)

def sigHome(status=0):
    display.clear()
    display.write_display()
    drawMap(maps.home,status)

def sigWalls(walls):
    display.clear()
    display.write_display()
    for i in range(4):
        if walls[i]==1:
            drawWall(i)


def sigDirection(dir,status=1):
    display.clear()
    display.write_display()
    arrow_maps=[maps.left,maps.back,maps.right,maps.fwd]
    drawMap(arrow_maps[dir],2 if status==1 else 1)


def sigVictim(victimtype=None,side=None):
    display.clear()
    display.write_display()
    flash()
    if victimtype!=None:
        vic_maps={'O':maps.heat,'H':maps.visH,'S':maps.visS,'U':maps.visU}
        drawMap(vic_maps[victimtype],0)
        if side!=None:
            drawWall(side)

while(True):
    display.clear()
    display.write_display()
    raw_input("Continue")
    for i in range(9):
        sigTime(i)
        time.sleep(1)
    sigLost()
    time.sleep(2)
    sigHome(1)
    time.sleep(1)
    wall_list=[1,1,1,1]
    sigWalls(wall_list)
    time.sleep(2)
    vict_list=['O','H','S','U']
    for i in range(4):
        sigDirection(i,2)
        time.sleep(1)

    for i in range(4):
        for j in range(4):
            sigVictim(vict_list[i],j)
            time.sleep(1)
