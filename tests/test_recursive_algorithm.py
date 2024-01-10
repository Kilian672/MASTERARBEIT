import unittest
from src.recursive_algorithm import *

# Execute: python -m unittest tests.test_recursive_algorithm.TestRecursiveAlgorithm  
class TestRecursiveAlgorithm(unittest.TestCase):
    def test_fairClustering(self):
        
        # TestCase1
        V = [(1,'g'), (2,'g'), (3,'r'), (4,'g'), (5,'r'), (6,'g'), (7,'r'), (8,'r')]
        erg = fairClustering(V, (1/4, 1/4), (3/4, 3/4), 4)
        self.assertEqual(erg[0], 1.5)
        self.assertDictEqual({1: [(6, 'g'), (8, 'r')], 
                              2: [(4, 'g'), (7, 'r')], 
                              3: [(2, 'g'), (5, 'r')], 
                              4: [(1, 'g'), (3, 'r')]}, erg[1])
        
        # TestCase2
        V = [(1,'g'), (2,'g'), (3,'g'), (4,'g'), (5,'r'), (6,'r'), (7,'r'), (8,'r')]
        erg = fairClustering(V, (1/4, 1/4), (3/4, 3/4), 4)
        self.assertEqual(erg[0], 2.5)
        self.assertDictEqual({1: [(4, 'g'), (8, 'r')], 
                              2: [(3, 'g'), (7, 'r')], 
                              3: [(2, 'g'), (6, 'r')], 
                              4: [(1, 'g'), (5, 'r')]}, erg[1])
        

    def test_fairClustering3(self): 
        pass