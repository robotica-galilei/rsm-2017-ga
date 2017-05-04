import sys
sys.path.append("../")

import config.params as params

error_prec = [None for i in range(4)]
error_now = None

def update_error(error):
    global error_prec
    global error_now

    if error_prec[-1] == None:
        error_prec[-1] = error
        error_now = error
    else:
        del(error_prec[0])
        error_prec.append(error_now)
        error_now = error

def P(k):
    return error_now*k

def I(k):
    error_sum = 0
    num = 0
    for i in error_prec:
        if(i != None):
            error_sum += i
            num += 1

    if error_now != None:
        error_sum+= error_now

    return error_sum*k

def D(k):
    avg = 0.
    num = 0
    for i in error_prec:
        if(i != None):
            avg += i
            num += 1
    avg /= num
    return (error_now-avg)*k

def get_pid(PID_p, PID_i, PID_d, error = None):
    if error != None:
        update_error(error)
    return P(PID_p)+I(PID_i)+D(PID_d)
