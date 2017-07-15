from __future__ import division
import time
import maps
from PIL import Image
from PIL import ImageDraw
from Adafruit_LED_Backpack import BicolorMatrix8x8

class displayMatrix:
    def __init__(self):
        self.display = BicolorMatrix8x8.BicolorMatrix8x8()
        self.display.begin()
        self.shutDown()
        self.colors=[BicolorMatrix8x8.RED, BicolorMatrix8x8.GREEN, BicolorMatrix8x8.YELLOW, BicolorMatrix8x8.OFF]


    def flash(self,n_blink=2,freq=4):
        period=1
        if freq>0:
            period=1/freq
        for i in range(n_blink):
            self.display.clear()
            for x in range(8):
                for y in range(8):
                    self.display.set_pixel(x,y,self.colors[0])
            self.display.write_display()
            time.sleep(period/2)
            self.display.clear()
            self.display.write_display()
            time.sleep(period/2)

    def drawMap(self,bitmap,color,render=True):
        c=self.colors[color]
        for y in range(8):
            row=list(bitmap[y])
            print(row)
            for x in range(8):
                if row[x]=='1':
                    self.display.set_pixel(x, y, c)
        if render:
            self.display.write_display()

    def drawWall(self,n,color=1,render=True):
        c=self.colors[color]
        walls=[((0,0),(0,7)),((0,7),(7,7)),((7,7),(0,7)),((0,7),(0,0))]
        selected_wall=walls[n]
        for y in range(selected_wall[1][0],selected_wall[1][1]+1):
            for x in range(selected_wall[0][0],selected_wall[0][1]+1):
                self.display.set_pixel(x,y,c)
        if render:
            self.display.write_display()

    def sigFuckYou(self):
        self.display.clear()
        self.drawMap(maps.swasti,0)

    def sigDone(self):
        self.display.clear()
        self.drawMap(maps.tick,1)

    def sigTime(self,minutes):
        if minutes<0 or minutes >8:
            return -1
        self.display.clear()
        self.drawMap(maps.numbers[minutes],(0 if minutes<=2 else 2) if minutes<=4 else 1)

    def sigLost(self):
        self.display.clear()
        self.drawMap(maps.lost,0)

    def sigHome(self,status=0):
        self.display.clear()
        self.drawMap(maps.home,status)

    def sigWalls(self,walls):
        self.display.clear()
        for i in range(4):
            if walls[i]==1:
                self.drawWall(i,render=False)
        self.drawMap(maps.robot,2)


    def sigDirection(self,dir,status=1):
        self.display.clear()
        arrow_maps=[maps.left,maps.back,maps.right,maps.fwd]
        self.drawMap(arrow_maps[dir],2 if status==1 else 1)


    def sigVictim(self,victimtype=None,side=None):
        self.flash()
        if victimtype!=None:
            vic_maps={'O':maps.heat,'H':maps.visH,'S':maps.visS,'U':maps.visU}
            self.drawMap(vic_maps[victimtype],0,render=False)
            if side!=None:
                for i in range(3):
                    self.drawWall(side)
                    time.sleep(0.2)
                    self.drawWall(side,color=3)
                    time.sleep(0.2)
                self.drawWall(side)
            else:
                self.display.write_display()

    def shutDown(self):
        self.display.clear()
        self.display.write_display()
