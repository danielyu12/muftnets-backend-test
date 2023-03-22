import random
import math
import Algorithms.UserSelection as cellJSONSelector
import Algorithms.MuFnetsAlgorithm as NetworksAlgorithm

cellJSON = {
    "num_species": "INT", #USE
    "cell_traps":  "INT ARRAY", #USE
    "chamber_height": "INT ARRAY",
    "num_signals": "INT",
    "signal_type": ["SHORT","LONG"], #USE
    "contact_type": ["CONTACT","CONTACTLESS"], #USE
    "direction": ["SERIAL","NON-SERIAL"], #USE
    "output_filtering": "BOOLEAN", #USE
    "output_gradient": "BOOLEAN",                                     
    "chamber_aspect_ratio": "INT ARRAY",
    "filter_aspect_ratio": "INT ARRAY",
    "in_flow": "FLOW OBJECT", #USE
    "ID":"INT"
}



def createTopology(N):
    src = None
    dest = None
    typeComm = ["C","S","L"]
    seqNO = 1

    topology = []
    nodes = []

    for _ in range(N):
        edges = []
        src = ""
        dest = ""
        t = 0

        while src == dest and (src,dest) not in edges and (dest,src) not in edges:
            src = "C" + str(math.floor(random.random() * N))
            dest = "C" + str(math.floor(random.random() * N))
            t = typeComm[math.floor(random.random() * 3)]
        
        nodes.append(src)
        nodes.append(dest)
        edges.append((src,dest))

        if random.random() * 100 > 25:
            if random.random() * 100 > 95:
                seqNO = seqNO + 1   
            topology.append(src+":"+t+":"+dest+":"+str(seqNO))
        else:
            topology.append(src+":"+t+":"+dest+":"+str(0))

    def createMST(topology):
        # print("topology",topology)
        adjList = {n:[] for n in nodes}
        # print(adjList)
        root = None


        for edge in topology:
            temp = edge.split(":")
            src = temp[0]
            t = temp[1]
            dest = temp[2] 
            isContiguous = int(temp[3])

            if root == None:
                root = src

            adjList[src].append((dest,t,isContiguous))


        # Run BFS
        Q = [root]
        minSpanningTree = []
        visited = []
        edges = []

        # while the Queue is not empty
        while Q:    
            # pop the first element                        
            parent = Q.pop(0)
            children = adjList[parent]
            
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
            # print("visted",visited)
            # print("Q",Q)
        

        return minSpanningTree

    minSpanningTree = createMST(topology)
    # print("MST",minSpanningTree)  

    return minSpanningTree


Subnetwork = {'C8': [('C0', 'L'), ('C2', 'L')], 'C6': [('C8', 'L'), ('C1', 'L')], 'C2': [('C0', 'C'), ('C4', 'C')], 'C5': [('C1', 'C'), ('C9', 'L')], 'C9': [('C7', 'C')]}

test1A = [
    "A:S:B:0",
    "A:L:C:0",
]

test1B = [
    "A:L:B:1",
    "A:L:C:0",
    "B:L:C:1",
]

test1C = [
    "A:L:B:1",
    "B:L:C:1",
    "C:L:D:1",
    "A:S:D:2",
    "D:L:E:2",
]

# MCM and serial MFM
test2 = [
    "A:S:B:0",
    "B:L:C:0",
    "C:L:D:1",
]

# isolcated + parallel-MFM
test3B = [
    "A:S:B:0",
    ##
    "A:L:B:1",
    "B:L:C:1",
    "D:L:E:1",
    "E:L:F:1",
    "F:L:G:1",
    "C:L:D:1",
    ##
    "A:L:C:2",
    "C:L:E:2",
    "E:L:G:2",
]

# unspecifed B lanes
test6A = [
    "A:S:B:1",
    "A:L:C:2",
    "C:S:D:2",
    "D:L:B:2",
    "D:L:H:2",
    "H:C:E:2",
    "E:C:G:2",
    "D:L:F:3"
]

# specifed B lanes; different strains of same species
test6B = [
    "A:S:B1:1",
    "A:L:C:2",
    "C:S:D:2",
    "D:L:B2:2",
    "D:L:H:2",
    "H:C:E:2",
    "E:C:G:2",
    "D:L:F:3"
]

test7 = [
    "A:C:B:1",
    "A:L:C:1",
    "B:L:C:1",
    "C:L:D:1",
    "D:S:E:1",
    "D:S:F:1",
    "E:S:F:1",
]

error_self = [
    "C8:L:C0:1",
    "C1:L:C6:0",
    "C9:L:C9:1",
    "C2:S:C7:0",
    "C9:S:C0:1",
]

error_cycle = [
    "C7:S:C6:0",
    "C3:S:C5:1",
    "C7:C:C9:0",
    "C3:S:C1:1",
    "C9:L:C7:1",
]

test8 = [
    "C0:S:C10:1",
    "C8:S:C5:1",
    "C8:S:C4:2",
    "C0:S:C6:2",
    "C10:L:C6:2",
    "C1:S:C3:2",
    "C2:S:C10:2",
    "C2:L:C3:3",
    "C1:L:C6:3",
    "C5:S:C9:4",
    "C3:L:C6:4",
    "C10:L:C4:4",
    "C10:C:C4:4",
    "C4:L:C7:0",
    "C0:C:C8:0",
    ]

test2Parents = [
    "A:S:C:1",
    "B:S:C:1"
]

testProblem1 = [
    "1:L:2:1",
    "2:L:3:1",
    "3:L:4:1",
    "1:L:3:2",
    "1:L:2:3"
]

testProblem2 = [
    "1:L:2:1",
    "2:L:3:1",
    "3:L:4:1",
    "1:L:5:2",
    "2:L:7:3",
    "3:L:6:2",
]

testSlides = [
    "A:L:C:0",
    "C:L:D:0",
    "D:C:F:0",
    "F:L:E:0",
    "D:L:H:0",
    "H:L:E:0",
    "E:L:G:0",
    "D:L:B:0",
]

testTree = [
    "D:L:G:0",
    "G:L:H:0",
    "A:L:B:0",
    "B:L:C:0",
    "D:L:F:0",
    "C:L:E:0",
    "B:L:D:0",
]

if __name__ == "__main__":
    # algorithm(test1A)
    # algorithm(test1B)
    # algorithm(test1C)
    # algorithm(test2)
    # algorithm(test3B)
    # algorithm(test6)

    # d = NetworksAlgorithm.algorithm(test6A)
    # l = ["MC(A,B)","MFM(AB,C)","MFM(C,D)","MFM(D,F)","MFM(F,E)"]

    # print("Brute Force Output:")
    # for i in l:
    #     print(i)

    # print("subnetwork 1: [" + ",".join(l)+"]")


    def bulkTest():
        A = NetworksAlgorithm.Algorithm(None)
        m = ""
        for cells in range(5,100,1):   # cells 10 thru 100
            for i in range(20):     # 20 samples per cell size  
                d = createTopology(cells) 
                val = A.algorithm(d)

                while val is not None:
                    # Log the error
                    m = m + ",".join([str(cells),str(i+1),val]) + "\n"
                    
                    d = createTopology(cells) 
                    val = A.algorithm(d)

                for e in d:
                    print("STEP: " , cells, e) 
        print(m)
    

    d = createTopology(20) 
    for e in d:
        print(e)

    A = NetworksAlgorithm.Algorithm(testSlides)

