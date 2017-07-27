import sys
import os

HIGH = 1
LOW = 0
OUT = "out"
IN = "in"
exported = []

pins = {'P9_14':'ehrpwm.1\:0','P8_13':'ehrpwm.2\:0','P9_16':'ehrpwm.1\:1','P8_19':'ehrpwm.2\:0'}

def start(pin, power, duty):
    if pin in pins:
        if not(pin in exported):
            write_file(str(pins[pin]) + "/request", 1)
            write_file(str(pins[pin]) + "/run", 1)
            exported.append(pin)
        write_file(str(pins[pin]) + "/period_freq", 1)
        write_file(str(pins[pin]) + "/duty_percent", 1)


def write_file(path, value):
    file = open("/sys/class/pwm/" + path, "w")
    file.write(value)
    file.close()
