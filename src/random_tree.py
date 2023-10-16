import random
import networkx as nx 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
import numpy as np


class RANDOMTREE:
   
    """
    This class is used to generate a Tree object, either randomly or by giving it an adjacency list. 

    Attributes
    ----------
    height : int
        The height of the randomly generated Tree. 
    max_noc : int
        The maximum number of children for each node. 
    adj_list : dict
        An adjacency list to generate the Tree from. 
    max_dist : int
        Maximum distance from child to parent node. 
    colors : int
        The number of colors to use for the nodes. 

    Methods
    -------
    get_number_of_nodes()
        Return number of nodes in tree. 
    get_color_dict()
        Return dictionary where the keys are the nodes and the items are the colors of the nodes. 
    get_color_list()
        Return a list with unique colors. 
    get_number_of_colors()
        Return number of colors used to color the nodes.  
    get_dist_mat()
        Return a matrix that contains the weighted distances between node i and j for each i and j.  
    init_tree()
        Helper function to initialize the tree either from an adjacency matrix or randomly.
    create_random_tree()
        Helper function to recursively create a random tree as an adjacency matrix.  
    draw_tree()
        Draw tree.

    Examples
    -------
    Either create a RANDOMTREE object by giving it a height and the maximum number of children for each node 
    or by giving it an adjacency list. You can also provide the adjacency list without colors. 
    >>> random_tree = RANDOMTREE(height=4, max_noc=3, edge_weights=True, colors=2)
    >>> adj_list = {0: {"children": [1], "color": 2},
    ...             1: {"children": [2, 3], "color": 1}, 
    ...             2: {"children": [], "color": 2}, 
    ...             3: {"children": [], "color": 1}
    ...             }
    >>> random_tree = RANDOMTREE(adj_list=adj_list, edge_weights=True)
    For further examples please see the README.md file. 
    """

    def __init__(self, height=1, max_noc=1, adj_list=None, edge_weights=True, max_dist=None, colors=None):
            	
        self.height = height
        self.max_noc = max_noc 
        self.adj_list = adj_list
        self.max_dist = max_dist
        self.colors = colors
        
        self.Tree = self.init_tree()

    def get_number_of_nodes(self): 
        """
        Get the number of nodes of the tree. 

        Returns
        -------
            int: number of nodes in Tree 
        """
        return len(self.Tree.nodes)
    
    def get_color_dict(self): 

        return {node[0]: node[1] for node in self.Tree.nodes.data("color")}
    
    def get_color_list(self): 

        return list(set([node[1] for node in self.Tree.nodes.data("color")]))

    def get_number_of_colors(self):
        """
        Get the numbeer of colors used to color the tree. 

        Returns
        -------
            int: number of colors
        """
        
        return len(self.get_color_list())

    def get_dist_mat(self): 
        """
        Return a matrix that contains the weighted distances between node i and j for each i and j.  

        Returns
        -------
            np.array: weighted distances between nodes 
        """
        # Compute the distance between each nodes
        apd = dict(nx.all_pairs_dijkstra(self.Tree, weight="weight"))
        dim = len(apd.keys())
        dist_mat = np.zeros((dim, dim))
        for i in apd.keys(): 
            for j in apd[i][0].keys(): 
                dist_mat[i][j] = apd[i][0][j]
    
        return dist_mat
    
    def init_tree(self): 
        """Helper function to initialize the tree either from an adjacency matrix or randomly."""
        
        if self.adj_list is None: 
            # If there is no adjacency list we have to generate a random tree
            tree = self.create_random_tree(self.height, self.max_noc)[0]
        else: 
            tree = self.adj_list

        T = nx.Graph()

        for node in tree.keys(): 
            
            if self.adj_list is None: 
                if self.colors is None: 
                    T.add_node(node, color = 1)
                else: 
                    noc_ = min(len(tree.keys()), self.colors)
                    T.add_node(node, color = random.randint(1, noc_))
                children = tree[node]
            else: 
                if self.colors is None: 
                    T.add_node(node, color = tree[node].get('color', 1))
                else: 
                    noc_ = min(len(tree.keys()), self.colors)
                    T.add_node(node, color = tree[node].get('color', random.randint(1, noc_)))
                children = tree[node]['children']
            
            
            for child in children: 
                if self.adj_list is None: 
                    if self.max_dist is None: 
                        T.add_edge(node, child, weight = 1)
                    else: 
                        T.add_edge(node, child, weight = random.randint(1, max(1, self.max_dist)))
                else: 
                    if self.max_dist is None: 
                        T.add_edge(node, child, weight = tree[child].get('dist_to_par', 1))
                    else: 
                        T.add_edge(node, child, weight = 
                                   tree[child].get('dist_to_par', random.randint(1, max(1, self.max_dist))))
                
        return T

    def create_random_tree(self, height, max_noc): 

        if height < 0: 
            return None 
        
        if height == 0: 
            return {0: []} 
        
        if height == 1:
            random_list = list(range(1, 1+random.randint(1,max_noc)))
            tree = {0: random_list}
            for index in random_list: 
                tree[index] = []
            return [tree, random_list]
        else:
            tree_info = self.create_random_tree(height-1, max_noc)
            tree = tree_info[0]
            current_nodes = tree_info[1]
            max_index = max(tree.keys())
            new_nodes = []

            while new_nodes == []: 
                for node in current_nodes: 
                    max_index = max(tree.keys())
                    random_list = list(range(max_index+1, max_index+1+random.randint(1,max_noc)))
                    tree[node] = random_list
                    for index in random_list: 
                        tree[index] = []
                        new_nodes.append(index)

            return [tree, new_nodes]
    
    def draw_tree(self): 
        """
        Draw tree. 
        Returns
        -------
            None
        """
        pos = nx.spring_layout(self.Tree)
    
        
        cols = [node[1] for node in self.Tree.nodes.data('color')]
        nx.draw_networkx_nodes(self.Tree, pos, node_size = 500, node_color = cols)
        nx.draw_networkx_edges(self.Tree, pos, arrows=False, label="weight")

        # add labels to edges 
         
        edge_labels = {(u_e, v_e): e_weight for u_e, v_e, e_weight in self.Tree.edges.data('weight')}
        nx.draw_networkx_edge_labels(self.Tree, pos, edge_labels = edge_labels)

        nx.draw_networkx_labels(self.Tree, pos)

        # patch_list = []
        # for color in self.get_color_list(): 
        #     patch = mpatches.Patch(color=mpl.colormaps['plasma'](color), label=f'Color {color}')
        #     patch_list.append(patch)
        #patch = mpatches.Patch(color=mpl.colormaps['plasma'](5), label=f'Color {2}')
        #plt.legend(handles=[patch])
        #plt.legend()
        plt.show()

    def get_fairness_vectors(self, delta=0): 

        fairness_vectors = {'alpha': {}, 'beta': {}}

        C = self.get_number_of_nodes()
        colors = self.get_color_list()
        node_colors = self.get_color_dict() 
        for color in colors:
            C_i = list(node_colors.values()).count(color)
            r_i = C_i/C 
            if delta != 0: 
                fairness_vectors['beta'][color] = min(1, r_i/(1-delta))
            else: 
                fairness_vectors['beta'][color] = 1
            fairness_vectors['alpha'][color] = r_i*(1-delta)       

        return fairness_vectors   



if __name__ == "__main__": 

    random_tree = RANDOMTREE(height=2, max_noc = 2, max_dist = 2, colors= 2)
    print(random_tree.get_fairness_vectors(delta=0))
    random_tree.draw_tree()
    