# test_solve_lin_prog.py

import unittest
import numpy as np

from src.solve_lin_prog import SOlVELINPROG
from src.random_tree import RANDOMTREE


class TestClass(unittest.TestCase):

    def test_b(self): 
        
        adj_list = {0: {"children": [1,2]}, 
                    1: {"children": [3]}, 
                    2: {"children": []}, 
                    3: {"children": []}}

        rt = RANDOMTREE(adj_list = adj_list)
        fv = rt.get_fairness_vectors(delta=0)
        lprog = SOlVELINPROG(rt, 2, alpha = fv['alpha'], beta = fv['beta'])

        b = lprog.b()
        b_ = np.array([2, 
                       -1, -1, -1, -1, 
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0])
        
        self.assertEqual(b, b_)