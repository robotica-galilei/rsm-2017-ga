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

def P(k=params.PID_p):
    return error_now*k

def I(k=params.PID_i):
    error_sum = error_now
    num = 0
    for i in error_prec:
        if(i != None):
            error_sum += i
            num += 1

    return error_sum*k

def D(k=params.PID_d):
    avg = 0.
    num = 0
    for i in error_prec:
        if(i != None):
            avg += i
            num += 1
    avg /= num
    return (error_now-avg)*k

def get_pid(error = None):
    if error != None:
        update_error(error)
    return P()+I()+D()
