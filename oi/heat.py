def readSensor(n):
    return 42
    
def getVictims():
    readings=[]
    found=False
    for i in range(0,4):
        readings.append(readSensor(i))
    return [1 if 1 in readings else 0,readings]
        
    