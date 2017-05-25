import sys
sys.path.append("../")

import config.params as params
import traction

class ERROR:

    def __init__(self, x=traction.x):
        self.error_prec = [None for i in range(x)]
        self.error_now = None

    def update_error(self, error):

        if self.error_prec[-1] == None:
            self.error_prec[-1] = error
            self.error_now = error
        else:
            del(self.error_prec[0])
            self.error_prec.append(self.error_now)
            self.error_now = error

    def P(self, k):
        return self.error_now* k

    def I(self, k):
        error_sum = 0

        for i in self.error_prec:
            if(i != None):
                error_sum += i

        if self.error_now != None:
            error_sum+= self.error_now

        return error_sum* k

    def D(self, k):
        avg = 0.
        num = 0
        for i in self.error_prec:
            if(i != None):
                avg += i
                num += 1
        avg /= num
        return (self.error_now-avg)*k

    def get_pid(self, PID_p, PID_i, PID_d, error = None):
        if error != None:
            update_error(error)
        return P(PID_p)+I(PID_i)+D(PID_d)
        else:
        return 0
