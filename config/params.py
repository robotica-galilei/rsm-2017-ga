'''
Configuration file for thresholds and parameters
'''
directions = ['N', 'S', 'E', 'O']
victim = 25

'''
Pins and ports
'''

kit_servo_pin = "P9_22"
imu_serial_port = "/dev/ttyO1"
imu_baudrate = 115200

tof_pins = {'60_NO' : 'gpio68', '60_NE' : 'gpio66', '60_SO' : 'gpio45', '60_SE' : 'gpio47', '60_EN' : 'gpio67', '60_ES' : 'gpio26', '60_ON' : 'gpio69', '60_OS' : 'gpio44', '200_N': 'gpio112', '200_S': 'gpio49', '200_E': 'gpio27', '200_O': 'gpio20'}
tof_addresses = {'60_NO' : 0x20, '60_NE' : 0x21 ,'60_SO' : 0x22, '60_SE' : 0x23, '60_EN' : 0x24, '60_ES' : 0x25, '60_ON' : 0x26, '60_OS' : 0x27, '200_N': 0x30, '200_S': 0x31, '200_E': 0x32, '200_O': 0x33}

heat_addresses = {'N': 0x12, 'S': 0x13, 'E': 0x11, 'O': 0x10}

motors_pins = {'fl':'P8_13','fr':'P8_19','rl':'P9_14','rr':'P9_16','dir_fl':'gpio31','dir_fr':'gpio48','dir_rl':'gpio60','dir_rr':'gpio30'}

'''
ToF calibration
'''
tof_calibration = {'NO' : 25, 'NE' : 25, 'SO' : 25, 'SE' : 25, 'EN' : 25, 'ES' : 25, 'ON' : 25, 'OS' : 25, 'N': 30, 'S': 30, 'E': 30, 'O': 30}
is_there_a_wall_threshold = 200

'''
PID costants
'''

PID_p = 1
PID_i = 0
PID_d = 0
