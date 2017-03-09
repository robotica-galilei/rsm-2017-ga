class Tof:
    def __init__(self, s_res_pins, s_addresses):
        #TODO pin configurations
        assert len(s_res_pins) == len(s_addresses) #Check that the 2 lists have the same length
        self.res_pins = s_res_pins
        self.addresses = s_addresses
        addresses_config()

    def addresses_config(self):
        #TODO reset pins
        #TODO configure each sensor
        return 0

    def get(self, n):
        #TODO get distance measurement
        assert n < len(self.res_pins)
        return 0
