import sys
sys.path.append("../")
import logging
import time

import config.params as params
import modules.GY906 as GY906

class Heat:
    def __init__(self, addresses = params.heat_addresses, port = params.video_victims_port, baudrate = 115200):
        '''
        Init routine
        addresses is a dictionary containing the addresses of the sensor.
        addresses = {'N': 0x12, 'S': 0x13, 'E': 0x11, 'O': 0x10}
        '''
        self.sens = {}
        for key, item in addresses.items():
            self.sens[key] = GY906.MLX90614(item, bus_num=1)
        self.last_read = time.time()

        self.ser = serial.Serial(port = port, baudrate=baudrate)
        self.ser.close()
        self.ser.open()
        self.starting_deg = 0

    def read_raw(self, dir):
        #Read just the single sensor
        val = self.sens[dir].get_obj_temp()
        print("Heat: ", val)
        if val < 10 or val > 80:
            val = 10
        return val

    def isThereSomeVideoVictim(self):
        '''
        Returns if something has been seen by the sensors
        '''
        if self.ser.isOpen():
            self.ser.flushInput()
            time_start = time.time()
            while self.ser.read() != '#' and time.time() - time_start < 1:
                pass
            if time.time() - time_start >= 1:
                return False, []
            value = self.ser.readline()[4:][:-2].split(',');
            value = [int(float(i)) for i in value]
            return self


    def isThereSomeVictim(self, temp=params.HEAT_THRESHOLD):
        '''
        Returns if something has been seen by the sensors
        '''
        victims = []
        for i in params.directions:
            now = self.read_raw(i)
            if( now >= temp):
                print("Heat: ", now)
                victims.append(i)
        return len(victims) >= 1, victims
