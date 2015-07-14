# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:06:39 2015

@author: piotr at nicecircuits.com
"""

class footprint:
    """
    """
    layerTopN=0
    layerBottomN=7    
    
    def __init__(self, name, alternativeLibName = ""):
        self.name = name
        self.alternativeLibName = alternativeLibName
        
        ##############
        #initialize empty list for storing primitives
        # generate (layerBottomN+1) empty lists for copper layers (excluding pads)
        self.copperLayers = [[] for x in range(self.layerBottomN + 1)]
        # top and bottom pad layers
        self.padLayers = [[], []]
        # top and bottom silkscreen layers
        self.silkLayers = [[], []]
        # top and bottom solder mask layers
        self.maskLayers = [[], []]
        # top and bottom Assembly drawings layers
        self.assemblyLayers = [[], []]
        # top and bottom solder paste layers
        self.pasteLayers = [[], []]
        # top and bottom glue layers
        self.glueLayers = [[], []]
        # top and bottom placement courtyard layers
        self.courtyardLayers = [[], []]

if __name__ == "__main__":
    print(sot23(None,None,3))