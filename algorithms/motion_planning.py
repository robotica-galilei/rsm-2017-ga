import numpy as np
import queue

def dijkstra(start, end ,mat):
    '''
    This function gets the starting cell, the final cell and the matrix.
    It returns the distance between the starting cell and the final cell.
    '''

    visited = np.zeros((np.shape(mat)[0],np.shape(mat)[1]))
    dist = np.zeros((np.shape(mat)[0],np.shape(mat)[1]))

    path = [[[] for i in range(np.shape(mat)[0])] for j in range(np.shape(mat)[1])]
    for i in range (1, np.shape(mat)[0]-1,2):
        for j in range (1, np.shape(mat)[1]-1,2):
            path[i][j].append((i,j))

    q = queue.PriorityQueue()
    q.put((0,start))
    visited[start[0]][start[1]] = 1
    dist[start[0]][start[1]] = 0

    while(not q.empty()):
        top = q.get()
        val = top[0]
        node = (top[1][0],top[1][1])
        if(val <= dist.item(node)):
            if(node[0]>2):
                new = (node[0]-2,node[1])
                wall = (node[0]-1,node[1])
                if (not mat.item(wall) and (not visited.item(new) or dist.item(new) > dist.item(node) +1)):
                    dist.itemset(new, dist.item(node) +1)
                    q.put((dist.item(new),new))
                    visited.itemset(new, True)
                    tmp = [(new[0],new[1])]
                    tmp.extend(path[node[0]][node[1]])
                    path[new[0]][new[1]] = tmp
            if(node[1]>2):
                new = (node[0],node[1]-2)
                wall = (node[0],node[1]-1)
                if (not mat.item(wall) and (not visited.item(new) or dist.item(new) > dist.item(node) +1)):
                    dist.itemset(new, dist.item(node) +1)
                    q.put((dist.item(new),new))
                    visited.itemset(new, True)
                    tmp = [(new[0],new[1])]
                    tmp.extend(path[node[0]][node[1]])
                    path[new[0]][new[1]] = tmp
            if(np.shape(mat)[0]-node[0]>2):
                new = (node[0]+2,node[1])
                wall = (node[0]+1,node[1])
                if (not mat.item(wall) and (not visited.item(new) or dist.item(new) > dist.item(node) +1)):
                    dist.itemset(new, dist.item(node) +1)
                    q.put((dist.item(new),new))
                    visited.itemset(new, True)
                    tmp = [(new[0],new[1])]
                    tmp.extend(path[node[0]][node[1]])
                    path[new[0]][new[1]] = tmp
            if(np.shape(mat)[1]-node[1]>2):
                new = (node[0],node[1]+2)
                wall = (node[0],node[1]+1)
                if (not mat.item(wall) and (not visited.item(new) or dist.item(new) > dist.item(node) +1)):
                    dist.itemset(new, dist.item(node) +1)
                    q.put((dist.item(new),new))
                    visited.itemset(new, True)
                    tmp = [(new[0],new[1])]
                    tmp.extend(path[node[0]][node[1]])
                    path[new[0]][new[1]] = tmp

    return dist[end[0]][end[1]], path[end[0]][end[1]][::-1] #Return the distance and the list of cells
