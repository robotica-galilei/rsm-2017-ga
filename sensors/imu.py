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
            self.ser.flushInput()
            while self.ser.read() != '#':
                pass
            value = self.ser.readline()[4:][:-2].split(',');
            value = [int(float(i)) for i in value]
            self.yaw = value[0]
            self.pitch = value[1]
            self.yawsum = value[3]
            self.roll = value[2]
            return self
