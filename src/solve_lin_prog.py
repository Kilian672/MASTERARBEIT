import sys
import numpy as np
from random_tree import RANDOMTREE

np.set_printoptions(threshold=sys.maxsize, linewidth=200)

class SOlVELINPROG: 

    def __init__(self, random_tree): 
        self.random_tree = random_tree

    def get_matrix(self): 
        
        n = self.random_tree.get_number_of_nodes()
        l = self.random_tree.get_number_of_colors()
        dist_mat = self.random_tree.get_dist_mat()
        node_dict = self.random_tree.node_dict
        cols = n + n*n
        rows = 1 + n + 2*n*n + 2*n*l

        A = np.zeros((rows, cols))

        # First condition: sum(y) <= k
        A[0, 0:n] = np.ones(n)

        # Second condition
        for j in range(1,n+1): 
            A[j, j*n:j*n+n] = -np.ones(n)

        # Third condition
        for j in range(n):
            for i in range(n):
                A[n+1+i+n*j, i] = -1
                A[n+1+i+n*j, n+i+n*j] = 1

        # Fourth condition
        for j in range(n): 
            for i in range(n):
                # A[1+n+n*n+i+4*j, n+i+4*j] = dist_mat[j,i]
                A[1+n+n*n+i+n*j, n+i+n*j] = dist_mat[j,i]

        # Fifth condition
        beta = 1/2
        for c in range(l): 
            for i in range(n): 
                for j in range(n): 
                    if node_dict[j]['color'] == c+1: 
                        #A[1+n+2*n*n+n*c+i, n+j*n+i] = 1-beta
                        A[1+n+2*n*n+n*c+i, n+j*n+i] = 1
                    #else: 
                        #A[1+n+2*n*n+n*c+i, n+j*n+i] = -beta
            
        return A


if __name__ == "__main__":
    
    adj_list = {0: [[1, 2, 3, 4, 5, 6, 7], 1],
                1: [[8, 9, 10, 11, 12, 13], 2], 
                2: [[], 1], 
                3: [[], 1], 
                4: [[], 1], 
                5: [[], 1], 
                6: [[], 1], 
                7: [[], 1],  
                8: [[], 2], 
                9: [[], 2], 
                10: [[], 2], 
                11: [[], 2], 
                12: [[], 2], 
                13: [[], 2]
                }
    random_tree = RANDOMTREE(4, 1, adj_list = adj_list, edge_weights=True, colors=2)
    solve_lin_prog = SOlVELINPROG(random_tree)
    print(solve_lin_prog.get_matrix())
    random_tree.draw_tree()