from algorithms.motion_planning import *
import numpy as np

if __name__ == '__main__':
    #Le matrici vanno date verticalmente
    #mat = np.matrix("0 1 0 1 0 1 0 1 0; 1 0 1 0 1 0 0 0 1; 0 0 0 0 0 0 0 0 0; 1 0 1 0 0 0 1 0 1; 0 0 0 0 0 0 0 0 0; 1 0 0 0 1 0 1 0 1; 0 1 0 1 0 0 0 1 0")
    mat = np.matrix("0 1 0 1 0 1 0; 1 0 0 0 0 0 1; 0 1 0 1 0 0 0; 1 0 0 0 0 0 1; 0 1 0 0 0 1 0; 1 0 0 0 0 0 0; 0 0 0 1 0 1 0; 1 0 0 0 0 0 1; 0 1 0 1 0 1 0")
    #print(dijkstra([1,1],[3,3],mat))
    available = [[7,5],[3,1]]
    print(best_path(1,[1,1],available,mat))
