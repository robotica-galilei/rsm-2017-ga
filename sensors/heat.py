import sys
sys.path.append("../")
import logging

import config.params as params
import modules.GY906 as GY906

class Heat:
    def __init__(self, addresses = params.heat_addresses):
        '''
        Init routine
        addresses is a dictionary containing the addresses of the sensor.
        addresses = {'N': 0x12, 'S': 0x13, 'E': 0x11, 'O': 0x10}
        '''
        self.sens = {}
        for key, item in addresses.items():
            self.sens[key] = GY906.MLX90614(item, bus_num=1)

    def read_raw(self, dir):
        #Read just the single sensor
        return self.sens[dir].get_obj_temp()

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
