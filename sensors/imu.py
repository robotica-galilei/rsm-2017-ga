import sys
sys.path.append("../")

import serial
import time
import config.params as params
import rospy
from std_msgs.msg import String

yaw = 0
yawsum = 0
pitch = 0
roll = 0

class Imu:
    def __init__(self, port = params.imu_serial_port, baudrate = params.imu_baudrate, from_ros=False):
        self.from_ros = from_ros
        if not self.from_ros:
            self.ser = serial.Serial(port = port, baudrate=baudrate, timeout=1)
            self.ser.close()
            self.ser.open()
        else:
            rospy.Subscriber("imu", String, self.callback)
        self.starting_deg = 0
        self.last_calibrated = 0
        self.error_occurred = False
        self.last_values = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0
        self.yawsum = 0

    def callback(self, data):
        self.yaw, self.pitch, self.roll, self.yawsum = data.data.split(':')
        self.yaw = int(self.yaw)
        self.pitch = int(self.pitch)
        self.roll = int(self.roll)
        self.yawsum = int(self.yawsum)
        self.last_time = time.time()

    def get_yawsum(self):
        return int(self.yawsum)

    def get_roll(self):
        return int(self.roll)

    def get_pitch(self):
        return int(self.pitch)

    def get_yaw(self):
        return int(self.yaw)

    def update(self):
        if not self.from_ros:
            if self.ser.isOpen():
                self.ser.flushInput()
                beep = time.time()
                while self.ser.read() != '#':
                    if(time.time()-beep>0.8):
                        self.error_occurred = True
                        return self
                    else:
                        beep = time.time()
                value = self.ser.readline()[4:][:-2].split(',');
                value = [int(float(i)) for i in value]
                self.yaw = value[0]
                self.pitch = value[1]
                self.roll = value[2]
                self.yawsum = value[3]
        return self
