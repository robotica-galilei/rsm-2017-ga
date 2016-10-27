import numpy as np
import queue

def dijkstra(start, end ,mat):
    '''
    This function gets the starting cell, the final cell and the matrix.
    It returns the distance between the starting cell and the final cell.
    '''

    visited = np.zeros((len(mat),len(mat[0])))
    dist = np.zeros((len(mat),len(mat[0])))
    q = queue.PriorityQueue()
    q.put((0,start))
    visited[start[0]][start[1]] = 1
    dist[start[0]][start[1]] = 0
    while(not q.empty()):
        top = q.get()
        val = top[0]
        node = top[1]
        if(val <= dist[node[0]][node[1]]):
            if(node[0]>2):
                new = [node[0]-2,node[1]]
                wall = [node[0]-1,node[1]]
                if (not mat[wall[0]][wall[1]] and (not visited[new[0]][new[1]] or dist[new[0]][new[1]] > dist[node[0]][node[1]] +1)):
                    dist[new[0]][new[1]] = dist[node[0]][node[1]] +1
                    q.put((dist[new[0]][new[1]],(new[0],new[1])))
                    visited[new[0]][new[1]] = True
            if(node[1]>2):
                new = [node[0],node[1]-2]
                wall = [node[0],node[1]-1]
                if (not mat[wall[0]][wall[1]] and (not visited[new[0]][new[1]] or dist[new[0]][new[1]] > dist[node[0]][node[1]] +1)):
                    dist[new[0]][new[1]] = dist[node[0]][node[1]] +1
                    q.put((dist[new[0]][new[1]],(new[0],new[1])))
                    visited[new[0]][new[1]] = True
            if(len(mat)-node[0]>2):
                new = [node[0]+2,node[1]]
                wall = [node[0]+2,node[1]]
                if (not mat[wall[0]][wall[1]] and (not visited[new[0]][new[1]] or dist[new[0]][new[1]] > dist[node[0]][node[1]] +1)):
                    dist[new[0]][new[1]] = dist[node[0]][node[1]] +1
                    q.put((dist[new[0]][new[1]],(new[0],new[1])))
                    visited[new[0]][new[1]] = True
            if(len(mat[0])-node[1]>2):
                new = [node[0],node[1]+2]
                wall = [node[0],node[1]+2]
                if (not mat[wall[0]][wall[1]] and (not visited[new[0]][new[1]] or dist[new[0]][new[1]] > dist[node[0]][node[1]] +1)):
                    dist[new[0]][new[1]] = dist[node[0]][node[1]] +1
                    q.put((dist[new[0]][new[1]],(new[0],new[1])))
                    visited[new[0]][new[1]] = True
            #print(dist[end[0]][end[1]])

    return dist[end[0]][end[1]]
    return 1
