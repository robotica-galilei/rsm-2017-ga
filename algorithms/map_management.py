import numpy as np

def getAbsoluteDirection(robotDirection, robotSensor):
    '''
    Function that gets the absolute direction of the sensor given the absolute
    direction of the robot and the direction of the sensor relative to the robot

    Absolute directions:
         3
    0  item   2
         1
    '''
    return (robotDirection-robotSensor+4)%4

def uodatePosition(position, index):
    '''
    Function that updates the position (adding 2 to the value in the index) given
    the actual position and the index
    @param position (tuple)
        The actual position (X,Y)
    @param index
        The index to edit (index = 0, index = 1)

    Returns the position edited as tuple
    '''
    #TODO

    return position;

def appendTwoLinesToMatrix(mat, axis, position):
    '''
    Function that appends two lines to a matrix given the matrix, the axis and the
    position.
    @param axis (boolean)
        If the lines are rows or colums. 0 for row, 1 for colums.
    @param position (boolean)
        0 is before index 0, 1 is after index n-1 give n as the length of the matrix

    Returns the new matrix after the edit.
    '''
    #TODO

    return 0;
