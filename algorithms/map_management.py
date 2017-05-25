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

def updatePosition(position, home,unexplored_queue, index):
    '''
    Function that updates the position (adding 2 to the value in the index) given
    the actual position and the index
    @param position (tuple)
        The actual position (X,Y)
    @param home (tuple)
        The home position (X,Y)
    @param unexplored_queue (list of tuples)
        The list of the cells to view (X,Y)
    @param index
        The index to edit (index = 0, index = 1)

    Returns the actual position, the home position and the unexplored_queue shifted
    '''
    for i in range(0,len(unexplored_queue)):
        unexplored_queue[i]=(unexplored_queue[i][0],unexplored_queue[i][1]+((not index)*2),unexplored_queue[i][2]+(index*2)) #Shift queued cells position
    position = (position[0],position[1]+((not index)*2),position[2]+(index*2)) #Shift robot position
    home = (home[0],home[1]+((not index)*2),home[2]+(index*2)) #Shift home position

    return position, home, unexplored_queue;

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
    if(axis == 0):
        if(position == 0):
            l = [[0 for i in range(len(mat[0][0]))]]
            l.extend([[0 for i in range(len(mat[0][0]))]])
            l.extend(mat[0])
            mat = [l]
        elif(position == 1):
            mat[0].append([0 for i in range(len(mat[0][0]))])
            mat[0].append([0 for i in range(len(mat[0][0]))])
    elif(axis == 1):
        if(position == 0):
            for idx, elem in enumerate(mat[0]):
                l = [0,0]
                l.extend(elem)
                mat[0][idx] = l
        elif(position == 1):
            for idx, elem in enumerate(mat[0]):
                mat[0][idx].append(0)
                mat[0][idx].append(0)


    return mat
