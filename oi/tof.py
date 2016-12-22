def readSensor(n):
    return 42

def getSide(n):
    return (readSensor(2*n),readSensor(2*n+1))

def readAll():
    return [getSide(0),getSide(1),getSide(2),getSide(3)]