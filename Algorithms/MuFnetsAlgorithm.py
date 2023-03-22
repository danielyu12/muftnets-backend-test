# Translator.py
# Purpose to translate cell topology expression into english
# Programmer: Muhammed Abdalla
# Oliveira Lab
# Copyright 2022

# code to translate from


# symbol, description, structure (from primitives)
# these are all contactless devices
import heapq


monolayer_chamber_syntax = {
    ":": ["short range contact based", "MC"],
    "-": ["short range serial", "MCM"],
    "=": ["long range serial", "MFM>MFM"],
    "#": ["gradient (signal splitter)", "SS"],
    "|": ["Particle Filter", "PF"],
    "S": ["source inlet"],
}

replacements = {
    "->": "-",
    "--": "=",
    ">>": ">"
}


def replacedel(txt):
    for k in replacements:
        if k in txt:
            txt = txt.replace(k, replacements.get(k))
    return txt

"""
# Example:
# A->B--C-D
# description:
# signals A serializes into the cycle of B & C and communicates with D

#example while making the algorithm
A -> (B-C)

"""

def translator():
    delimiters = monolayer_chamber_syntax.keys()
    line = ""
    cell_configs = []

    while True:
        line = input("enter an expression: ")

        if line == "Q":
            break

        print("expected expression:", line)
        line = replacedel(line)
        print("computer expression:", line)

        for i, char in enumerate(line):
            if char in delimiters:
                print(line[i - 1], monolayer_chamber_syntax[char][0], line[i + 1], "devices:",
                    monolayer_chamber_syntax[char][1])

"""
Input:      a list of connections (string); adjecency list
Output:     a list of devices (objects) and corrected routing

Input format:
A:C:B is A:B
A:S:B is A-B
A:L:B is A=B

B:S:A, B:S:C are two independent devices (one to many)
A:S:B, C:S:B are two independent devices (many to one)
the B channel has two B traps for the MCM
1) use split(':')
2) find all pairs with split(':')[1] == C or S
    2.1) collect all contact based into one unit
    2.2) check for overlapping in S connections
"""
 
class Algorithm:
    parsedAdjList = {}
    cellpairs = {}
    subnetworks = {}
    devices = {}
    priority = []
    PI = {}
    topoSorted = {}
    ordered = {}
    valveStatus = {}
    distances = {}

    def __init__(self, adjList) -> None:
        self.resetVars()
        self.algorithm(adjList)

    def resetVars(self):
        self.parsedAdjList = {}
        self.cellpairs = {}
        self.subnetworks = {}
        self.devices = {}
        self.priority = []
        self.PI = {}
        self.topoSorted = {}
        self.ordered = {}
        self.valveStatus = {}
        self.distances = {}

    def algorithm(self, adjList):
        self.resetVars()

        # print("adjList",adjList)
        if adjList == None:
            return None

        # 1 Dictionary population
        for pair in adjList:
            temp = pair.split(":")
            src = temp[0]
            t = temp[1]
            dest = temp[2] 
            isContiguous = int(temp[3])  # subnetwork ID

            numType = None
            if t == "C":
                numType = 0
            elif t == "S":
                numType = 1
            elif t == "L":
                numType = 2

            # represent subnetwork as a hashtable with chaining
            # else individual pairs just enter
            if isContiguous > 0:
                if self.subnetworks.get(isContiguous) == None:
                    self.subnetworks[isContiguous] = {}
                if self.subnetworks.get(isContiguous).get(src) == None:
                    self.subnetworks[isContiguous][src] = []

                self.subnetworks[isContiguous][src].append((dest,t))
            else:
                if self.cellpairs.get(src) == None:
                    self.cellpairs[src] = []
                self.cellpairs[src].append((dest,t))
            
            net = "Subnetwork "
            if isContiguous == 0:
                net = "Isolated Cell Pair "

            if self.devices.get(net+temp[3]) == None:
                self.devices[net+temp[3]] = []

            device = None
            if t == "C":
                device = "MC("+src+","+dest+")"
            elif t == "S":
                device = "MCM("+src+","+dest+")"
            elif t == "L":
                device = "MFM("+src+","+dest+")"
            self.devices[net+temp[3]].append(device)

            self.priority.append((numType,src,dest))

            if self.PI.get(src) == None:
                self.PI[src] = (None,None,0)
            self.PI[dest] = (src,t,0)

        heapq.heapify(self.priority)


        # print("predecessor:\t\t",self.PI)

        # 2 check for cycles
        if self.cycleCheck():
            print("Cycle Detected")
            return "cycle"
            
        # 3 Run the main algorithms
        self.topoSorted = self.topologicalSort()
        self.valveStatus = {n:1  for n in self.topoSorted}
        self.parsedAdjList = self.createAdjList()

        temp_topoSorted = self.topoSorted.copy()
        while temp_topoSorted:
            temp = temp_topoSorted.pop()
            if self.ordered.get(temp) == None:
                self.DFS_VISIT(self.parsedAdjList, temp,0) 


        self.optimize()
        self.printInfo()

        # 4 display the grid layout
        # if self.printMesh():
        #     # print("Device Error")
        #     return "device"

        return None

    def cycleCheck(self):
        def DFS(stack, PI, key):
            if key == None:
                return False
            elif key in stack:
                # checker to validate cycles
                stack.append(key)
                # print(stack)
                return True
            else:
                stack.append(key)
                child,_,_ = PI[key]
                return DFS(stack,PI,child)

        for k in self.PI.keys():
            child,_,_ = self.PI[k]
            if DFS([], self.PI.copy(),child):
                return True


    def topologicalSort(self):
        stack = []
        for k in self.PI.keys():
            a = k
            while a != None:
                # print(a,stack)
                if a in stack:
                    stack.pop(stack.index(a))
                stack.append(a)
                child,_,_ = self.PI[a]
                a = child

            # print("topological sort: ", stack)
        return stack


    def createAdjList(self):
        # print("flow topology:", self.topoSorted[::-1])
        newAdjList = {}
        for child, parent in self.PI.items():
            p,_,_ = parent
            c = child
            if p:
                if newAdjList.get(p) == None:
                    newAdjList[p] = []
                newAdjList[p].append(c)

        return newAdjList

    
    def DFS_VISIT(self,network,src,distance):
        if network.get(src) == None:
            return distance
        else: 

            while network[src]: 
                nextSrc = network[src].pop(0)
                # print(src, nextSrc,distance+1)
                
                # for each child, go to the end; once at the end, return the length of the branch 'd'
                d = self.DFS_VISIT(network, nextSrc, distance+1)
                
                # modify each node and add 'shortest length' 
                if self.ordered.get(src) == None:
                    self.ordered[src] = []

            self.ordered[src].append((d - distance, nextSrc))
            self.distances[nextSrc] = d - distance

        return d


    def printInfo(self):      
        # print()
        # for k in self.cellpairs.keys():
        #     print("isolated cell pair ", k, self.cellpairs[k])

        # print()
        # for k in self.devices.keys():
        #     print("devices: ", k, self.devices[k])

        print("predecessor:\t\t",self.PI)
        print("topological sort:\t", self.topoSorted)
        print("optimized adj list:\t", self.ordered)
        # while priority:
        #     print(heapq.heappop(priority))


    def optimize(self): 
        for key in self.ordered:
            self.ordered[key].sort()
            # print("|\t",key,"\tpre-optimize:\t",preOrd[key],"|\tpost-optimize:\t",self.ordered[key],"\t|")

    def printMesh(self):
        rev = []

        for cell in self.topoSorted:
            rev.insert(0,cell)
        
        indices = {c:i for i,c in enumerate(rev)}

        for child, p in self.PI.items():
            parent,t,_ = p
            # if t ==  'C':
            #     if abs(indices[parent] - indices[child]) > 0:
            #         print("Contact Based Comm: cannot span between flows")
            #         return True
            # elif t ==  's':
            #     if abs(indices[parent] - indices[child]) > 1:
            #         print("Short Based Comm: cannot span over 2 flows")
            #         return True

        # print("Indices ",indices)

        line = ""
        spacer = "\t"  

        for cell in rev:
            line = line + spacer + cell

        line = line + '\n'

        for row in range(10):
            lanes = 0

            for i,cell in enumerate(rev):

                p,t,r = self.PI[cell]

                if self.distances:
                    pass

                if self.valveStatus[cell] == 1:
                    line = line + spacer + "||"
                    lanes = 0
                else:
                    lanes = lanes + 1

            line = line + "\n"

        print(line)

if __name__ == "__main__":
    pass