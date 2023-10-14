from random_tree import RANDOMTREE
import numpy as np

class SOlVELINPROG: 

    def __init__(self, random_tree): 
        self.random_tree = random_tree

    def get_matrix(self, n, l): 
        
        n = self.random_tree.get_number_of_nodes()
        l = self.random_tree.get_number_of_colors()
        dist_mat = self.random_tree.get_dist_mat()
        cols = n + n*n
        rows = 1 + n + 2*n*n + n*l

        A = np.zeros((rows, cols))

        A[0, 0:n] = np.ones(n)
        for j in range(1,n+1): 
            A[j, j*n:j*n+n] = np.ones(n)

        for j in range(n):
            for i in range(n):
                A[n+1+i+4*j, j] = 1
                A[n+1+i+4*j, n+i+4*j] = 1

        for j in range(n): 
            for i in range(n):
                # A[1+n+n*n+i+4*j, n+i+4*j] = dist_mat[j,i]
                A[1+n+n*n+i+4*j, n+i+4*j] = dist_mat[j,i]

            

        return A


if __name__ == "__main__":
    
    random_tree = RANDOMTREE(2, 2, edge_weights=True, colors=2)
    solve_lin_prog = SOlVELINPROG(random_tree)
    print(solve_lin_prog.get_matrix(4,2))