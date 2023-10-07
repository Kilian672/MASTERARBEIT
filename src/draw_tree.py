import sys
import networkx as nx
import matplotlib.pyplot as plt


class Tree: 

    def __init__(self, nested_tuple) -> None:
        
        self.T = nx.from_nested_tuple(nested_tuple, sensible_relabeling=True)
        self.attributes = {}
        self.node_colors = {}
    
    def plot_tree(self) -> None:
        
        
        values = [self.node_colors.get(node, 1) for node in self.T.nodes()]

        pos = nx.spring_layout(self.T)
        nx.draw_networkx_nodes(self.T, pos, node_size = 500, node_color=values)
        nx.draw_networkx_labels(self.T, pos)
        nx.draw_networkx_edges(self.T, pos, arrows=False)
        plt.show()

    def test_feasibility(self, lambd, k, weights):
    
        count = 0
        self.attributes = {node:{'sup': sys.maxsize, 'dem': lambd/weights[node][0], 'dist_par': weights[node][1]} 
                           for node in nx.dfs_postorder_nodes(self.T)}

        for node in nx.dfs_postorder_nodes(self.T):
            for child in self.get_children(node):
                if self.attributes[child]['sup'] <= self.attributes[child]['dem']:
                    self.attributes[node]['sup'] = min(self.attributes[node]['sup'], self.attributes[child]['sup']+self.attributes[child]['dist_par'])
                else: 
                    if self.attributes[child]['dem'] < self.attributes[child]['dist_par']: 
                        count = count + 1       # place a center on the edge e(u,v) at distance dem(u) from u
                        self.attributes[node]['sup'] = min(self.attributes[node]['sup'], self.attributes[child]['dist_par'] - self.attributes[child]['dem'])
                        self.node_colors[child] = 0.5
                        print(child)
                        print(self.attributes[node]['sup'])
                    else: 
                        self.attributes[node]['dem'] = min(self.attributes[node]['dem'], self.attributes[child]['dem'] - self.attributes[child]['dist_par'])

        if self.attributes[0]["sup"] > self.attributes[0]["dem"]: 
            self.node_colors[0] = 0.5 
            count = count + 1

        return count <= k

    def get_children(self, node):
        children = []
        for key in nx.all_neighbors(self.T, node): 
            if key > node: 
                children.append(key)
        return children


if __name__ == "__main__": 

    weights = [(1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1), (1,1)]
    nested_tuple = (((),((), ())), ((), (), ()))
    tree = Tree(nested_tuple)
    print(tree.test_feasibility(1, 3, weights))
    tree.plot_tree()