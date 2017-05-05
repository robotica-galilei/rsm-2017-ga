import curses
import actuators.motors as motors

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
v = 20
try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            m.stop()
        elif char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
            screen.addstr(0, 0, 'right')
            m.setSpeeds(70,10)
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'left ')
            m.setSpeeds(-10,70)
        elif char == curses.KEY_UP:
            screen.addstr(0, 0, 'up   ')
            m.setSpeeds(v,v)
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 0, 'down ')
            m.setSpeeds(-v,-v)
        elif char == ord('1'):
            screen.addstr(0, 0, 'down ')
            v = 20
        elif char == ord('2'):
            screen.addstr(0, 0, 'down ')
            v = 40
        elif char == ord('3'):
            screen.addstr(0, 0, 'down ')
            v = 60
        elif char == ord('4'):
            screen.addstr(0, 0, 'down ')
            v = 80
        elif char == ord('5'):
            screen.addstr(0, 0, 'down ')
            v = 100
        else:
            print(char)
finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
