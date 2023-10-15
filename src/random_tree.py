import random
import networkx as nx 
import matplotlib.pyplot as plt
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
    edge_weights : bool
        If true, each edge will get (randomly generated) weights between 0 and 10. 
        If false, the edges will be weighted equally with value 1. 
    colors : int
        The number of colors to use for the nodes. 

    Methods
    -------
    get_number_of_nodes()
        Return number of nodes in tree. 
    get_number_of_colors()
        Return number of colors used to color the nodes.  
    get_dist_mat()
        Return a matrix that contains the weighted distances between node i and j for each i and j.  
    init_tree()
        Helper function to initialize the tree from the adjacency matrix.
    init_random_tree()
        Helper function to initialize a randomly generated tree. 
    create_random_tree()
        Helper function to create a random tree as adjacency list. 
    draw_tree()
        Draw tree.

    Examples
    -------
    Either create a RANDOMTREE object by giving it a height and the maximum number of children for each node 
    or by giving it a adjacency matrix. You can also provide the adjacency matrix without colors. 
    >>> random_tree = RANDOMTREE(height=4, max_noc=3, edge_weights=True, colors=2)
    >>> adj_list = {0: {"children": [1], "color": 2},
    ...             1: {"children": [2, 3], "color": 1}, 
    ...             2: {"children": [], "color": 2}, 
    ...             3: {"children": [], "color": 1}
    ...             }
    >>> random_tree = RANDOMTREE(adj_list=adj_list, edge_weights=True)

    """

    def __init__(self, height=1, max_noc=1, adj_list=None, edge_weights=True, colors=None):
        self.height = height
        self.max_noc = max_noc 
        self.adj_list = adj_list
        self.edge_weights = edge_weights
        self.colors = colors
        if self.adj_list is None: 
            self.Tree = self.init_random_tree()
        else: 
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
        
        apd = dict(nx.all_pairs_dijkstra(self.Tree, weight="weight"))
        dim = len(apd.keys())
        dist_mat = np.zeros((dim, dim))
        for i in apd.keys(): 
            for j in apd[i][0].keys(): 
                dist_mat[i][j] = apd[i][0][j]
    
        return dist_mat
    
    def init_tree(self): 
        """
        Helper function to initialize the tree from the adjacency matrix.

        Returns
        -------
            A tree using nx.Graph() from networx module

        """
        tree_list = self.adj_list
        G = nx.Graph()
        for node in tree_list.keys():
            G.add_node(node, color = tree_list[node].get("color", 1))
            if tree_list[node]["children"] != []: 
                for child in tree_list[node]["children"]: 
                    if self.edge_weights: 
                        G.add_edge(node, child, weight = random.randint(1,10))
                    else: 
                        G.add_edge(node, child, weight = 1)

        return G

    def init_random_tree(self): 
        """
        Helper function to initialize a randomly generated tree with weights.

        Returns
        -------
            A tree using nx.Graph() from networx module

        """
        tree_list = self.create_random_tree(self.height, self.max_noc)[0]
        G = nx.Graph()
        for node in tree_list.keys():
            if self.colors is None: 
                G.add_node(node, color = 1)
            else: 
                colors = min(len(tree_list.keys()), self.colors)
                G.add_node(node, color = random.randint(1, colors))
            if tree_list[node] != []: 
                for child in tree_list[node]: 
                    if self.edge_weights: 
                        G.add_edge(node, child, weight = random.randint(1,10))
                    else: 
                        G.add_edge(node, child, weight = 1)

        return G
    
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
        if self.edge_weights: 
            edge_labels = {(u_e, v_e): e_weight for u_e, v_e, e_weight in self.Tree.edges.data('weight')}
            nx.draw_networkx_edge_labels(self.Tree, pos, edge_labels = edge_labels)

        nx.draw_networkx_labels(self.Tree, pos)
        plt.show()

    

if __name__ == "__main__": 

    adj_list = {0: {"children": [1], "color": 2},
                1: {"children": [2, 3], "color": 1}, 
                2: {"children": [], "color": 2}, 
                3: {"children": [], "color": 1}
                }
    
    random_tree = RANDOMTREE(height=2, max_noc=2, edge_weights=False, colors=2)
    print(random_tree.get_color_dict())
    print(random_tree.Tree.nodes.data("color"))
    random_tree.get_dist_mat() 
    #random_tree.draw_tree()