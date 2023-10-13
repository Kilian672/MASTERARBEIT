import random
import networkx as nx 
import matplotlib.pyplot as plt

class RANDOMTREE: 

    def __init__(self, height, max_noc, edge_weights=False):
        self.height = height
        self.max_noc = max_noc 
        self.edge_weights = edge_weights
        self.Tree = self.get_random_tree()
        

    def get_random_tree(self): 
        
        tree_list = self.create_random_tree(self.height, self.max_noc)[0]
        G = nx.Graph()
        G.add_nodes_from(list(tree_list.keys()))
        for node in tree_list.keys():
            if tree_list[node] != []: 
                for child in tree_list[node]: 
                    G.add_edge(node, child, weight=random.randint(1,10))

        return G

    def create_random_tree(self, height, max_noc): 

        if height < 0: 
            return None 
        
        if height == 0: 
            return None 
        
        if height == 1:
            random_list = list(range(2, 2+random.randint(1,max_noc)))
            tree = {1: random_list}
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
                    random_list = list(range(max_index+1, max_index+random.randint(1,max_noc)))
                    tree[node] = random_list
                    for index in random_list: 
                        tree[index] = []
                        new_nodes.append(index)

            return [tree, new_nodes]
    
    def draw_tree(self): 
        
        edge_labels = {(u_e, v_e): e_weight for u_e, v_e, e_weight in self.Tree.edges.data('weight')}
        
        
        pos = nx.spring_layout(self.Tree)
        nx.draw_networkx_nodes(self.Tree, pos, node_size = 500)
        nx.draw_networkx_edges(self.Tree, pos, arrows=False, label="weight")
        nx.draw_networkx_edge_labels(self.Tree, pos, edge_labels= edge_labels)
        nx.draw_networkx_labels(self.Tree, pos)
        plt.show()

    

if __name__ == "__main__": 

    random_tree = RANDOMTREE(5, 3)
    random_tree.draw_tree()
