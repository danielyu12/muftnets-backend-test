"""
This algorithm is to figure out the terminus of the valves

{A:[(1,B),(2,C)]} ==

A       B       C    
||      ||      ||
OO  ==  OO      ||

||      XX      ||
OO  ==  ==  ==  OO

||              ||
XX              XX

Each row consists of:
1) adding
2) detail
    A) Opening (connecting to)
    B) closing port


"""
import heapq

# Need: Length of columns, column spacing, row spacing
def createMesh(cellInfo, cellIndex, colSpace, rowSpace):
    # return endpoints, meshAdj List
    # tuple(int, string) endpoints
    # array[]

    root = cellIndex[0]
    def preprocess():
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
        
        print("0", cellInfo)
        updateChildren(root,0,cellInfo)
        print("0", cellInfo)

        endpoints = getEndPoints(root, {}, cellInfo)
        print("endpoint", endpoints)
        unfolded = unfoldAdjList(cellInfo)
        print("unfolded list", unfolded)

        return endpoints, unfolded

    endpoints, unfolded = preprocess()

    title = ""
    padding = ""


    for cell in cellIndex:
        title = title + cell + "  "*colSpace
        padding = padding + "|" + "  "*colSpace

    mesh = title
    for _ in range(rowSpace+1):
        mesh = mesh + "\n" + padding

    # for each row
    for row in range(max(unfolded.keys())):
        lineInfo = ""
        # go thru the cell in order
        index = 0
        while index < len(cellIndex):
            cell = cellIndex[index]
            if cell in unfolded.get(row+1):
                lineInfo = lineInfo + "O" + \
                    "==" * colSpace * (1-unfolded.get(row+1).index(cell)) + \
                    "  " * colSpace * (unfolded.get(row+1).index(cell))

                # print("parent "+cell+" in row: "+str(row))
            else:
                # print(cell, row)
                if cell != -1:
                    if endpoints[cell] == row:
                        cellIndex[index] = -1
                        # print("closed", cell)
                    else:
                        lineInfo = lineInfo + "|" + "  "*colSpace 
                
                if cellIndex[index] == -1:
                    lineInfo = lineInfo + " " + "=="*colSpace     

            index = index + 1      

        mesh = mesh + "\n" + lineInfo
    # print(mesh)

createMesh({"A":[(1,"B"),(2,"C")], "B":[(1,"D"),(2,"E")]},["A", "B", "C", "D", "E"],2,1)      