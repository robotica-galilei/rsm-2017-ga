import sys
sys.path.append("../")

import config.params as params
import motors_pid as pid

#fora experiments

def traction_init():
    x=params.yaw_N
    yaw = motors_pid.ERROR()
    x=params.pinch_N
    pinch = motors_pid.ERROR()

#lavora sulla differenza di trazione tra destra e sinistra per mantenere la condizione di parallelismo
def yaw_correction(yaw_now, yaw_ok):
    #salva l'errore per ottenere un pid
    #errore = differenza tra yaw attuale e yaw voluto
    error = yaw_now - yaw_ok
    correction = yaw.get_pid(params.Pyaw, params.Iyaw, params.Dyaw, error)
    return correction


#lavora sulla differenza di trazione tra davanti e dietro per evitare slittamenti delle ruote o ribaltamenti
def pinch_correction(pinch_now, pinch_ok, vel_now):
    #salva l'errore per ottenere un pid
    #errore = differenza tra roll attuale e roll voluto
    #quando derivata è costante roll voluto = roll attuale
    #quando roll voluto < -valrampa potenza rampagiù
    #quando roll voluto > valrampa potenza rampasu

    d=pinch.D(1)
    p=pinch.P(1)
    if d==0:
        pinch_ok=pinch_now
        if p > params.ramp_angle:
            vel=parmams.vel_rampsu

        if p < -params.ramp_angle:
            vel=params.vel_rampgiu

        else:
            vel=vel_now

    error = pinch_now - pinch_ok
    correction = pinch.get_pid(params.Ppinch, params.Ipinch, params.Dpinch, error)

    return pinch_ok, correction, vel;
