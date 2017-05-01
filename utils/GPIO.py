import sys
import os

HIGH = 1
LOW = 0
OUT = "out"
IN = "in"
exported = []

class GPIOError(Exception):
     def __init__(self, message, errors):
         super(GPIOError, self).__init__(message)
         self.errors = errors


def write_file(path, value):
    file = open("/sys/class/gpio/" + path, "w")
    file.write(value)
    file.close()


def read_file(path):
    file = open("/sys/class/gpio/" + path, "r")
    value = bool(int(file.read()[:1]))
    file.close()
    return value


def setup(gpio, direction):
    if gpio not in exported:
        try:
            sys.stdout = open(os.devnull, "w")
            os.system("echo " + gpio[4:] + " > /sys/class/gpio/export")
            sys.stdout = sys.__stdout__
        except Exception as e:
            print(e)
        exported.append(gpio)
    write_file(gpio + "/direction", direction)


def output(gpio, value):
    if gpio not in exported:
        raise GPIOError('GPIO setup required','Cannot use gpio before init')
    write_file(gpio + "/value", str(value))


def input(gpio):
    if gpio not in exported:
        raise GPIOError('GPIO setup required','Cannot use gpio before init')
    return read_file(gpio + "/value")
