'''
refer to muhammed slides powerpoint
a bunch of if statements

Decision tree

1) are there 2+ cells
2) comm signals (short, long)
3) directionality (serial, non-serial)
4) Serial or non-serial
    serial
        contact:
            output signal filter:
                Yes: Solution -> CF with var(H)
                No: Solution -> serial-MC with var(H)
        No-contact:
            diff heights:
                comm. type:
                    short: DEFAULT SOLUTION -> MCM
                        Concentration Tuning: Conflict
                        Time Tuning: var(AR)
                        filter
                    long:
    non-serial: 
        contact:
            diff heights:
            Yes: Conflict
            No: Solution -> MC



'''

import DeviceObjects.DeviceTypes as DeviceTypes

def checkTwoCell(cell_traps):
    # are there exactly 2 cells
    # a default device consists of two cells
        # multiple primitives
    # a network consists of +2 default devices
    if len(cell_traps) == 2:
        return True
    else:
        return False

def selectDevice(cellJSON):
    
    isDifferentHeights = False
    prev = cellJSON["chamber_height"][0]
    for h in cellJSON["chamber_height"]:
        if h != prev:
            isDifferentHeights = True
            break
        prev = h

    outputFiltering = cellJSON["output_filtering"] == True

    tuning = {
        "concentration": False,
        "time": False
    }
    if outputFiltering:
        print("OUTPUT FILTERING")
    if tuning["concentration"]:
        print("GRADIENT OUTPUT")
    #serial (unidirectional)
    if cellJSON["direction"] == "SERIAL":
        if cellJSON["contact_type"] == "CONTACT":
            solution = ["MC","type 1 (default)","src:C:dest"]
            if isDifferentHeights:
                solution = ["MC","type 2 (cascading)","src:CV:dest"]
                print("Selected: ", solution)
            return solution

        elif cellJSON["contact_type"] == "CONTACTLESS":

            if cellJSON["signal_type"] == "LONG":
                specimens = checkTwoCell(cellJSON["cell_traps"])
                if not specimens:
                    return "Error: more than two cells"

                solution = ["MFM", "type 1 (default)","src:L:dest"]
                if isDifferentHeights:
                    solution = ["MFM","type 2 (var(H))","src:L:dest"]
                elif tuning["time"]:
                    solution = ["MFM","type 3 (var(AR)","src:LT:dest"]
                print("Selected: ", solution)
                return solution

            elif cellJSON["signal_type"] == "SHORT":

                specimens = checkTwoCell(cellJSON["cell_traps"])
                if not specimens:
                    return "Error: more than two cells"

                solution = ["MCM","type 1 (default)","src:S:dest"]
                if isDifferentHeights:
                    solution = ["MCM","type 2 (var(H))","A--B"]
                if tuning["time"]:
                    solution = ["MCM","type 3 (var(AR))","A--B"]
                print("Selected: ", solution)
                return solution
            else:
                return None
        else:
            return None
    #Non-Serial (bidirectional)
    elif cellJSON["direction"] == "NON-SERIAL":
        if cellJSON["contact_type"] == "CONTACT" and not isDifferentHeights:
            solution = ["MC","type 1 (default)","src:dest"]
            print("Selected: ", solution)
            return solution
        else:
            return None 

    return None

def createDevice(deviceType, cellJSON):
    if deviceType == "MC":
        return DeviceTypes.MC(cellJSON)
    elif deviceType == "MCM":
        return DeviceTypes.MCM(cellJSON)
    elif deviceType == "MFM": 
        return DeviceTypes.MFM(cellJSON)