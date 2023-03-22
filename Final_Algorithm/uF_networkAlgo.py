"""
uF_networkAlgo.py


input: array<string>, array<string:array<string>>
    adjecency list representing cell to cell edges 
    map of each key to an array representing each node's characteristics

output: array<tuple<int,string>>, map<string:string>, array<string>


copyright Oliveira Lab 2023
"""



# Initialize field variable

def algorithm(root, nodes, adjList):
    PI = {}
    topoSorted = {}
    ordered = {}

    # print("adjList",adjList)
    if adjList == None:
        return None

    # 1 Populate predecessor array
    for pair in adjList:
        temp = pair.split(":")
        src = temp[0]
        dest = temp[2] 

        numType = None
        if temp[1] == "C":
            numType = 0
        elif temp[1] == "S":
            numType = 1
        elif temp[1] == "L":
            numType = 2

        
        if PI.get(src) == None:
            PI[src] = (None,None,0)
        PI[dest] = (src,temp[1],0)
    
    # 2 Determine if MST connects to all nodes (no need to check for cycles for MST)
    mst = MinimumSpanningTree(root, adjList)
    
    # 3 Run Topological Sort & Adjecency List Algorithms
    topoSorted = TopologicalSort(PI)
    parsedAdjList = CreateSortedAdjList(PI)

    # 4 Get completed mapping
    temp_topoSorted = topoSorted.copy()
    while temp_topoSorted:
        temp = temp_topoSorted.pop()
        if ordered.get(temp) == None:
            ShortestBranch(parsedAdjList, temp,0, ordered)     
    Optimize(ordered)

    # 5 Unfold completed mapping
    endpoints, unfolded = PostProcess(root, ordered, topoSorted)

    # 6 identify devices
    # 7 Return values
    print("predecessor array\t",PI)
    print("topological sorted\t",topoSorted)
    print("ordered adj list \t",ordered)
    print("endpoints \t\t",endpoints)
    print("unfolded adj list\t",unfolded)
    return PI, topoSorted, ordered, endpoints, unfolded

### HELPER FUNCTIONS AND ALGORITHMS ###

def MinimumSpanningTree(root, str_adjList):
    kv_adjList = {}

    # Parse adjlist
    for edge in str_adjList:
        temp = edge.split(":")
        src = temp[0]
        t = temp[1]
        dest = temp[2] 

        if kv_adjList.get(src) == None:
            kv_adjList[src] = []

        kv_adjList[src].append((dest,t,0))

    # Run BFS
    Q = [root]
    minSpanningTree = []
    visited = []
    edges = []

    # while the Queue is not empty
    while Q:    
        # pop the first element                        
        parent = Q.pop(0)

        if kv_adjList.get(parent) == None:
            continue

        children = kv_adjList[parent]
        
        # enqueue each child from parent node into the queue
        while children:
            child,t,_ = children.pop(0)
            if child not in visited and child not in Q:
                Q.append(child)
                
                if (parent, child) not in edges and (child, parent) not in edges:
                    edges.append((parent,child))
                    minSpanningTree.append(":".join([parent,str(t),child,str(0)]))
                
        # mark parent as visited, then repeat until Queue is empty
        visited.append(parent)
    

    return minSpanningTree

def TopologicalSort(PI):
    stack = []
    for k in PI.keys():
        a = k
        while a != None:
            # print(a,stack)
            if a in stack:
                stack.pop(stack.index(a))
            stack.append(a)
            child,_,_ = PI[a]
            a = child

        # print("topological sort: ", stack)
    return stack


def CreateSortedAdjList(PI):
    # print("flow topology:", self.topoSorted[::-1])
    newAdjList = {}
    for child, parent in PI.items():
        p,_,_ = parent
        c = child
        if p:
            if newAdjList.get(p) == None:
                newAdjList[p] = []
            newAdjList[p].append(c)

    return newAdjList


def ShortestBranch(network, src, distance, ordered):
    if network.get(src) == None:
        return distance
    else: 

        while network[src]: 
            nextSrc = network[src].pop(0)
            # print(src, nextSrc,distance+1)
            
            # for each child, go to the end; once at the end, return the length of the branch 'd'
            d = ShortestBranch(network, nextSrc, distance+1, ordered)
            
            # modify each node and add 'shortest length' 
            if ordered.get(src) == None:
                ordered[src] = []

        ordered[src].append((d - distance, nextSrc))
        # distances[nextSrc] = d - distance

    return d


def Optimize(ordered): 
    for key in ordered:
        ordered[key].sort()


def printInfo(self):      
    print("predecessor:\t\t",self.PI)
    print("topological sort:\t", self.topoSorted)
    print("complete adj list:\t", self.ordered)


#### POST PROCESS ALGORITHMS ####
def PostProcess(root, cellInfo, cellIndex):
        # getting end points
        # Format {"A":[(1,"B"),(2,"C")], "B":[(1,"D"),(2,"E")]}

        def updateChildren(key, parentIdx, cellInfo):
            if (cellInfo.get(key) != None):
                childrenList = cellInfo[key]
                newChildrenList = []

                # print(key, cellInfo)

                for pair in childrenList:
                    offset,child = pair
                    newChildrenList.append((offset+parentIdx,child))

                cellInfo[key] = newChildrenList

                offset,_ = max(newChildrenList)
                while childrenList:
                    childIdx, newChild = childrenList.pop(0)
                    updateChildren(newChild, offset, cellInfo)     
                

        def getEndPoints(key, endpoints, cellInfo):
            if cellInfo.get(key) != None:
                extent,_ = max(cellInfo[key])
                endpoints[key] = extent
               
                # print(key, extent)
                cpy = cellInfo[key].copy()
                while cpy:
                    row,child = cpy.pop(0)

                    if cellInfo.get(child) == None:
                        endpoints[child] = row

                    endpoints = getEndPoints(child, endpoints, cellInfo)
            
            return endpoints

        def unfoldAdjList(adjList):
            # Format {"A":[(1,"B"),(2,"C")], "B":[(3,"D"),(4,"E")]}
            # to  unfolded = [[A, B], [A, C], [B, D], [B, E]] 
            #  
            # then just do a simple: if cell in unfolded[row] {}

            unfoldedList = {}
            keys = adjList.keys()
            
            for key in keys:               
                for pair in adjList[key]:
                    row,child = pair
                    if unfoldedList.get(row) == None:
                        unfoldedList[row] = []
                    unfoldedList[row].append(key)
                    unfoldedList[row].append(child)
            
            return unfoldedList
        # print(max( [(1,"P"),(9,"d")] ) )
        
        # print("heap", cellInfo)
        updateChildren(root,0,cellInfo)
        # print("heap", cellInfo)

        endpoints = getEndPoints(root, {}, cellInfo)
        # print("endpoint", endpoints)
        unfolded = unfoldAdjList(cellInfo)
        # print("unfolded list", unfolded)

        return endpoints, unfolded


