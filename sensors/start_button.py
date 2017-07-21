import sys
sys.path.append("../")
import logging
import rospy
from std_msgs.msg import String

import config.params as params
import utils.GPIO as GPIO

class StartButton:
    def __init__(self, gpio = params.START_STOP_BUTTON_PIN, from_ros = False):
        '''
        Init routine
        '''
        self.from_ros = from_ros
        if self.from_ros:
            self.activated = False
            rospy.Subscriber("button", String, self.callback)
        else:
            self.gpio = gpio
            GPIO.setup(self.gpio, GPIO.IN)

    def callback(self, data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        if data.data == 'True':
            self.activated = True

    def read_raw(self):
        '''
        Read all the sensor values
        '''
        if not self.from_ros:
            return GPIO.input(self.gpio)
        else:
            return self.activated
