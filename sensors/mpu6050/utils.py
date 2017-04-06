import MPU6050_multithreading as gyrolib
import time

def rotate(deg, m):
    tolleranza = 2
    angolofinale = int(gyrolib.yaw + deg)
    if deg > 0:
        if angolofinale > 179:
            angolofinale -= 360
        m.setSpeeds(-20, 20)
        while (angolofinale - 2 != int(gyrolib.yaw) and angolofinale - 1 != int(gyrolib.yaw)):
            print(angolofinale)
            print(int(gyrolib.yaw))
            print("")
            time.sleep(0.001)
        m.stop()
    else:
        if angolofinale < -180:
            angolofinale += 360
        m.setSpeeds(20, -20)
        while (angolofinale + 2 != int(gyrolib.yaw) and angolofinale + 1 != int(gyrolib.yaw)):
            print(angolofinale)
            print(int(gyrolib.yaw))
            print("")
            time.sleep(0.001)
        m.stop()


def posizionati(deg, m, gyro):
    gradi = deg - gyrolib.yaw
    if (gradi > 180):
        gradi = gradi - 360
    elif (gradi < -180):
        gradi = gradi + 360
    if (gradi != 0):
        rotate(gradi, m)
