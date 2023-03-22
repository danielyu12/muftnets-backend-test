import Algorithms.UserSelection as UserSelection
import DeviceObjects.DeviceTypes as DeviceObjects 

if __name__ == "__main__":
    def test1():
        deviceList = []

        cellJSON1 = {
            "num_species": 2,
            "cell_traps": ["A", "B"],
            "chamber_height": [0.75,0.75],
            "num_signals": 3,
            "signal_type": "LONG",   
            "contact_type": "CONTACTLESS",
            "direction": "SERIAL",
            "output_filtering": False, 
            "output_gradient": False,                                     
            "chamber_aspect_ratio": [2.5, 50],
            "filter_aspect_ratio": [50,50],
            "in_flow": DeviceObjects.Flow().flowContents["mediaOUT"]
        }

        cellJSON2 = {
            "num_species": 2,
            "cell_traps": ["B", "C"],
            "chamber_height": [0.75,0.75],
            "num_signals": 3,
            "signal_type": "LONG",   
            "contact_type": "CONTACTLESS",
            "direction": "SERIAL",
            "output_filtering": False, 
            "output_gradient": False,                                     
            "chamber_aspect_ratio": [2.5, 50],
            "filter_aspect_ratio": [50,50],
            "in_flow": None
        }

        print("-"*100)

        ## A LONG B (MFM)
        selection1 = UserSelection.selectDevice(cellJSON1)
        print("Device 1 chosen: ",selection1)
        device1 = UserSelection.createDevice(selection1[0],cellJSON1)
        print(device1)
        print("OUTPUT 1: ", device1.getOutput(-1))

        ## Algorithm of creating outputs
        ## take the output of device 1, and put it into the input of device two
        cellJSON2["in_flow"] = device1.getOutput(-1)
        print("-"*100)

        ## B LONG C (MFM)
        selection2 = UserSelection.selectDevice(cellJSON2)
        print("Device 2 chosen: ",selection2)
        device2 = UserSelection.createDevice(selection2[0],cellJSON2)
        print(device2)
        print("OUTPUT 2: ", device2.getOutput(-1))

    ## A->B->C

###########################################################################################

import random
import math
import Algorithms.UserSelection as cellJSONSelector
# import Algorithms.MuFnetsAlgorithm as NetworksAlgorithm


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


def createRandomDevice():
    name = 0
    seqNO = 1

    deviceJSON = cellJSON.copy()
    deviceJSON["num_species"] = math.floor(random.random() * 10)
    deviceJSON["cell_traps"] = ["cell"+str(name),"cell"+str(name+1)]
    name = name + 2

    deviceJSON["signal_type"] = deviceJSON["signal_type"][math.floor(random.random() * 2)]
    deviceJSON["contact_type"] = deviceJSON["contact_type"][math.floor(random.random() * 2)]
    deviceJSON["direction"] = deviceJSON["direction"][math.floor(random.random() * 2)]
    deviceJSON["output_filtering"] = True if math.floor(random.random() * 2) > 1 else False
    deviceJSON["output_gradient"] = True if math.floor(random.random() * 2) > 1 else False
    deviceJSON["in_flow"] = None

    if math.floor(random.random() * 10) > 9:
        if math.floor(random.random() * 10) > 8:
            seqNO = seqNO + 1
        deviceJSON["ID"] = seqNO
    else:
      deviceJSON["ID"] = 0

    
    # select the proper device
    selection = cellJSONSelector.selectDevice(deviceJSON)

    # 
    device = cellJSONSelector.createDevice(selection,deviceJSON)
    print(device)


createRandomDevice()