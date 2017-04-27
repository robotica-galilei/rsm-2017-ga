import modules.GY906 as GY906

class heat:
    def __init__(self, addresses):
        '''
        Init routine
        addresses is a dictionary containing the addresses of the sensor.
        addresses = {'N': 0x12, 'S': 0x13, 'E': 0x11, 'O': 0x10}
        '''
        self.sens = {}
        for key, item in addresses.items():
            self.sens[key] = GY906.MLX90614(item, bus_num=2)

    def read_raw(self, dir):
        #Read just the single sensor
        return self.sens[dir].get_obj_temp()
