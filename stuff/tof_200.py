import smbus
import struct
import time

def bswap(val):
    return struct.unpack('<H', struct.pack('>H', val))[0]
def mread_word_data(adr, reg):
    return bswap(bus.read_word_data(adr, reg))
def mwrite_word_data(adr, reg, data):
    return bus.write_word_data(adr, reg, bswap(data))
def makeuint16(lsb, msb):
    return ((msb & 0xFF) << 8)  | (lsb & 0xFF)
def VL53L0X_decode_vcsel_period(vcsel_period_reg):
# Converts the encoded VCSEL period register value into the real
# period in PLL clocks
    vcsel_period_pclks = (vcsel_period_reg + 1) << 1;
    return vcsel_period_pclks;



VL53L0X_REG_IDENTIFICATION_MODEL_ID             = 0x00c0
VL53L0X_REG_IDENTIFICATION_REVISION_ID          = 0x00c2
VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD       = 0x0050
VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD     = 0x0070
VL53L0X_REG_SYSRANGE_START                      = 0x000

VL53L0X_REG_RESULT_INTERRUPT_STATUS             = 0x0013
VL53L0X_REG_RESULT_RANGE_STATUS                 = 0x0014


address = 0x29

bus = smbus.SMBus(2)

start = time.time()
for i in range(10):
    val1 = bus.write_byte_data(address, VL53L0X_REG_SYSRANGE_START, 0x01)

    cnt = 0
    while (cnt < 100): # 1 second waiting time max
            time.sleep(0.010)
            val = bus.read_byte_data(address, VL53L0X_REG_RESULT_RANGE_STATUS)
            if (val & 0x01):
                    break
            cnt += 1

    data = bus.read_i2c_block_data(address, 0x14, 12)
    print str(makeuint16(data[11], data[10]))

end = time.time()
print(end - start)
