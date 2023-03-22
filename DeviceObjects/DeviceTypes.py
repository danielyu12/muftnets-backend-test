# types.py
# Purpose to translate cell topology expression into english
# Programmer: Muhammed Abdalla
# Oliveira Lab
# Copyright 2022

class Flow:
    def __init__(self) -> None:
        self.flowContents = {                        # the I/O of the channel flows
            "mediaIN": {                        # contents of what is following in (LATER WE ONLY CARE ABOUT OUTPUT)
                "cells":[],
                "molecules":[]
            },

            "mediaOUT": {                       # contents of what is following out
                "cells": [],
                "molecules": []
            }
        }

class Device:
    def __init__(self,cellJSON) -> None:

        self.deviceFields = {
            "num_species": 0,                   # number species (int)
            "cell_traps": [],                   # the cell names (str)
            "chamber_height": [],               # cell trap sizes (float: um)
            "num_signals": 0,                   # number communication signals (int)
            "signal_type": "",                  # type connection
            "contact_type": "",                 # type connection
            "direction": "",                    # type connection
            "output_filtering": False,          # output filtering (bool)                   
            "chamber_aspect_ratio": [],         # filter unit (MC, MCM, MFM, CF) (float: um)
            "filter_aspect_ratio": [],          # filter unit (CF only) (float: um)
            "in_flow": None                     # if there are contents flowing in this device
        }

        self.channels = []                           # flow channels

        
        #print("-"*100)
        for field,value in zip(cellJSON.keys(),cellJSON.values()):
            if field in self.deviceFields.keys():
                self.deviceFields[field] = value
                #print("[GENERATING FIELD]",field,":",value)
        #print("-"*100)
    
    def filter(self, flowContents):
        flowContents["mediaOUT"]["cells"] = []

    def gradient(self, G):
        pass
        # multiply # outputs by G
        # each output i, 0 thru G is (G-i)% of the input flow
        # gradient = []
        # outputCopy = self.channels[-1].copy()
        # outputCopy["mediaOUT"]["cells"]
        # self.channels[-1] = []
        # for i in range(G+1):
        #     temp = self.channels[-1].copy()
        #     temp = [(i*1.0)/G,outputCopy["mediaOUT"]["molecules"]]

    def getInput(self,channelNum):
        return self.channels[channelNum]["mediaIN"]

    def getOutput(self,channelNum):
        return self.channels[channelNum]["mediaOUT"]

class MC(Device):
    # assigns the user defined parameters offered for the MC unit
    def __init__(self, cellJSON) -> None:
        super().__init__(cellJSON)
        
        # figure out the flow for MC
        # in = out
        self.channels.append(Flow().flowContents)
        self.channels[0]["mediaIN"]["cells"] = self.deviceFields["cell_traps"].copy()
        self.channels[0]["mediaIN"]["cells"].extend(self.channels[0]["in_flow"]["cells"]) # take the external input
        self.channels[0]["mediaIN"]["molecules"].extend(self.channels[0]["in_flow"]["molecules"]) # take the external input

        self.channels[0]["mediaOUT"]["cells"].extend(self.channels[0]["mediaIN"]["cells"])
        self.channels[0]["mediaOUT"]["molecules"].extend(self.channels[0]["mediaIN"]["molecules"])

        if self.deviceFields["output_filtering"] == True:
            self.filter(self.channels[-1])

    def type(self):
        return "MC"

class MCM(Device):
    # assigns the user defined parameters offered for the MC unit
    def __init__(self, cellJSON) -> None:
        super().__init__(cellJSON)
        
        # figure out the flow for MCM
        # there are two flows: major and minor flow, or [0] and [1]
        self.channels.append(Flow().flowContents) # major flow
        self.channels.append(Flow().flowContents) # minor flow

        # major flow
        self.channels[0]["mediaIN"]["cells"].append(self.deviceFields["cell_traps"][0])
        self.channels[0]["mediaIN"]["cells"].extend(self.deviceFields["in_flow"]["cells"])
        self.channels[0]["mediaIN"]["molecules"].extend(self.deviceFields["in_flow"]["molecules"])

        self.channels[0]["mediaOUT"]["cells"].append(self.deviceFields["cell_traps"][0])
        self.channels[0]["mediaOUT"]["molecules"].append(self.deviceFields["cell_traps"][0])
        self.channels[0]["mediaOUT"]["cells"].extend(self.deviceFields["in_flow"]["cell"])
        self.channels[0]["mediaOUT"]["molecules"].extend(self.deviceFields["in_flow"]["molecules"])


        # minor flow
        self.channels[1]["mediaIN"]["cells"].append(self.deviceFields["cell_traps"][1])
        self.channels[1]["mediaOUT"]["cells"].append(self.deviceFields["cell_traps"][1])
        self.channels[1]["mediaOUT"]["molecules"].append(self.deviceFields["cell_traps"][1])
        self.channels[1]["mediaOUT"]["molecules"].extend(self.deviceFields["in_flow"]["molecules"]) # take the external input
        self.channels[1]["mediaOUT"]["molecules"].extend(self.channels[0]["mediaOUT"]["molecules"]) # take input molecules to output
    
        if self.deviceFields["output_filtering"] == True:
            self.filter(self.channels[-1])

    def type(self):
        return "MCM"
    

class MFM(Device):
    # assigns the user defined parameters offered for the MC unit
    def __init__(self, cellJSON) -> None:
        
        super().__init__(cellJSON)
        
        # figure out the flow for MFM
        # there are three flows, we only care about what goes into the first and comes out the last
        self.channels.append(Flow().flowContents) # input flow
        self.channels.append(Flow().flowContents) # connector flow
        self.channels.append(Flow().flowContents) # output flow

        # input flow
        self.channels[0]["mediaIN"]["cells"].append(self.deviceFields["cell_traps"][0])
        self.channels[0]["mediaIN"]["cells"].extend(self.deviceFields["in_flow"]["cells"])
        self.channels[0]["mediaIN"]["molecules"].extend(self.deviceFields["in_flow"]["molecules"])

        self.channels[0]["mediaOUT"]["cells"].append(self.deviceFields["cell_traps"][0])
        self.channels[0]["mediaOUT"]["molecules"].append(self.deviceFields["cell_traps"][0])
        self.channels[0]["mediaOUT"]["cells"].extend(self.deviceFields["in_flow"]["cells"])
        self.channels[0]["mediaOUT"]["molecules"].extend(self.deviceFields["in_flow"]["molecules"])

        # connector flow
        self.channels[1]["mediaIN"]["cells"].append(self.deviceFields["cell_traps"][1])
        self.channels[1]["mediaOUT"]["cells"].append(self.deviceFields["cell_traps"][1])
        self.channels[1]["mediaOUT"]["molecules"].append(self.deviceFields["cell_traps"][1])
        self.channels[1]["mediaOUT"]["molecules"].extend(self.channels[0]["mediaOUT"]["molecules"])

        # output flow 
        # no cell input/output, only molecules output
        self.channels[2]["mediaOUT"]["molecules"].extend(self.channels[1]["mediaOUT"]["molecules"])

        if self.deviceFields["output_filtering"] == True:
            self.filter(self.channels[-1])

    def type(self):
        return "MFM"