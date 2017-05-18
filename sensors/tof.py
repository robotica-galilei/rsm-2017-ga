import sys
sys.path.append("../")
import rospy
from std_msgs.msg import String
import time
import math
import logging

import modules.tof_60 as tof_60
import modules.tof_200 as tof_200
import config.dimensions as dim
import config.params as params

class Tof:
    def __init__(self, pins = params.tof_pins, addresses = params.tof_addresses, from_ros= False):
        #Init routine
        self.from_ros = from_ros
        if self.from_ros:
            self.last_values = {'N': -1, 'S': -1, 'E': -1, 'O': -1, 'NE': -1, 'NO': -1}
            rospy.init_node('listener', anonymous=True)
            rospy.Subscriber("sensors", String, self.callback)
        else:
            self.sens = {}
            self.sens['NO'] = tof_60.VL6180X(pins['60_NO'], addresses['60_NO'])
            self.sens['NE'] = tof_60.VL6180X(pins['60_NE'], addresses['60_NE'])
            self.sens['SO'] = tof_60.VL6180X(pins['60_SO'], addresses['60_SO'])
            self.sens['SE'] = tof_60.VL6180X(pins['60_SE'], addresses['60_SE'])
            self.sens['EN'] = tof_60.VL6180X(pins['60_EN'], addresses['60_EN'])
            self.sens['ES'] = tof_60.VL6180X(pins['60_ES'], addresses['60_ES'])
            self.sens['ON'] = tof_60.VL6180X(pins['60_ON'], addresses['60_ON'])
            self.sens['OS'] = tof_60.VL6180X(pins['60_OS'], addresses['60_OS'])
            self.sens['N'] = tof_200.VL53L0X(pins['200_N'], addresses['200_N'])
            self.sens['S'] = tof_200.VL53L0X(pins['200_S'], addresses['200_S'])
            self.sens['E'] = tof_200.VL53L0X(pins['200_E'], addresses['200_E'])
            self.sens['O'] = tof_200.VL53L0X(pins['200_O'], addresses['200_O'])

    def callback(self, data):
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        direction, val = data.data.split(':')
        self.last_values[direction] = int(val)

    def activate_all(self):
        if not self.from_ros:
            for key, item in self.sens.items():
                print(key)
                i = 0
                while(i<3):
                    try:
                        item.activate()
                        break
                    except:
                        i += 1
                if i < 3:
                    print(i)
                else:
                    print("ERROR")
                time.sleep(0.1)

    def read_raw(self, direction):
        #Read just the single sensor
        if not self.from_ros:
            try:
                return self.sens[direction].get_distance()
            except Exception:
                return self.sens[direction].get_distance()
        else:
            return self.last_values[direction]

    def read_raw_all(self):
        #Return a dictionary with all the sensors
        all_s = {}
        for key, item in self.sens.items():
            all_s[key] = self.read_raw(key)
        return all_s

    def read_fix(self,dir):
        #Return the distance in a certain direction cleaned
        meas = self.read_raw(dir)
        if meas != -1:
            if meas > 0:
                return meas-params.tof_calibration[dir]
            else:
                return 0
        else:
            return -1

    def is_there_a_wall(self, dir):
        d = self.read_fix(dir)
        if  d < params.is_there_a_wall_threshold and d != -1:
            d = self.read_fix(dir)
            if  d < params.is_there_a_wall_threshold and d != -1:
                return True
            else:
                return False
        else:
            return False

    def best_side(self, side1, side2):
        #choose the best side

        avg1 = self.read_fix(side1)
        avg2 = self.read_fix(side2)

        if avg1 == -1 :
            return side2, avg2, 1
        elif avg2 == -1:
            return side1, avg1, -1
        elif side1 == 'N' and side2 =='S' and avg1 < avg2+dim.cell_dimension:
            return side1, avg1, -1
        elif avg1 < avg2:
            return side1, avg1, -1
        else:
            return side2, avg2, 1

    def n_cells(self, avg, k = dim.cell_dimension):

        #return int(math.floor(avg/dim.cell_dimension))  #approssimazione

        if k==None:
            #to test if  it works
            k=dim.cell_dimension
        print("AVG: ", avg)
        print("STUFF: ", avg - (k - dim.robot_width)/2.)
        x = int(math.floor((avg - (k - dim.robot_width)/2.) / k)) +1 #con il robot piazzato al centro della cella
        #if x == 0:
        #    return 1
        return x

    def n_cells_avg(self, avg, k = dim.cell_dimension):

        #return int(math.floor(avg/dim.cell_dimension))  #approssimazione

        if k==None:
            #to test if  it works
            k=dim.cell_dimension

        x = int(math.floor((avg+dim.robot_width/2) / k) +1) #con il robot piazzato al centro della cella
        if x == 0:
            return 1
        return x

    def is_in_cell_center(self, avg, precision = 40, k= dim.cell_dimension):
        #Precision is cm from the center
        shift = k/2 - precision
        t1 = int(math.floor((avg+shift+dim.robot_width/2) / k) +1)
        t2 = int(math.floor((avg-shift+dim.robot_width/2) / k) +1)
        return t1 == t2

    def n_cells_init(self, avg, k = dim.cell_dimension):

        #return int(math.floor(avg/dim.cell_dimension))  #approssimazione

        if k==None:
            #to test if  it works
            k=dim.cell_dimension

        x = int(math.floor((avg - (k - dim.robot_width)/2.) / k + 0.5)) +1 #con il robot piazzato al centro della cella
        if x == 0:
            return 1
        return x



    def n_cells_pid(self, avg, cosalfa, k = None):

        #return int(math.floor(avg/dim.cell_dimension))  #approssimazione

        if k==None:
            #to test if  it works
            k=dim.cell_dimension

        return int(abs(math.floor((avg - (k - dim.robot_width)/2.)) / k)) #con il robot piazzato al centro della cella





    def real_distance(self, dist, cosalfa):
        return dist*cosalfa

    def trust(self, key = None, value = None):
        #Return trust(reliability) of a sensor given the key
        if value == None:
            self.read_raw(key)
        trust = True
        if value == -1:
            trust = False
        return trust

    def get_trusted_directions_all(self):
        #Return a dictionary of the trusted directions {'N': True, 'S': False ... }

        trusted = {'N':True, 'S':True, 'O':True, 'E':True}
        for key, item in self.sens.items():
            if len(key[:1]) == 1:
                if self.read_raw(key) == -1:
                    trusted[key[:1]] = False
        return trusted

    def error(self, avg = None, cosalfa = None, z = None,  a=1):
        if avg==None and cosalfa==None and z==None:
            side, avg, cosalfa, senalfa, s_div, z = self.best_side('E','O')

            N=self.n_cells_pid(avg, cosalfa)
            #return z*(1-(1./(a+1))*(2*avg+dim.robot_width)*(1+a*cosalfa)/(dim.cell_dimension*(1+N))) # relative error [-1, - 1]
            #return z*((dim.cell_dimension*(1+N))-(1./(a+1))*(2*avg+dim.robot_width)*(1+a*cosalfa)) # absolute error
            return z*(1-(2*avg+dim.robot_width)/(dim.cell_dimension*(1+N)))
        else:
            return None

    def diff(self, s1 = None, s2 = None, s3 = None, dir = None):
        if s1 != None and s2 != None and s3 != None:
            t1 = self.trust(value=s1)
            t2 = self.trust(value=s2)
            t3 = self.trust(value=s3)
            if t1 == False and t3 == False:
                return None
            else:
                return float(2*(t1*(s1-s2*t2)-t3*(s3-s2*t2)))/(t1+t3)
        else:
            alfa_dict = {'N': ('NE','N','NO'), 'E': ('ES','E','EN'), 'S':('SO','S','SE'), 'O':('ON','O','OS')}
            s1 = None; s2 = None
            for key in alfa_dict[dir]:
                if len(key) == 2:
                    if s1 == None:
                        s1 = self.read_raw(key)
                    else:
                        s2 = self.read_raw(key)
            return s1-s2
