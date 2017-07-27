import sys
sys.path.append("../")
import logging
import time
import serial
import rospy
from std_msgs.msg import String

import config.params as params

class Ultra:
    def __init__(self, addresses = params.heat_addresses, port = params.video_victims_port, baudrate = 57600, from_ros= False):
        '''
        Init routine
        addresses is a dictionary containing the addresses of the sensor.
        addresses = {'N': 0x12, 'S': 0x13, 'E': 0x11, 'O': 0x10}
        '''
        self.from_ros = from_ros
        if self.from_ros:
            self.last_values = {'NE': 0, 'NO': 0}
            self.last_time = {'NE': 0, 'NO': 0}
            rospy.Subscriber("Ultra", String, self.callback)

        else:
            self.ser = serial.Serial(port = port, baudrate=baudrate, timeout=1)
            self.ser.close()
            self.ser.open()

    def callback(self, data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        dx, sx = data.data.split(':')
        self.last_values['NE'] = int(dx)
        self.last_values['NO'] = int(sx)
        self.last_time['NE'] = time.time()
        self.last_time['NO'] = time.time()

    def read_raw(self, dir):
        #Read just the single sensor
        if not self.from_ros:
            self.ser.flushInput()
            i = 0
            while(self.ser.read() != '\r' and i<100):
                i += 1
                time.sleep(0.01)
            if i<100:
                val=str(self.ser.readline())
            dx, sx = data.data.split(':')
            self.last_values['NE'] = int(dx)
            self.last_values['NO'] = int(sx)
            return self.last_values[dir]
        else:
            return self.last_values[dir]

    def isThereSomeVideoVictim(self):
        '''
        Returns if something has been seen by the sensors
        '''
        if self.activate_video:
            self.ser.flushInput()
            i = 0
            while(self.ser.read() != '\r' and i<100):
                i += 1
                time.sleep(0.01)
            if i<100:
                val=str(self.ser.readline())
                #print (val)
                bit_readings=list(val)
                #print (bit_readings)
                processed_readings=[]
                for i in range(4):
                    processed_readings.append(int(bit_readings[2*i])*2+int(bit_readings[2*i+1]))
                #print(processed_readings)
                self.victims_found=[]
                self.victims_found.append((name_meaning[processed_readings[0]],position_meaning[processed_readings[1]]))
                self.victims_found.append((name_meaning[processed_readings[2]],position_meaning[processed_readings[3]]))
                print(self.victims_found)
                victims_a = []
                stringa = ''
                if self.victims_found[0][0] != None: # and self.victims_found[0][1]!='Center':
                        victims_a.append(self.victims_found[0][0]+'O')
                if self.victims_found[1][0] != None: # and self.victims_found[1][1]!='Center':
                        victims_a.append(self.victims_found[1][0]+'E')

                return len(victims_a)>0, victims_a
            else:
                return [False, []]
        else:
            return [False, []]


    def isThereSomeVictim(self, temp=params.HEAT_THRESHOLD):
        '''
        Returns if something has been seen by the sensors
        '''
        victims = []
        for i in params.heat_directions:
            now = self.read_raw(i)
            if( now >= temp):
                #print(i + "Heat: ", now)
                victims.append(i)
            else:
                #print("No Heat: ", now)
                pass
        return len(victims) >= 1, victims
