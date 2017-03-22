HIGH = 1
LOW = 0
OUT = "out"
IN = "in"
exported = set()


def write_file(path, value):
    file = open("/sys/class/gpio/" + path, "w")
    file.write(value)
    file.close()


def setup(gpio, direction):
    if gpio not in exported:
        exported.add(gpio)
    write_file(gpio + "/direction", direction)


def output(gpio, value):
    if gpio not in exported:
        raise GPIOError('GPIO setup required')
    write_file(gpio + "/value", value)
