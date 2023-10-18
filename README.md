# MASTERARBEIT
Project to store all the code for the Algorithms used while doing research for my master thesis. 

## Create Random Tree
In this section we will explain how to initialize an object of  the RANDOMTREE class. The RANDOMTREE class is used to generate random samples of a tree. There are different options to either color the nodes or to add edge weights. Also one can initialize a deterministict tree by simply providing an adjacency list for the nodes. The RANDOMTREE class has several usefull functions such as a function to visualize the tree. In the following we will give examples on how to create a RANDOMTREE object and how to visualize it. 

### Create Tree randomly
If you want to create a random sample of a tree you simply have to specify the height and the maximum number of children (max_noc) for each node. You can also specify the maximal distance between to adjacent nodes and the number of colors to color the tree. The draw_tree() method of the RANDOMTREE class provides a visualization of the tree. The code snippet below shows how you can create a RANDOMTREE object and how to visualize it. 

```python
if __name__ == "__main__": 

    random_tree = RANDOMTREE(height=2, max_noc = 2, max_dist = 2, colors= 2)
    random_tree.draw_tree()

```

### Create Tree via adjacency list
You can also create a RANDOMTREE object using an adjacency list. The code snippet below shows how such a list should look like. 

```python
adj_list = { 
                0: {"children": [1,2], "color": 1} 
                1: {"children": [3], "color": 2, "dist_to_par": 2}, 
                2: {"children": []}, 
                3: {"children": [], "color": 1}
            }
```
The "dist_to_par" key stands for the distance of the node to its parent node. The "color" key stands for the color you want to assign to the node (Color 1, Color 2, Color 3, ...). Please make sure to use only colors greater then or equal to 1. The more numbers you provide the more colors you get. The "children" key stands for the children of the node. Please provide a list containing the indices of the nodes you want to assign to the node as children. As you can see in the example it is not necessary to always provide a color or a distance to the parent. Missing information will be filled by default values (the default for "color" is 1 and the default for "dist_to_par" is also 1). If you provide values for "max_dist" or "colors" parameter while defining a new object of the RANDOMTREE class, missing information will be filled randomly. 
A complete example for the initialization of a RANDOMTREE object via adjacency list could look like this: 
```python
if __name__ == "__main__": 

    adj_list = { 
                    0: {"children": [1,2], "color": 1} 
                    1: {"children": [3], "color": 2, "dist_to_par": 2}, 
                    2: {"children": []}, 
                    3: {"children": [], "color": 1}
                }

    random_tree = RANDOMTREE(adj_list=adj_list, max_dist = 2, colors= 2)
    random_tree.draw_tree()
``` 

## Solve Linear Programm

