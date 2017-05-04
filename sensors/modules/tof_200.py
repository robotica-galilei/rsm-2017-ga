import sys
sys.path.append("../../")

import time
import smbus
import utils.GPIO as GPIO

# ===========================================================================
# ST_VL53L0X ToF ranger Class
#
# Originally written by A. Weber
# References Arduino library by Casey Kuhns of SparkFun:
# https://github.com/sparkfun/ToF_Range_Finder-VL6180_Library\
# ===========================================================================

def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)

VL53L0X_REG_IDENTIFICATION_MODEL_ID             = 0x00c0
VL53L0X_REG_IDENTIFICATION_REVISION_ID          = 0x00c2
VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD       = 0x0050
VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD     = 0x0070
VL53L0X_REG_SYSRANGE_START                      = 0x000

VL53L0X_REG_RESULT_INTERRUPT_STATUS             = 0x0013
VL53L0X_REG_RESULT_RANGE_STATUS                 = 0x0014


class VL53L0X:
    i2c = None

    def __init__(self, gpio, address=0x29, debug=False):
        # Depending on if you have an old or a new Raspberry Pi, you
        # may need to change the I2C bus.  Older Pis use SMBus 0,
        # whereas new Pis use SMBus 1.  If you see an error like:
        # 'Error accessing 0x29: Check your I2C address '
        # change the SMBus number in the initializer below!

        # setup i2c bus and SFR address
        self.i2c = smbus.SMBus(2)
        self.address = 0x29
        self.wanted_address = address
        self.gpio = gpio
        self.debug = debug

        # Module identification
        self.idModel = 0x00
        self.idModelRevMajor = 0x00
        self.idModelRevMinor = 0x00
        self.idModuleRevMajor = 0x00
        self.idModuleRevMinor = 0x00
        self.idDate = 0x00
        self.idTime = 0x00

        GPIO.setup(self.gpio, GPIO.OUT)
        self.deactivate() # Must be started turned off


    def deactivate(self):
        GPIO.output(self.gpio, GPIO.LOW)


    def activate(self):
        GPIO.output(self.gpio, GPIO.HIGH)

        # Change address if requested
        if self.wanted_address != 0x29:
            self.change_address(0x29, self.wanted_address)

    def change_address(self, old_address, new_address):
        # NOTICE:  IT APPEARS THAT CHANGING THE ADDRESS IS NOT STORED IN NON-
        # VOLATILE MEMORY POWER CYCLING THE DEVICE REVERTS ADDRESS BACK TO 0X29

        if old_address == new_address:
            return old_address
        if new_address > 127:
            return old_address
        #self.set_register(0x8A, new_address & 0x7F)
        self.i2c.write_byte_data(old_address, 0x8A, new_address & 0x7F)
        self.address = new_address;
        return new_address


    def get_distance(self):

        val1 = self.i2c.write_byte_data(self.address, VL53L0X_REG_SYSRANGE_START, 0x01)

        cnt = 0
        while (cnt < 100): # 1 second waiting time max
                time.sleep(0.010)
                val = self.i2c.read_byte_data(self.address, VL53L0X_REG_RESULT_RANGE_STATUS)
                if (val & 0x01):
                        break
                cnt += 1

        data = self.i2c.read_i2c_block_data(self.address, 0x14, 12)
        distance = makeuint16(data[11], data[10])
        if distance == 20 or distance > 2000:
            distance = -1
        return distance


    def set_range(self, value):
        # Change the range
        # Value can be an integer between 1 and 3 (1, 2, or 3)
        ranges = [0,0xFD, 0x7F, 0x54]
        sen.set_register(0x097,ranges[value-1])


    def get_register(self, register_address, extra=-1):
        a1 = (register_address >> 8) & 0xFF
        a0 = register_address & 0xFF
        if extra == -1:
            self.i2c.write_i2c_block_data(self.address, a1, [a0])
            data = self.i2c.read_byte(self.address)
        elif extra == 12:
            data = self.i2c.read_i2c_block_data(self.address,register_address, extra)
        return data

    def get_register_16bit(self, register_address):
        a1 = (register_address >> 8) & 0xFF
        a0 = register_address & 0xFF
        self.i2c.write_i2c_block_data(self.address, a1, [a0])
        data0 = self.i2c.read_byte(self.address)
        return (data0 << 8) | (data1 & 0xFF)
        data1 = self.i2c.read_byte(self.address)

    def set_register(self, register_address, data):
        a1 = (register_address >> 8) & 0xFF
        a0 = register_address & 0xFF
        self.i2c.write_i2c_block_data(self.address, a1, [a0, (data & 0xFF)])

    def set_register_16bit(self, register_address, data):
        a1 = (register_address >> 8) & 0xFF
        a0 = register_address & 0xFF
        d1 = (data >> 8) & 0xFF
        d0 = data & 0xFF
        self.i2c.write_i2c_block_data(self.address, a1, [a0, d1, d0])
