import uF_networkAlgo


if __name__ == "__main__":
    test8 = {
        "adjList": [
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
        ],

        "nodes":["C"+str(i) for i in range(10)],
        "root":"C0"
        }

    uF_networkAlgo.algorithm(test8["root"], test8["nodes"], test8["adjList"])
    