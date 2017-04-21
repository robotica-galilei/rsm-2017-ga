import modules.GY906 as GY906

class heat:
    def __init__(self, addresses):
        '''
        Init routine
        addresses is a dictionary containing the addresses of the sensor.
        addresses = {'N':0x20; 'S':0x21 ...}
        '''
        self.sens = {}
        for item, key in addresses.items():
            self.sens[key] = GY906.MLX90614(addresses[key])

    def read_raw(self, dir):
        #Read just the single sensor
        return self.sens[dir].get_obj_temp()
