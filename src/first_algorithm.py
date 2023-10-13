def compute_clusters(Tree, k):
    '''
    Computes (unfair) clustering on given tree with k-center objective.

            Parameters:
                    Tree (dict): A dictionary representing the tree as adjacency list. 
                    k (int): The number of centers to compute. 
            Returns:
                    clusters (list): list of subtrees which are the clusters
            
    ''' 
    pass

def is_not_fair(cluster, alpha, beta): 
    '''
    Checks whether a cluster is fair or not w.r.t given fairness vectors.

            Parameters:
                    cluster (dict): A dictionary representing a cluster of the original tree as adjacency list. 
                    alpha (list): The lower bound fairness vector. 
                    beta (list): The upper bound fairness vector. 
            Returns:
                    True or False
            
    ''' 
    pass

def get_next_node(Tree, cluster, unused_nodes): 
    pass

def improves_fairness(node, cluster, alpha, beta): 
    pass

def is_center(node): 
    pass

def find_best_centers(Tree, centers, k): 
    pass

def fair_tree_clustering(Tree, k, alpha, beta): 
    '''
    Computes fair clustering on given tree w.r.t fairness conditions given by fairness vectors.

            Parameters:
                    Tree (dict): A dictionary representing the tree as adjacency list. 
                    k (int): The number of centers to compute. 
                    alpha (list): The lower bound fairness vector. 
                    beta (list): The upper bound fairness vector.

            Returns:
                    
    '''


    clusters = compute_clusters(Tree, k)

    saved_unused_nodes = []
    new_centers = []

    for cluster in clusters: 
        center_count = 0
        while is_not_fair(cluster, alpha, beta): 
            next_node = get_next_node(Tree, cluster, saved_unused_nodes)
            if improves_fairness(next_node, cluster, alpha, beta):
                cluster.append(next_node)
                if is_center(next_node): 
                    center_count = center_count + 1
            else: 
                saved_unused_nodes.append(next_node) 

        new_centers.append(fair_tree_clustering(cluster, center_count, alpha, beta))

    return find_best_centers(Tree, new_centers, k)



Tree = {0: {"children": [1,2], "groups": ["red"]},
        1: {"children": [3,4], "groups": ["red"]}, 
        2: {"children": [5,6,7], "groups": ["green"]}, 
        4: {"children": [8,9], "groups": ["green"]},
        5: {"children": [10], "groups": ["green"]},
        6: {"children": [], "groups": ["red"]},
        7: {"children": [], "groups": ["green"]},
        8: {"children": [], "groups": ["red"]},
        9: {"children": [], "groups": ["red"]},
        10: {"children": [], "groups": ["green"]},
         }

alpha = [0.5, 0.5]
beta = [0.5, 0.5]


fair_tree_clustering(Tree, 2, alpha, beta)