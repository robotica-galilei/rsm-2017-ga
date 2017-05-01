import sys
sys.path.append("../")
import time
import math

import modules.tof_60 as tof_60
import modules.tof_200 as tof_200
import config.dimensions as dim
import config.params as params

def real_distance(dist, cosalfa):
    return dist*cosalfa

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

    def activate_all(self):
        for key, item in self.sens.items():
            print(key)
            i = 0
            while(i<3):
                try:
                    item.activate()
                    break
                except:
                    i += 1
            if i < 3:
                print(i)
            else:
                print("ERROR")
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
        alfa_dict = {'N': ('NE','N','NO'), 'E': ('ES','E','EN'), 'S':('SO','S','SE'), 'O':('ON','O','OS')}
        s1 = None; s2 = None; s3 = None
        for key in alfa_dict[dir]:
            if len(key) == 2:
                if s1 == None:
                    s1 = self.read_raw(key)
                    ps1 = params.tof_calibration[key]
                else:
                    s3 = self.read_raw(key)
                    ps3 = params.tof_calibration[key]
            else:
                s2 = self.read_raw(key)
                ps2 = params.tof_calibration[key]

        s1 = (s1-ps1)* self.trust(value=s1)
        s2 = (s2-ps2)* self.trust(value=s2)
        s3 = (s2-ps2)* self.trust(value=s3)

        s_sum = s1 + s2 + s3
        s_div = self.trust(value=s1) + self.trust(value=s2) + self.trust(value=s3)

        if s_div != 0:
            avg = s_sum/s_div
        else:
            avg = -1

        d = self.diff(s1, s2, s3)

        cosalfa = 1./math.sqrt(1+(d/dim.tof_60_distance)**2)
        senalfa = (d/dim.tof_60_distance)/math.sqrt(1+(d/dim.tof_60_distance)**2)
        return avg, cosalfa, senalfa

    def best_side(self, side1, side2):
        avg1, cosalfa1, senalfa1 = self.read_fix(side1)
        avg2, cosalfa2, senalfa2 = self.read_fix(side2)

        if avg1 == -1:
            return side2, avg2, cosalfa2, senalfa2, 1
        elif avg2 == -1:
            return side1, avg1, cosalfa1, senalfa1, -1
        elif avg1 < avg2:
            return side1, avg1, cosalfa1, senalfa1, -1
        else:
            return side2, avg2, cosalfa2, senalfa2, 1

    def n_cells(self, avg, cosalfa):
        return int(math.floor(real_distance(avg, cosalfa)/dim.cell_dimension))

    def trust(self, key = None, value = None):
        #Return trust(reliability) of a sensor given the key
        if value == None:
            self.read_raw(key)
        trust = True
        if value == -1:
            trust = False
        return trust

    def get_trusted_directions_all(self):
        #Return a dictionary of the trusted directions {'N': True, 'S': False ... }

        trusted = {'N':True, 'S':True, 'O':True, 'E':True}
        for key, item in self.sens.items():
            if len(key[:1]) == 1:
                if self.read_raw(key) == -1:
                    trusted[key[:1]] = False
        return trusted

    def error(self, a=1):
        side, avg, cosalfa, senalfa, z = self.best_side('E','O')
        print(avg)
        print(cosalfa)
        print(senalfa)
        print(self.n_cells(avg, cosalfa))
        return z*(dim.cell_dimension*(1+self.n_cells(avg, cosalfa))-(1./(a+1))*(2*avg+dim.robot_width)*(1+a*cosalfa))

    def diff(self, s1, s2, s3):
        t1 = self.trust(value=s1)
        t2 = self.trust(value=s2)
        t3 = self.trust(value=s3)
        if t1 == False and t3 == False:
            return -1
        else:
            return float(2*(t1*(s1-s2)+t3*(s2-s3)))/float(t1+t3)
