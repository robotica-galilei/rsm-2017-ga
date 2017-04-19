import tof_60
import tof_200

class tof:
    def __init__(self, pins, addresses):
        #Init routine
        self.sens = {}
        self.sens['NO'] = tof_60.VL6180X(pins['60_NO'], addresses['60_NO'])
        self.sens['NE'] = tof_60.VL6180X(pins['60_NE'], addresses['60_NE'])
        self.sens['SO'] = tof_60.VL6180X(pins['60_SO'], addresses['60_SO'])
        self.sens['SE'] = tof_60.VL6180X(pins['60_SE'], addresses['60_SE'])
        self.sens['EN'] = tof_60.VL6180X(pins['60_EN'], addresses['60_EN'])
        self.sens['ES'] = tof_60.VL6180X(pins['60_ES'], addresses['60_ES'])
        self.sens['ON'] = tof_60.VL6180X(pins['60_ON'], addresses['60_ON'])
        self.sens['OS'] = tof_60.VL6180X(pins['60_OS'], addresses['60_OS'])
        self.sens['N'] = tof_60.VL6180X(pins['200_N'], addresses['200_N'])
        self.sens['S'] = tof_60.VL6180X(pins['200_S'], addresses['200_S'])
        self.sens['E'] = tof_60.VL6180X(pins['200_E'], addresses['200_E'])
        self.sens['O'] = tof_60.VL6180X(pins['200_O'], addresses['200_O'])

        for key, item in self.sens.items():
            item.activate()

    def read_raw(self, string):
        #Read just the single sensor
        return self.sens[string].get_distance()

    def read_raw_all(self):
        #Return a dictionary with all the sensors
        all_s = {}
        for key, item in self.sens.items():
            all_s[key] = self.read_raw[key]
        return all_s

    def read_fix(self,dir):
        #TODO Return the distance in a certain direction cleaned
        pass

    def get_trusted(self):
        #TODO Return a dictionary of the trusted directions {'N': True, 'S': False ... }
        pass
