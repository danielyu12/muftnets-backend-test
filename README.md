# MuFnets Algorithm API
## Micro-fluidic cell-cell network tool

### Summary
This novel tool enables biologists to create custom communication networks for cells. Users then compile their network of cells to obtain a more organized layout of mono-layer chambers.

![image](https://user-images.githubusercontent.com/54071115/214073247-e092e1fc-da72-4d30-9473-e0da6402f6ae.png)

Users will be able to specify the types of cells in a network by modifying the User Requirements (UR)

![image](https://user-images.githubusercontent.com/54071115/214073527-321b7952-e651-4312-bbf8-c9873b84c8b8.png)

The image above represents a super-simplified version of a network involving two cells, A & B

### The Code

*Final Verison* of this code is under Final_Algorithm
```
uF_networkAlgo.py
uF_main.py
```

### Testing

##### 1) in a seperate file, import the Algorithm API. Similar format as in uF_main.py
```
import uF_networkAlgo
 # or
import uF_networkAlgo as NAME
```
##### 2) To use this algorithm you must obtain 3 values:<br>
  a) ```<string> root``` - root is the starting cell-node in the network topology the user has defined<br>
  b) ```<string> array nodes``` - nodes is an array of string objects of the cell-nodes in the network topology<br>
  c) ```<string, string array> map adjList``` adjList represents connections for all cell-nodes in the topology -> ('src' : ['dest 1', 'dest 2'])<br>

##### 3) Once these values are obtained, run:<br>
```
uF_networkAlgo.algorithm(root, nodes, adjList)
 # with 'as' renaming
NAME.algorithm(root, nodes, adjList)
```

### Algorithms used
1) Breadth First and Depth First Travseral Algorithms<br>
2) Topological Sort<br>
3) Prim's Minimum Spanning Tree Algorithm<br>
