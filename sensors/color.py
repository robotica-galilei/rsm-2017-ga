import sys
sys.path.append("../")
import logging
import rospy
from std_msgs.msg import String

import config.params as params
import modules.TCS34725 as TCS34725

class Color:
    def __init__(self, address = params.color_address, from_ros= False):
        '''
        Init routine
        addresses is a dictionary containing the addresses of the sensor.
        addresses = {'N': 0x12, 'S': 0x13, 'E': 0x11, 'O': 0x10}
        '''
        self.from_ros = from_ros
        if self.from_ros:
            self.last_values = [0,0,0,0]
            #rospy.init_node('color_listener', anonymous=True)
            rospy.Subscriber("color", String, self.callback)
        else:
            self.sens = TCS34725.TCS34725()

    def callback(self, data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        self.last_values[0], self.last_values[1], self.last_values[2], self.last_values[3] = data.data.split(',')
        self.last_values = [int(i) for i in self.last_values]

    def read_raw(self):
        '''
        Read all the sensor values
        '''
        if not self.from_ros:
            return self.sens.get_raw_data()
        else:
            return self.last_values

    def is_cell_black(self, thresh=params.BLACK_THRESHOLD):
        '''
        Returns if the read is above the threshold
        '''
        print("COLOR: ", self.read_raw())
        return self.read_raw()[0] < 30 and self.read_raw()[1] < 30 and self.read_raw()[2] < 30 and self.read_raw()[3] < 100
