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
                        0: {"children": [1,2], "color": 1}, 
                        1: {"children": [3], "color": 2, "dist_to_par": 2}, 
                        2: {"children": []}, 
                        3: {"children": [], "color": 1}
                }
```
* **color** = color you want to assign to the node, i.e. Color 1 or Color 2 or Color 3 ... . Please make sure to use only colors greater then or equal to 1. The more numbers you provide the more colors (or groups) you get.
* **dist_to_par** = distance of the node to its parent node

* **children** = list of all the nodes who are children of the node
 
As you can see in the example above it is not necessary to always provide a color or a distance to the parent node. Missing information will be filled with default values (the default for **color** is 1 and the default for **dist_to_par** is also 1). If you provide values for the **max_dist** or **colors** parameter while initializing a new object of the RANDOMTREE class, missing information will be filled randomly. 
A complete example for the initialization of a RANDOMTREE object via adjacency list could look like this: 
```python
if __name__ == "__main__": 

    adj_list = { 
                        0: {"children": [1,2], "color": 1}, 
                        1: {"children": [3], "color": 2, "dist_to_par": 2}, 
                        2: {"children": []}, 
                        3: {"children": [], "color": 1}
                }

    random_tree = RANDOMTREE(adj_list=adj_list, max_dist = 2, colors= 2)
    random_tree.draw_tree()
``` 
> **_NOTE:_**  If you don't provide a **children** key for one node the code will assume, that the node is a leave.


## Solve Linear Programm
In the following we will explain how we can use the SOLVELINPROG class to set up and solve the following LP associated to a RANDOMTREE object: 

![LP1](/img/LP1.jpg "Optionaler Titel")


1. First we have to create another RANDOMTREE object by either providing an adjacency list or by providing a height and a maximal number of children for each node. Additionaly we can provide the number of colors to generate and the maximal distance from a node to its parent. The code is shown below.
```python
    # initialize RANDOMTREE object 
    random_tree = RANDOMTREE(2, 3, colors=2)
```
2. Now we have to get the fairness vectors from the RANDOMTREE class. For this we can call the get_fairnees_vectors() method from the RANDOMTREE class as shown below. The $\alpha_c$ and $\beta_c$ values will be choosen according to the relative amout of nodes colored with color c. We will see in step 3. how to use the fairness vectors.
```python
    # get fairness vectors
    fv = random_tree.get_fairness_vectors()
```
> **_NOTE:_**  The get_fairness_vectors() method can also take a parameter $\delta$ between 0 and 1 which stands for how relaxed the fairness constraints should be. 

3. Now we can use the fairness vectors calculated above to create a SOLVELINPROG object. The code is as follows
```python
    # initialize SOLVELINPROG object to solve LP
    solve_lin_prog = SOlVELINPROG(random_tree, k=2, alpha = fv['alpha'], beta = fv['beta'])
```
* **random_tree**: the RANDOMTREE object calculated above
* **k**: number of centers to calculate
* **alpha**: the alpha fairness vector calculated above
* **beta**: the beta fairness vector calculated above

4. Finally the only thing left is to calculate our result and visualize it. 
The code is as follows
```python
    # Solve LP and get information about assignment
    solve_lin_prog.get_info(solve_lin_prog.solve_prog().x)
    # Draw random tree
    random_tree.draw_tree()
```
This will calculate the result of the above mentioned LP for the RANDOMTREE object and print it to the console. Also this will visualize the tree with its colors. 

The complete example looks like this: 
```python
if __name__ == "__main__":
    
    # initialize RANDOMTREE object 
    random_tree = RANDOMTREE(2, 3, colors=2)
    # get fairness vectors
    fv = random_tree.get_fairness_vectors()
    # initialize SOLVELINPROG object to solve LP
    solve_lin_prog = SOlVELINPROG(random_tree, k=2, alpha = fv['alpha'], beta = fv['beta'])
    # Solve LP and get information about assignment
    solve_lin_prog.get_info(solve_lin_prog.solve_prog().x)
    # Draw random tree
    random_tree.draw_tree()

```