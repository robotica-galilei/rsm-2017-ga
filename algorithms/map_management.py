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
        unexplored_queue[i]=(unexplored_queue[i][0]+((not index)*2),unexplored_queue[i][1]+(index*2)) #Shift queued cells position
    position = (position[0]+((not index)*2),position[1]+(index*2)) #Shift robot position
    home = (home[0]+((not index)*2),home[1]+(index*2)) #Shift home position

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
            #mat = np.hstack((np.zeros((np.shape(mat)[0],2)),mat)) #Add 2 rows to the top
            l = [[0 for i in range(len(mat[0]))]]
            l.extend(l)
            l.extend(mat)
            mat = l
        elif(position == 1):
            #mat = np.hstack((mat,np.zeros((np.shape(mat)[0],2)))) #Add 2 rows to the bottom
            l = [0 for i in range(len(mat[0]))]
            mat.append(l)
            mat.append(l)
            mat
    elif(axis == 1):
        if(position == 0):
            #mat = np.vstack((np.zeros((2,np.shape(mat)[1])),mat)) #Add 2 columns to the left
            for idx, elem in enumerate(mat):
                l = [0,0]
                l.extend(elem)
                mat[idx] = l
        elif(position == 1):
            #mat = np.vstack((mat,np.zeros((2,np.shape(mat)[1])))) #Add 2 columns to the right
            for idx, elem in enumerate(mat):
                mat[idx].append(0)
                mat[idx].append(0)


    return mat
