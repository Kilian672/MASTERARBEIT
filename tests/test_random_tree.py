# random_tree.py

import unittest
from src.random_tree import RANDOMTREE
# all entries within <> are placeholders

class TestClass(unittest.TestCase):


    def test_get_number_of_nodes(self):

        rt = RANDOMTREE(2,2)
        non = rt.get_number_of_nodes()
        self.assertIsInstance(non, int)
        self.assertLess(non, 8)
        self.assertGreater(non, 2)

    def test_init_tree(self): 

        ### Init tree via adjacency list 
        # Without colors and weights
        adj_list = {0: {"children": [1,2,3]}, 
                    1: {"children": []}, 
                    2: {"children": []}, 
                    3: {"children": []}}
        rt = RANDOMTREE(adj_list=adj_list)
        self.assertEqual(rt.get_number_of_nodes(), 4)
        self.assertEqual(rt.get_number_of_colors(), 1)

        # With random colors 
        rt = RANDOMTREE(adj_list=adj_list, colors=3)
        self.assertEqual(rt.get_number_of_nodes(), 4)
        self.assertLessEqual(rt.get_number_of_colors(), 3)
        self.assertGreaterEqual(rt.get_number_of_colors(), 1)

        for node in adj_list.keys(): 
            if node%2 == 0: 
                adj_list[node]["color"] = 1
            else: 
                adj_list[node]["color"] = 2
        rt = RANDOMTREE(adj_list=adj_list)
        self.assertEqual(rt.get_number_of_colors(), 2)



        
		

if __name__ == '__main__':
    unittest.main()