import sys
import os
import time
import utils.GPIO as GPIO
import subprocess
import signal

if __name__ == '__main__':
    pin = "gpio65"
    #os.system("sh /root/rsm-2017-ga/start.sh")
    #os.system("sh /root/rsm-2017-ga/start_routine.sh")

    GPIO.setup(pin, GPIO.IN)

    pro = subprocess.Popen("python /root/rsm-2017-ga/main.py", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    while True:
        if GPIO.input(pin) == True:
            print("OMFG, you pressed da button!")
            os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
            time.sleep(2)
            pro = subprocess.Popen("python /root/rsm-2017-ga/main.py", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        time.sleep(0.05)
