import sys
sys.path.append("../")

import serial
import time
import config.params as params

yaw = 0
yawsum = 0
pitch = 0
roll = 0

class Imu:
    def __init__(self, port = params.imu_serial_port, baudrate = params.imu_baudrate):
        self.ser = serial.Serial(port = port, baudrate=baudrate)
        self.ser.close()
        self.ser.open()

    def update(self):
        if self.ser.isOpen():
            ser.flushInput()
            while ser.read() != '#':
                pass
            value = ser.readline()[4:][:-2].split(',');
            value = [int(float(i)) for i in value]
            yaw = value[0]
            pitch = value[1]
            roll = value[2]
            yawsum = value[3]
