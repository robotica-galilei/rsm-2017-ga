'''
Configuration file for thresholds and parameters
'''
directions = ['N', 'S', 'E', 'O']
heat_directions = ['N', 'E', 'O']

'''
Pins and ports
'''

kit_servo_pin = "P9_22"
START_STOP_BUTTON_PIN_ADA = "P8_16"
START_STOP_BUTTON_PIN = "gpio46"
imu_serial_port = "/dev/ttyO1"
video_victims_port = "/dev/ttyO5"
imu_baudrate = 115200
color_address = 0x29

#tof_pins = {'60_NO' : 'gpio68', '60_NE' : 'gpio66', '60_SO' : 'gpio45', '60_SE' : 'gpio47', '60_EN' : 'gpio67', '60_ES' : 'gpio26', '60_ON' : 'gpio69', '60_OS' : 'gpio44', '200_N': 'gpio112', '200_S': 'gpio27', '200_E': 'gpio49', '200_O': 'gpio20'}
tof_pins = {'60_NO' : 'gpio68', '60_NE' : 'gpio66', '200_N': 'gpio32', '200_S': 'gpio86', '200_E': 'gpio87', '200_O': 'gpio89'}
tof_addresses = {'60_NO' : 0x20, '60_NE' : 0x21 ,'60_SO' : 0x22, '60_SE' : 0x23, '60_EN' : 0x24, '60_ES' : 0x25, '60_ON' : 0x26, '60_OS' : 0x27, '200_N': 0x30, '200_S': 0x31, '200_E': 0x32, '200_O': 0x33}

touch_pins = {'E': 'gpio115', 'O':'gpio7'}

heat_addresses = {'N': 0x12, 'E': 0x11, 'O': 0x10}

#motors_pins = {'fl':'P8_13','fr':'P8_19','rl':'P9_14','rr':'P9_16','dir_fl':'gpio31','dir_fr':'gpio48','dir_rl':'gpio60','dir_rr':'gpio30'}
motors_pins = {'fl':'P9_14','fr':'P8_13','rl':'P9_16','rr':'P8_19','dir_fl':'gpio113','dir_fr':'gpio72','dir_rl':'gpio111','dir_rr':'gpio70'}

'''
ToF calibration
'''
tof_calibration = {'NO' : 25, 'NE' : 25, 'SO' : 25, 'SE' : 25, 'EN' : 25, 'ES' : 25, 'ON' : 25, 'OS' : 25, 'N': 40, 'S': 40, 'E': 40, 'O': 40}
is_there_a_wall_threshold = 200

'''
Heat calibration
'''
HEAT_THRESHOLD = 28

'''
Color calibration
'''
BLACK_THRESHOLD = 350

'''
Led parameters
'''

LED_PIN = 'gpio61'
LED_BLINK_DELAY = 0.5

'''
traction costants
'''

#to test: I use random numbers

yaw_N = 5
Pyaw = 0.4
Iyaw = 0.05
Dyaw = -0.03

pinch_N = 10
Ppinch = 0.4
Ipinch = 0.05
Dpinch = -0.03


'''
ramp
'''
vel_rampgiu = 25
vel_rampsu = 100
ramp_angle = 20



'''
ERROR_COSTANTS
'''

ERROR_OBSTACLE= 50

'''
MOTORS_PARAMS
'''

MOTOR_CELL_TIME     =       1.3
MOTOR_MIN_CELL_TIME     =       0.4
MOTOR_ROTATION_TIME =       1.5
MOTOR_DEFAULT_POWER_LINEAR      =       50
MOTOR_PRECISION_POWER_LINEAR      =       25
MOTOR_DEFAULT_POWER_ROTATION    =       70
