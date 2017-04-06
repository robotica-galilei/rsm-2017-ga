"""
MPU6050 Python I2C Class - MPU6050 example usage
Copyright (c) 2015 Geir Istad

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from MPU6050 import MPU6050
import threading

roll = 0
pitch = 0
yaw = 0
yawsum = 0

class GYRO(threading.Thread):
    def __init__(self,threadName):
        threading.Thread.__init__(self)
        self.stop_flag = True
        self.threadName = threadName

        self.i2c_bus = 2
        self.device_address = 0x68
        # The offsets are different for each device and should be changed
        # accordingly using a calibration procedure
        self.x_accel_offset = -5489
        self.y_accel_offset = -1441
        self.z_accel_offset = 1305
        self.x_gyro_offset = -2
        self.y_gyro_offset = -72
        self.z_gyro_offset = -5
        self.enable_debug_output = True

        self.mpu = MPU6050(self.i2c_bus, self.device_address, self.x_accel_offset, self.y_accel_offset,
                      self.z_accel_offset, self.x_gyro_offset, self.y_gyro_offset, self.z_gyro_offset,
                      self.enable_debug_output)

        self.mpu.dmp_initialize()
        self.mpu.set_DMP_enabled(True)
        self.mpu_int_status = self.mpu.get_int_status()
        #print(hex(mpu_int_status))

        self.packet_size = self.mpu.DMP_get_FIFO_packet_size()
        #print(packet_size)
        self.FIFO_count = self.mpu.get_FIFO_count()
        #print(FIFO_count)

        self.FIFO_buffer = [0]*64

        self.FIFO_count_list = list()

    def run(self):
        global roll
        global pitch
        global yaw
        while(self.stop_flag):
            self.FIFO_count = self.mpu.get_FIFO_count()
            self.mpu_int_status = self.mpu.get_int_status()

            # If overflow is detected by status or fifo count we want to reset
            if (self.FIFO_count == 1024) or (self.mpu_int_status & 0x10):
                self.mpu.reset_FIFO()
                #print('overflow!')
            # Check if fifo data is ready
            elif (self.mpu_int_status & 0x02):
                # Wait until packet_size number of bytes are ready for reading, default
                # is 42 bytes
                while self.FIFO_count < self.packet_size:
                    self.FIFO_count = self.mpu.get_FIFO_count()
                self.FIFO_buffer = self.mpu.get_FIFO_bytes(self.packet_size)
                self.accel = self.mpu.DMP_get_acceleration_int16(self.FIFO_buffer)
                self.quat = self.mpu.DMP_get_quaternion_int16(self.FIFO_buffer)
                self.grav = self.mpu.DMP_get_gravity(self.quat)

                self.roll_pitch_yaw = self.mpu.DMP_get_euler_roll_pitch_yaw(self.quat, self.grav)
                roll = self.roll_pitch_yaw.x
                pitch = self.roll_pitch_yaw.y
                yaw = self.roll_pitch_yaw.z*2
