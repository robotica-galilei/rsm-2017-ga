import curses
import actuators.motors as motors


def set_cont(cont_n, n_max, x):
    if cont_n+x==n_max or cont_n+x==0:
        cont_n = cont_n
    else:
        cont_n+=x
    return cont_n


pins ={'fl':'P8_13','fr':'P8_19','rl':'P9_14','rr':'P9_16','dir_fl':'gpio31','dir_fr':'gpio48','dir_rl':'gpio60','dir_rr':'gpio30'}
m=motors.Motor()

# get the curses screen window
screen = curses.initscr()

# turn off input echoing
curses.noecho()

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)
v_standart=100 #hahaha standarTTTTTT
v = 0
x=1
y=1
x_max=5
y_max=5
v_max=5
z=False
P=2

try:
    while True:



        char = screen.getch()
        if char == ord('q'):
            v=0
            cont_v = 1
            cont_x = 1
            cont_y = 1


        for i in range (v_max):
            if char == ord(string(i)):
                screen.addstr(0, 0, string)
                cont_v = i

        elif char == curses.KEY_LEFT:
            # print doesn't work with curses, use addstr instead
            x = -2*cont_x/x_max+1
            y = cont_y/y_max

        elif char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
<<<<<<< HEAD
            screen.addstr(0, 0, 'right')
            m.setSpeeds(70,10)
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'left ')
            m.setSpeeds(10,70)
=======
            x = cont_x/x_max
            y = -2*cont_y/y_max+1

>>>>>>> 9aebba640c47c7a0ee6b499072127b142e6798c1
        elif char == curses.KEY_UP:
            x=1
            y=1


        elif char == curses.KEY_DOWN:
            x=-1
            y=-1


        elif char == ord('d'):
            cont_x=set_cont(cont_x, x_max,+1)
            cont_y=set_cont(cont_y, y_max,+1)


        elif char == ord('a'):
            cont_x=set_cont(cont_x, x_max,+1)
            cont_y=set_cont(cont_y, y_max,+1)


        elif char == ord('s'):
            cont_v=set_cont(cont_x, x_max,-1)


        elif char == ord('w'):
            cont_v=set_cont(cont_v, v_max,1)


        elif char == ord('e') and z=False:
            screen.addstr(0, 0, 'linear mode activated')
            z = True

        elif char == ord('e') and z=True:
            screen.addstr(0, 0, 'linear mode disabled')
            z = False

        v=cont_v/v_max*v_standart

        else:
            print(char)

        if z==True:
            error=v-v_now
            v_now=v_now+error*P

        else:
            v_now=v

        if v==0:
            m.stop()

        else:
            m.setSpeeds(x*v_now,y*v_now)

finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
