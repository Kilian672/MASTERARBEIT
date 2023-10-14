import random
import networkx as nx 
import matplotlib.pyplot as plt
import numpy as np


class RANDOMTREE: 

    def __init__(self, height, max_noc, edge_weights=True, colors=None):
        self.height = height
        self.max_noc = max_noc 
        self.edge_weights = edge_weights
        self.colors = colors
        self.Tree = self.get_random_tree()
        if self.colors is not None: 
            self.node_dict = self.color_tree()
        else: 
            self.node_dict = None

    def get_number_of_nodes(self): 
        return len(self.Tree.nodes)
    
    def get_number_of_colors(self):
        
        if self.colors is not None: 
            return self.colors
        else: 
            return 1

    def color_tree(self): 
        node_dict = {}
        for node in self.Tree.nodes.keys():
            node_dict[node] = {"color": random.randint(1,self.colors)}

        return node_dict    

    def get_dist_mat(self): 
        
        apd = dict(nx.all_pairs_dijkstra(self.Tree, weight="weight"))
        #print(apd)
        dim = len(apd.keys())
        dist_mat = np.zeros((dim, dim))
        for i in apd.keys(): 
            for j in apd[i][0].keys(): 
                dist_mat[i][j] = apd[i][0][j]

        return dist_mat
     
    def get_random_tree(self): 
        
        tree_list = self.create_random_tree(self.height, self.max_noc)[0]
        G = nx.Graph()
        G.add_nodes_from(list(tree_list.keys()))
        for node in tree_list.keys():
            if tree_list[node] != []: 
                for child in tree_list[node]: 
                    if self.edge_weights: 
                        G.add_edge(node, child, weight=random.randint(1,10))
                    else: 
                        G.add_edge(node, child)

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
        
        pos = nx.spring_layout(self.Tree)
    
        if self.node_dict is not None: 
            cols = [self.node_dict[node]["color"] for node in self.node_dict.keys()]
            nx.draw_networkx_nodes(self.Tree, pos, node_size = 500, node_color = cols)
        else: 
            nx.draw_networkx_nodes(self.Tree, pos, node_size = 500)
        nx.draw_networkx_edges(self.Tree, pos, arrows=False, label="weight")

        # add labels to edges 
        if self.edge_weights: 
            edge_labels = {(u_e, v_e): e_weight for u_e, v_e, e_weight in self.Tree.edges.data('weight')}
            nx.draw_networkx_edge_labels(self.Tree, pos, edge_labels= edge_labels)

        nx.draw_networkx_labels(self.Tree, pos)
        plt.show()

    

if __name__ == "__main__": 

    random_tree = RANDOMTREE(2, 2, edge_weights=True, colors=2)
    print(random_tree.Tree.nodes)
    random_tree.draw_tree()
    
