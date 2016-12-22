def readCorner(n):
    return 42

def getObstacle():
    readings=[]
    found=False
    for i in range(0,4):
        readings.append(readCorner(i))
    return [1 if 1 in readings else 0,readings]