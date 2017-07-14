import sys
sys.path.append("../")
import logging
import time
import serial
import rospy
from std_msgs.msg import String

import config.params as params
import modules.GY906 as GY906



name_meaning=[None,'U','S','H']
position_meaning=[None,'Incoming','Center','Passed']

class Heat:
    def __init__(self, addresses = params.heat_addresses, port = params.video_victims_port, baudrate = 115200, from_ros= False):
        '''
        Init routine
        addresses is a dictionary containing the addresses of the sensor.
        addresses = {'N': 0x12, 'S': 0x13, 'E': 0x11, 'O': 0x10}
        '''
        self.from_ros = from_ros
        if self.from_ros:
            self.last_values = {'N': 0, 'E': 0, 'O': 0}
            self.last_victim = 0
            self.last_saved = 0
            self.victims = [False,[]]
            #rospy.init_node('heat_listener', anonymous=True)
            rospy.Subscriber("heat", String, self.callback)
            self.ser = serial.Serial(port = port, baudrate=baudrate, timeout=1)
            self.ser.close()
            self.ser.open()
            if len(self.ser.readline()) < 1:
                self.activate_video = False
            else:
                self.activate_video = True
        else:
            self.sens = {}
            for key, item in addresses.items():
                self.sens[key] = GY906.MLX90614(item, bus_num=1)
            self.last_read = time.time()
        self.starting_deg = 0

    def callback(self, data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        direction, val = data.data.split(':')
        self.last_values[direction] = float(val)
        victims = self.isThereSomeVictim()
        if victims[0]:
            self.last_victim = time.time()
            self.victims = victims

    def read_raw(self, dir):
        #Read just the single sensor
        if not self.from_ros:
            val = self.sens[dir].get_obj_temp()
            if val < 10 or val > 80:
                val = 10
            return val
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
