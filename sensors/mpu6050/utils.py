import MPU6050_multithreading as gyrolib

def rotate(deg, m):
    tolleranza = 2
    gyro.refresh()
    angolofinale = gyrolib.yaw + deg
    if deg > 0:
        if angolofinale > 179:
            angolofinale -= 360
        m.setSpeeds(40, -40)
        while (int(abs(angolofinale - 2)) != gyrolib.yaw and int(abs(angolofinale - 1)) != gyrolib.yaw):
            print(angolofinale)
            print(gyro.yaw)
        m.stop()
    else:
        if angolofinale < -180:
            angolofinale += 360
        m.setSpeeds(-40, 40)
        while (int(abs(angolofinale + 2)) != gyrlibo.yaw and int(abs(angolofinale + 1)) != gyrolib.yaw):
            print(angolofinale)
            print(gyro.yaw)
        m.stop()


def posizionati(deg, m, gyro):
    gradi = deg - gyrolib.yaw
    if (gradi > 180):
        gradi = gradi - 360
    elif (gradi < -180):
        gradi = gradi + 360
    if (gradi != 0):
        rotate(gradi, m)
