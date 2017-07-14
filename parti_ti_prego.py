import sys
import os
import time
import utils.GPIO as GPIO
import subprocess
import signal
import actuators.motors as motors
import config.params as params

if __name__ == '__main__':
    pin = "gpio65"
    #os.system("sh /root/rsm-2017-ga/start.sh")
    #os.system("sh /root/rsm-2017-ga/start_routine.sh")

    GPIO.setup(pin, GPIO.IN)
    m = motors.Motor(params.motors_pins)
    m.stop()
    pro = subprocess.Popen("python /root/rsm-2017-ga/main.py", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)

    while True:
        if GPIO.input(pin) == True:
            started_pressing = time.time()
            while GPIO.input(pin) == True:
                pass
            pressed_time = time.time() - started_pressing
            print("OMFG, you pressed da button!")
            if pressed_time < 3:
                os.killpg(os.getpgid(pro.pid), signal.SIGKILL)
                m.stop()
                #os.system("kill -9 " + os.getpgid(pro.pid))
                time.sleep(2)
                pro = subprocess.Popen("python /root/rsm-2017-ga/main.py", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
            else:
                os.system("killall -9 screen")
                os.system("killall -9 python")
                sys.exit("Long pressed")
        time.sleep(0.05)
