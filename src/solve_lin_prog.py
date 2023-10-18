import sys
import numpy as np
from scipy.optimize import linprog
try: 
    from src.random_tree import RANDOMTREE
except: 
    from random_tree import RANDOMTREE


np.set_printoptions(threshold=sys.maxsize, linewidth=200)

class SOlVELINPROG: 

    def __init__(self, random_tree, k, alpha, beta): 
    
        self.random_tree = random_tree
        self.k = k 
        self.alpha = alpha
        self.beta = beta
        self.n = self.random_tree.get_number_of_nodes()
        self.l = self.random_tree.get_number_of_colors()
        self.dist_mat = self.random_tree.get_dist_mat()
        self.color_list = self.random_tree.get_color_list()
        self.color_dict = self.random_tree.get_color_dict()
        

    def c(self): 

        n = self.n 
        c = np.ones((n+n*n,))
        c[0:n] = np.zeros(n)
        c[n:] = self.dist_mat.flatten()
        
        return c

    def b(self):

        n = self.n
        l = self.l

        #rows = 1 + n + 2*n*n + 2*n*l #### 1.) 
        rows = 1 + n + n*n + 2*n*l   #### 2.) 
         

        b = np.zeros((rows,))

        # First condition
        b[0] = self.k 

        # Second condition
        b[1:n+1] = -np.ones(n)
        
        # Third condition
        b[n+1: n+1+n*n] = np.zeros(n*n)

        # Fourth condition
        # r = ?
        #b[n+1+n*n: n+1+2*n*n] = r * np.ones(n*n)

        # Fifth condition
        #b[n+1+2*n*n: n+1+2*n*n+2*n*l] = np.zeros(2*n*l)  #### 1.)
        b[n+1+n*n: n+1+n*n+2*n*l] = np.zeros(2*n*l)       #### 2.)          
        
        return b
        

    def A(self): 
        
        n = self.n
        l = self.l 

        cols = n + n*n
        
        #rows = 1 + n + 2*n*n + 2*n*l  #### 1.) 
        rows = 1 + n + n*n + 2*n*l     #### 2.)

        A = np.zeros((rows, cols))

        # First condition
        A[0, 0:n] = np.ones(n)

        # Second condition
        for j in range(n): 
            A[j+1, (j+1)*n:(j+1)*n+n] = -np.ones(n)

        # Third condition
        for j in range(n):
            for i in range(n):
                A[n+1+i+n*j, i] = -1
                A[n+1+i+n*j, n+i+n*j] = 1

        # Fourth condition
        #for j in range(n): 
            #for i in range(n):
                # A[1+n+n*n+i+4*j, n+i+4*j] = dist_mat[j,i]
                #A[1+n+n*n+i+n*j, n+i+n*j] = dist_mat[j,i]
                #A[1+n+n*n+i+n*j, n+i+n*j] = 1

        # Fifth condition
        for c, color in enumerate(self.color_list): 
            for i in self.color_dict.keys(): 
                for j in self.color_dict.keys(): 
                    if self.color_dict[j] == color: 
                        A[1+n+n*n+n*c+i, n+j*n+i] = 1-self.beta[color]
                    else:
                        A[1+n+n*n+n*c+i, n+j*n+i] = -self.beta[color] 

        for c, color in enumerate(self.color_list): 
            for i in self.color_dict.keys(): 
                for j in self.color_dict.keys(): 
                    if self.color_dict[j] == color: 
                        A[1+n+n*n+n*l+n*c+i, n+j*n+i] = self.alpha[color]-1
                    else:
                        A[1+n+n*n+n*l+n*c+i, n+j*n+i] = self.alpha[color] 
                
        return A
    
    def solve_prog(self): 

        b_ub = self.b()
        A_ub = self.A()
        c_ = self.c()
        

        res = linprog(c_, A_ub=A_ub, b_ub=b_ub)
        
        return res

    def get_info(self, x): 

        if x is None: 
            print("The problem is infeasible.")
            return

        x = np.array(x)
        x = x.reshape((int(len(x)/self.n),self.n))

        for j in range(len(x[0])): 
            if x[0][j] > 0: 
                print(f"Node {j} is a center")

        print("-----------------------------------------------------")

        y = x[1:]
        for j in range(y.shape[0]): 
            for i in range(y.shape[1]):
                if y[j][i] > 0: 
                    print(f"Node {j} was assigned to center {i} with probability {y[j][i]}.")




if __name__ == "__main__":
    
    adj_list = {0: {"children": [1, 2, 3, 4, 5, 6, 7], "color": 1},
                1: {"children": [8, 9, 10, 11, 12, 13], "color": 2}, 
                2: {"children": [], "color": 1}, 
                3: {"children": [], "color": 1}, 
                4: {"children": [], "color": 1}, 
                5: {"children": [], "color": 1}, 
                6: {"children": [], "color": 1}, 
                7: {"children": [], "color": 1},  
                8: {"children": [], "color": 2}, 
                9: {"children": [], "color": 2}, 
                10: {"children": [], "color": 2}, 
                11: {"children": [], "color": 2 }, 
                12: {"children": [], "color": 2}, 
                13: {"children": [], "color": 2}
                }
    

    random_tree = RANDOMTREE(2, 2, colors=2)
    fv = random_tree.get_fairness_vectors(delta=0)
    solve_lin_prog = SOlVELINPROG(random_tree, 2, alpha = fv['alpha'], beta = fv['beta'])
    print(solve_lin_prog.A())
    solve_lin_prog.get_info(solve_lin_prog.solve_prog().x)
    random_tree.draw_tree()