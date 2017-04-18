import os

HIGH = 1
LOW = 0
OUT = "out"
IN = "in"
exported = set()

class GPIOError(Exception):
     def __init__(self, message, errors):
         super(GPIOError, self).__init__(message)
         self.errors = errors

def write_file(path, value):
    file = open("/sys/class/gpio/" + path, "w")
    file.write(value)
    file.close()


def setup(gpio, direction):
    if gpio not in exported:
        try:
            sys.stdout = open(os.devnull, "w")
            os.system("echo " + gpio[4:] + " > /sys/class/gpio/export")
            sys.stdout = sys.__stdout__
        except:
            pass
        exported.add(gpio)
    write_file(gpio + "/direction", direction)


def output(gpio, value):
    if gpio not in exported:
        raise GPIOError('GPIO setup required','Cannot use gpio before init')
    write_file(gpio + "/value", str(value))
