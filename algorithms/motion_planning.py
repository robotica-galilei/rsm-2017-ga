import numpy as np
try:
    import Queue
except:
    import queue

def queueCheck(mat, node, new, wall, dist, path, visited, q, dir_now, dir_then):
    '''
    Just a function to reduce the repetition of code into dijkstra algorithm
    @param mat
        The matrix of the maze
    @param node
        The node the robot is coming from
    @param new
        The node the robot is going to
    @param wall
        The edge that may be a wall (to check in mat)
    @param dist
        The matrix of the distances
    @param path
        The matrix of the paths
    @param visited
        The boolean matrix of visited nodes
    @param q
        The priority queue for dijkstra algorithm
    @param dir_now
        The direction of the robot on the node it is coming from
    @param dir_then
        The direction of the robot after the move

    This function returns all the matrices and the priority queue updated
    '''
    if (not mat.item(wall) and (not visited.item(new) or dist.item(new) > dist.item(node) +1) and mat.item(new)//256 != 1):
        dist.itemset(new, dist.item(node) +1 + abs(((abs(dir_now-dir_then)+1)%4)-1))
        q.put((dist.item(new),new,dir_then))
        visited.itemset(new, True)
        tmp = [(new[0],new[1])]
        tmp.extend(path[node[0]][node[1]])
        path[new[0]][new[1]] = tmp

    return mat, dist, path, visited, q


def dijkstra(direction,start, end ,mat, bridge):
    '''
    This function gets the starting cell, the final cell and the matrix.
    It returns the distance between the starting cell and the final cell.
    '''

    visited = np.zeros((np.shape(mat)[0],np.shape(mat)[1]))
    dist = np.zeros((np.shape(mat)[0],np.shape(mat)[1]))
    dist.fill('Inf')
    path = [[[] for i in range(np.shape(mat)[1])] for j in range(np.shape(mat)[0])]
    for i in range (1, np.shape(mat)[0]-1,2):
        for j in range (1, np.shape(mat)[1]-1,2):
            path[i][j].append((i,j))
    try:
        q = queue.PriorityQueue()
    except:
        q = Queue.PriorityQueue()
    q.put((0,start,direction))
    visited[start[0]][start[1]] = 1
    dist[start[0]][start[1]] = 0
    while(not q.empty()):
        top = q.get()
        val = top[0]
        node = (top[1][0],top[1][1])
        if(mat.item(node)//1024 == 1):
            if node == bridge[0] and visited.item(bridge[1]) == False:
                q.put((val+15, bridge[1], top[2]))
                dist.itemset(bridge[1],val+15)
                visited.itemset(bridge[1], True)
                tmp = [(bridge[1][0],bridge[1][1])]
                tmp.extend(path[node[0]][node[1]])
                path[bridge[1][0]][bridge[1][1]] = tmp
            elif visited.item(bridge[0]) == False:
                q.put((val+15, bridge[0], top[2]))
                dist.itemset(bridge[0],val+15)
                visited.itemset(bridge[0], True)
                tmp = [(bridge[0][0],bridge[0][1])]
                tmp.extend(path[node[0]][node[1]])
                path[bridge[0][0]][bridge[0][1]] = tmp

        if(val <= dist.item(node)):
            if(node[0]>2): #Check left
                new = (node[0]-2,node[1])
                wall = (node[0]-1,node[1])
                mat, dist, path, visited, q = queueCheck(mat, node, new, wall, dist, path, visited, q, top[2], 0)
            if(node[1]>2): #Check up
                new = (node[0],node[1]-2)
                wall = (node[0],node[1]-1)
                mat, dist, path, visited, q = queueCheck(mat, node, new, wall, dist, path, visited, q, top[2], 3)
            if(np.shape(mat)[0]-node[0]>2): #Check right
                new = (node[0]+2,node[1])
                wall = (node[0]+1,node[1])
                mat, dist, path, visited, q = queueCheck(mat, node, new, wall, dist, path, visited, q, top[2], 2)
            if(np.shape(mat)[1]-node[1]>2): #Check down
                new = (node[0],node[1]+2)
                wall = (node[0],node[1]+1)
                mat, dist, path, visited, q = queueCheck(mat, node, new, wall, dist, path, visited, q, top[2], 1)
    return dist[end[0]][end[1]], path[end[0]][end[1]][::-1] #Return the distance and the list of cells


def bestPath(direction,pos, possible, mat, bridge):
    '''
    Function that given the starting position and the list of all the possible
    cells to see, select the nearest thanks to dijkstra algorithm

    The matrix has this shape:

      0 1 2 3 4 5 (first index)
    0 a b c d e f
    1 g h i j k l
    2 m n o p q r

    (second index)

    and is sent as
    np.matrix("a g m; b h n; c i o; d j p; e k q; f l r")
    '''
    best = [-1,(0,0)]

    for i in possible:
        tmp = dijkstra(direction,pos, i, mat, bridge)
        if(tmp[0]<best[0] or best[0]==-1):
            best=tmp

    return best
