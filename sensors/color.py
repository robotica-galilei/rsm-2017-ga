import sys
sys.path.append("../")
import logging

import config.params as params
import modules.TCS34725 as TCS34725

class Color:
    def __init__(self, address = params.color_address):
        '''
        Init routine
        addresses is a dictionary containing the addresses of the sensor.
        addresses = {'N': 0x12, 'S': 0x13, 'E': 0x11, 'O': 0x10}
        '''
        self.sens = TCS34725.TCS34725()

    def read_raw(self):
        '''
        Read all the sensor values
        '''
        return self.sens.get_raw_data()

    def is_cell_black(self, thresh=params.BLACK_THRESHOLD):
        '''
        Returns if the read is above the threshold
        '''
        return self.read_raw()[3] < thresh
