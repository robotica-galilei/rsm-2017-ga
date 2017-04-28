import Adafruit_BBIO.UART as UART
import serial

yaw = 0
pitch = 0
roll = 0

class Imu:
    def __init__(self, port = params.imu_serial_port):
        self.ser = serial.Serial(port = port, baudrate=115200)
        self.ser.close()
        self.ser.open()

    def update(self):
        print(self.ser.read())
