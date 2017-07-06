import time
import maps
from PIL import Image
from PIL import ImageDraw
from Adafruit_LED_Backpack import BicolorMatrix8x8
display = BicolorMatrix8x8.BicolorMatrix8x8()
display.begin()
colors=[BicolorMatrix8x8.RED, BicolorMatrix8x8.GREEN, BicolorMatrix8x8.YELLOW]

def drawMap(map,color):
    c=colors[color]
    display.clear()
    for x in range(8):
        row=list(map[x])
        print(row)
        for y in range(8):
            if row[y]=='1':
                display.set_pixel(x, 7-y, c)
    display.write_display()

def drawWall(n,color):
    c=colors[color]
    display.set_pixel(0,0,c)
    display.write_display()


def goForward():
    drawMap(maps.fwd,1)

def goLeft():
    drawMap(maps.left,1)

def goRight():
    drawMap(maps.right,1)

def goBack():
    drawMap(maps.back,1)

def goHome():
    drawMap(maps.home,2)

def gotHome():
    drawMap(maps.home,1)

def hotVictim():
    drawMap(maps.heat,2)

def unharmedVictim():
    drawMap(maps.visU,2)

def harmedVictim():
    drawMap(maps.visH,2)

def stableVictim():
    drawMap(maps.visS,2)

"""
goForward()
time.sleep(1)
goLeft()
time.sleep(1)
goRight()
time.sleep(1)
goBack()
time.sleep(1)
goHome()
time.sleep(1)
gotHome()
"""
stableVictim()
drawWall(0,0)
