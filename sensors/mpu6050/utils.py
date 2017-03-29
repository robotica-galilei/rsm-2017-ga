def rotate(deg, m, gyro):
    tolleranza = 2
    angolofinale = gyro.yaw + deg
    if deg > 0:
        if angolofinale > 179:
            angolofinale -= 360
        m.setSpeeds(40, -40)
        while (abs(angolofinale - 2) != gyro.yaw and abs(angolofinale - 1) != gyro.yaw):
            pass
        m.stop()
    else:
        if angolofinale < -180:
            angolofinale += 360
        m.setSpeeds(-40, 40)
        while (abs(angolofinale + 2) != gyro.yaw and abs(angolofinale + 1) != gyro.yaw):
            pass
        m.stop()


def posizionati(deg, m, gyro):
    gradi = deg - gyro.yaw
    if (gradi > 180):
        gradi = gradi - 360
    elif (gradi < -180):
        gradi = gradi + 360
    if (gradi != 0):
        rotate(gradi, m, gyro)
