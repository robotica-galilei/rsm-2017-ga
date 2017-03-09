class Motor:
    def __init__(self):
        #TODO pin configurations
        self.actual_l = 0
        self.actual_r = 0

    def setSpeedLeft(self, power):
        #TODO set speed
        self.actual_l = power

    def setSpeedRight(self, power):
        #TODO set speed
        self.actual_r = power

    def stopLeft(self):
        self.setSpeedLeft(0)

    def stopRight(self):
        self.setSpeedRight(0)

    def setSpeeds(self, left, right, l_power, r_power):
        self.setSpeedLeft(l_power)
        self.setSpeedRight(r_power)

    def stop(self):
        self.stopLeft()
        self.stopRight()
