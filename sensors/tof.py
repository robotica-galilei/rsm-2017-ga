import sys
sys.path.append("../")
import time

import modules.tof_60 as tof_60
import modules.tof_200 as tof_200
import config.dimensions as dim
import config.params

class Tof:
    def __init__(self, pins = params.tof_pins, addresses = params.tof_addresses):
        #Init routine
        # tof_pins = {'60_NO' : 'gpio68', '60_NE' : 'gpio66', '60_SO' : 'gpio45', '60_SE' : 'gpio47', '60_EN' : 'gpio67', '60_ES' : 'gpio26', '60_ON' : 'gpio69', '60_OS' : 'gpio44', '200_N': 'gpio112', '200_S': 'gpio49', '200_E': 'gpio3', '200_O': 'gpio2'}
        # tof_addresses = {'60_NO' : 0x20, '60_NE' : 0x21 ,'60_SO' : 0x22, '60_SE' : 0x23, '60_EN' : 0x24, '60_ES' : 0x25, '60_ON' : 0x26, '60_OS' : 0x27, '200_N': 0x30, '200_S': 0x31, '200_E': 0x32, '200_O': 0x33}
        self.sens = {}
        self.sens['NO'] = tof_60.VL6180X(pins['60_NO'], addresses['60_NO'])
        self.sens['NE'] = tof_60.VL6180X(pins['60_NE'], addresses['60_NE'])
        self.sens['SO'] = tof_60.VL6180X(pins['60_SO'], addresses['60_SO'])
        self.sens['SE'] = tof_60.VL6180X(pins['60_SE'], addresses['60_SE'])
        self.sens['EN'] = tof_60.VL6180X(pins['60_EN'], addresses['60_EN'])
        self.sens['ES'] = tof_60.VL6180X(pins['60_ES'], addresses['60_ES'])
        self.sens['ON'] = tof_60.VL6180X(pins['60_ON'], addresses['60_ON'])
        self.sens['OS'] = tof_60.VL6180X(pins['60_OS'], addresses['60_OS'])
        self.sens['N'] = tof_200.VL53L0X(pins['200_N'], addresses['200_N'])
        self.sens['S'] = tof_200.VL53L0X(pins['200_S'], addresses['200_S'])
        self.sens['E'] = tof_200.VL53L0X(pins['200_E'], addresses['200_E'])
        self.sens['O'] = tof_200.VL53L0X(pins['200_O'], addresses['200_O'])

        time.sleep(1)

        for key, item in self.sens.items():
            print(key)
            i = 0
            while(i<3):
                try:
                    item.activate()
                    break
                except:
                    i += 1
            print(i)
            time.sleep(0.1)

    def read_raw(self, string):
        #Read just the single sensor
        return self.sens[string].get_distance()

    def read_raw_all(self):
        #Return a dictionary with all the sensors
        all_s = {}
        for key, item in self.sens.items():
            all_s[key] = self.read_raw(key)
        return all_s

    def read_fix(self,dir):
        #Return the distance in a certain direction cleaned
        s1 = None; s2 = None; s3 = None
        for key, item in self.sens.items():
            if key[:1] == dir:
                if s1 == None:
                    s1 = read_raw(key)
                else:
                    s2 = read_raw(key)
            elif key == dir:
                s3 == read_raw(key)
        alfa = atan(dim.tof_60_distance/abs(s1-s2))
        avg = (s1+s2)/2
        return avg, alfa

    def get_trusted(self):
        #TODO Return a dictionary of the trusted directions {'N': True, 'S': False ... }

        threshold = 220

        trusted = {'N':True, 'S':True, 'O':True, 'E':True}
        for key, item in self.sens.items():
            if len(key[:1]) == 1:
                if read_raw(key) >= threshold:
                    trusted[key[:1]] = False
        return trusted
