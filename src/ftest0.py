import pandas as pd
from bigtree import dict_to_tree, postorder_iter
import sys 
import matplotlib.pyplot as plt 

class FTEST0: 

    def __init__(self, T, Lambda, k): 
        self.T = T
        self.Lambda = Lambda
        self.k = k
        self.root = dict_to_tree(self.T)

    def test_feasibility(self):

        count = 0
        for node in postorder_iter(self.root):
            node.sup = sys.maxsize
            node.dem = self.Lambda/node.weight

        for node in postorder_iter(self.root):
            for child in node.children: 
                if child.sup <= child.dem: 
                    node.sup = min(node.sup, child.sup + child.dist_par)
                else: 
                    if child.dem < child.dist_par: 
                        count = count + 1       # place a center on the edge e(u,v) at distance dem(u) from u
                        node.sup = min(node.sup, child.dist_par - child.dem)
                    else: 
                        node.dem = min(node.dem, child.dem - child.dist_par)

        if self.root.root.sup > self.root.root.dem:  
            count = count + 1

        return count <= self.k

    def draw_algorithm(self): 
        
 
        figure, axes = plt.subplots() 
        cc = plt.Circle(( 0.5 , 0.5 ), 0.4 , alpha=0.1) 
        
        axes.set_aspect( 1 ) 
        axes.add_artist( cc ) 
        plt.title( 'Colored Circle' ) 
        plt.show()      




if __name__ == "__main__": 
    
    Lambda = 50
    k = 1

    T = {
        "f": {"weight": 90, "dist_par": 20},
        "f/g": {"weight": 65, "dist_par": 30},
        "f/g/i": {"weight": 40, "dist_par": 70}, 
        "f/g/i/h": {"weight": 50, "dist_par": 40},
        "f/b": {"weight": 60, "dist_par": 10},
        "f/b/d": {"weight": 40, "dist_par": 5},
        "f/b/d/e": {"weight": 30, "dist_par": 50}, 
        "f/b/d/c": {"weight": 50, "dist_par": 30}, 
        "f/b/a": {"weight": 35, "dist_par": 30},
    }

    ftest0 = FTEST0(T, Lambda, k)
    #print(ftest0.test_feasibility())
    ftest0.draw_algorithm()
    
    #root = dict_to_tree(path_dict)

    #root.show(attr_list=["weight"])

    #print([node.node_name for node in postorder_iter(root)])