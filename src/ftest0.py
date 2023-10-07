import pandas as pd
from bigtree import dict_to_tree, postorder_iter, levelorder_iter
import sys 
import matplotlib.pyplot as plt 

class FTEST0: 

    def __init__(self, T, Lambda, k): 
        self.T = T
        self.Lambda = Lambda
        self.k = k
        self.root = dict_to_tree(self.T)

    def get_height(self): 
        
        height = 0
        for key in self.T.keys():
            pos = len(key.split("/"))
            if pos > height:
                height = pos

        return height 

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
        height = self.get_height()
        parent_dict = {}
        
        for node in levelorder_iter(self.root): 
            if node.is_root: 
                cc = plt.Circle((2**height/2, 2*height), 0.5)
                axes.add_artist( cc )
                parent_dict[node.node_name] = (2**height/2, 2*height)
                children = node.children
                if len(children) == 1: 
                    cc = plt.Circle((2**height/2, 2*height-1), 0.5)
                    axes.add_artist( cc )
                    parent_dict[children[0].node_name] = (2**height/4, 2*height-1)
                else: 
                    cc1 = plt.Circle((2**height/4, 2*height-1), 0.5)
                    cc2 = plt.Circle(((3*(2**height))/4, 2*height-1), 0.5)
                    axes.add_artist(cc1)
                    axes.add_artist(cc2)
                    parent_dict[children[0].node_name] = (2**height/4, 2*height-1)
                    parent_dict[children[1].node_name] = ((3*(2**height))/4, 2*height-1)
                
            else: 
                children = node.children
                current_depth = len(node.path_name.split(node.sep))#
                if len(children) == 0 or children is None: 
                    continue
                if len(children) == 1:
                    par_tup = parent_dict[node.node_name]
                    cc= plt.Circle((par_tup[0], par_tup[1]-1), 0.5) 
                    parent_dict[children[0].node_name] = (par_tup[0], par_tup[1]-1)
                    axes.add_artist(cc)
                else: 
                    par_tup = parent_dict[node.node_name]
                    cc1 = plt.Circle((par_tup[0]+1/2, par_tup[1]-1), 0.5)
                    cc1 = plt.Circle((par_tup[0]-1/2, par_tup[1]-1), 0.5)
                    parent_dict[children[0].node_name] = (par_tup[0]+1/2, par_tup[1]-1)
                    parent_dict[children[1].node_name] = (par_tup[0]-1/2, par_tup[1]-1)
                    axes.add_artist(cc1)
                    axes.add_artist(cc2)
                
        self.root.show(attr_list=["weight"])
        axes.set_aspect( 1 ) 
        print(parent_dict)
                
            # for child in node.children: 

            #     print(node)
            #     cc = plt.Circle(( 0.5 , 0.5 ), 0.4 , alpha=0.1) 
                
            #     axes.set_aspect( 1 ) 
            #     axes.add_artist( cc ) 
        
        plt.title( 'Colored Circle' ) 
        plt.xlim(0, 2**height)
        plt.ylim(0, 2*height+1)
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
    #print(ftest0.get_height())
    #root = dict_to_tree(path_dict)

    #root.show(attr_list=["weight"])

    #print([node.node_name for node in postorder_iter(root)])