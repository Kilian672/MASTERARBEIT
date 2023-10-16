# MASTERARBEIT
Project to store all the code for the Algorithms used while doing research for my master thesis. 

## Create Random Tree
In this section we will explain how to use the RANDOMTREE class for computations. The RANDOMTREE class is used to generate random samples of a tree. There are different options to either color the nodes or to add edge weights. Also one can initialize a deterministict tree by simply providing an adjacency list for the nodes. The RANDOMTREE class has several usefull functions such as a function to visualize the tree. In the following we will give examples on how to create a RANDOMTREE object and how to visualize it. 

### Create Tree randomly
If you want to create a random sample of a tree you simply have to specify the height and the maximum number of children (max_noc) for each node. You can also specify the maximal distance between to adjacent nodes and the number of colors to color the tree. The draw_tree method of the RANDOMTREE class provides a visualisation of the tree. The code snippet below shows how you can create a RANDOMTREE object and how to visualize it. 

```python
if __name__ == "__main__": 

    random_tree = RANDOMTREE(height=2, max_noc = 2, max_dist = 2, colors= 2)
    random_tree.draw_tree()

```

## Solve Linear Programm

