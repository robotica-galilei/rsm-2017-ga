import sys
import os
import time
import utils.GPIO as GPIO

if __name__ == '__main__':
    pin = "gpio65"
    os.system("sh /root/rsm-2017-ga/start.sh")
    os.system("sh /root/rsm-2017-ga/start_routine.sh")

    GPIO.setup(pin, GPIO.IN)

    os.system("pm2 start /root/rsm-2017-ga/main.py")

    while True:
        if GPIO.input(pin) == True:
            print("OMFG, you pressed da button!")
            os.system("pm2 restart main")
            time.sleep(10)
        time.sleep(0.05)
