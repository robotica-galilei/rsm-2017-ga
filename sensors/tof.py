import sys
sys.path.append("../")
import time
import math
import logging

import modules.tof_60 as tof_60
import modules.tof_200 as tof_200
import config.dimensions as dim
import config.params as params

class Tof:
    def __init__(self, pins = params.tof_pins, addresses = params.tof_addresses):
        #Init routine
        # tof_pins = {'60_NO' : 'gpio68', '60_NE' : 'gpio66', '60_SO' : 'gpio45', '60_SE' : 'gpio47', '60_EN' : 'gpio67', '60_ES' : 'gpio26', '60_ON' : 'gpio69', '60_OS' : 'gpio44', '200_N': 'gpio112', '200_S': 'gpio49', '200_E': 'gpio3', '200_O': 'gpio2'}
        # tof_addresses = {'60_NO' : 0x20, '60_NE' : 0x21 ,'60_SO' : 0x22, '60_SE' : 0x23, '60_EN' : 0x24, '60_ES' : 0x25, '60_ON' : 0x26, '60_OS' : 0x27, '200_N': 0x30, '200_S': 0x31, '200_E': 0x32, '200_O': 0x33}
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

    def activate_all(self):
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

    def read_raw(self, string):
        #Read just the single sensor
        try:
            return self.sens[string].get_distance()
        except Exception:
            return self.sens[string].get_distance()

    def read_raw_all(self):
        #Return a dictionary with all the sensors
        all_s = {}
        for key, item in self.sens.items():
            all_s[key] = self.read_raw(key)
        return all_s

    def read_fix(self,dir):
        #Return the distance in a certain direction cleaned
        alfa_dict = {'N': ('NE','N','NO'), 'E': ('ES','E','EN'), 'S':('SO','S','SE'), 'O':('ON','O','OS')}
        s1 = None; s2 =None; s3 = None
        t1 = 0; t2 = 0; t3 = 0;
        sum1 = 0; sum2 = 0; sum3 = 0
        s_t1 = 0; s_t2 = 0; s_t3 = 0;
        for i in range(3):
            for key in alfa_dict[dir]:
                if len(key) == 2:
                    if s1 == None:
                        s1 = self.read_raw(key)
                        t1 =self.trust(value=s1)
                        sum1+=s1*t1
                        s_t1+=t1
                        ps1 = params.tof_calibration[key]
                    else:
                        s3 = self.read_raw(key)
                        t3 =self.trust(value=s3)
                        sum3+=s3*t3
                        s_t3+=t3
                        ps3 = params.tof_calibration[key]
                else:
                    s2 = self.read_raw(key)
                    t2 =self.trust(value=s2)
                    sum2+=s2*t2
                    s_t2+=t2
                    ps2 = params.tof_calibration[key]
            print(s1, s2, s3)



        s1=sum1
        s2=sum2
        s3=sum3
        t1=s_t1
        t2=s_t2
        t3=s_t3
        print(s1,s2,s3)
        print(t1,t2,t3)
        if t1 != 0:
            s1=(s1/t1)-ps1
        else:
            s1=-1
        if t2 != 0:
            s2=(s2/t2)-ps2
        else:
            s2=-1
        if t3 != 0:
            s3=(s3/t3)-ps3
        else:
            s3=-1

        print(s1, s2, s3)
        #calculate average and the cos and sin of angle
        s_sum = s1 + s2 + s3
        s_div = self.trust(value=s1) + self.trust(value=s2) + self.trust(value=s3)

        if s_div != 0:
            avg = s_sum/s_div

        else:
            avg = -1

        d = self.diff(s1, s2, s3)
        if d != None:
            cosalfa = 1./(math.sqrt(1+math.pow(float(d)/float(dim.tof_60_distance),2)))
            senalfa = (d/dim.tof_60_distance)/(math.sqrt(1+math.pow(float(d)/float(dim.tof_60_distance),2)))
        else:
            cosalfa = None
            senalfa = None


        return avg, cosalfa, senalfa, s_div

    def is_there_a_wall(self, dir):
        d = self.read_fix(dir)[0]
        if  d < params.is_there_a_wall_threshold and d != -1:
            d = self.read_fix(dir)[0]
            if  d < params.is_there_a_wall_threshold and d != -1:
                return True
            else:
                return False
        else:
            return False

    def best_side(self, side1, side2):
        #choose the best side

        avg1, cosalfa1, senalfa1, s_div1 = self.read_fix(side1)
        avg2, cosalfa2, senalfa2, s_div2 = self.read_fix(side2)

        if avg1 == -1 :
            return side2, avg2, cosalfa2, senalfa2, s_div2, 1
        elif avg2 == -1:
            return side1, avg1, cosalfa1, senalfa1, s_div1, -1
        elif s_div2 > s_div1:
            return side2, avg2, cosalfa2, senalfa2, s_div2, 1
        elif s_div1 > s_div2:
            return side1, avg1, cosalfa1, senalfa1, s_div1, -1
        elif avg1 < avg2:
            return side1, avg1, cosalfa1, senalfa1, s_div1, -1
        else:
            return side2, avg2, cosalfa2, senalfa2, s_div2, 1

    def n_cells(self, avg, cosalfa, k = None):

        #return int(math.floor(avg/dim.cell_dimension))  #approssimazione

        if k==None:
            #to test if  it works
            k=dim.cell_dimension

        return int(math.floor((avg - (k - dim.robot_width)/2.)) / k) #con il robot piazzato al centro della cella

    def n_cells_pid(self, avg, cosalfa, k = None):

        #return int(math.floor(avg/dim.cell_dimension))  #approssimazione

        if k==None:
            #to test if  it works
            k=dim.cell_dimension

        return int(avg(math.floor((avg - (k - dim.robot_width)/2.)) / k)) #con il robot piazzato al centro della cella





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
            side, avg, cosalfa, senalfa, z = self.best_side('E','O')

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
                return float(2*(t1*(s1-s2*t2)-t3*(s3+s2*t2)))/(t1+t2)
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
