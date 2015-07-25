# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 23:13:18 2015

@author: piotr at nicecircuits.com
"""

class footprintConnectorRasterTht(footprint):
    """
    Footprint generator for THT raster connetors. Generate only pins.
    First pin in bottom left corner. 
    """
    def __init__(self, name, alternativeLibName, cols, rows, pitch, padDimensions, 
        originMarkSize=0):
        super().__init__(name, alternativeLibName=alternativeLibName, originMarkSize=originMarkSize)
        #TODO: 
        x1 = pitch * (pinCount/4 - 0.5)
        for y in [-1, 1]:
            for x in range(int(pinCount/2)):
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=\
                    [(x1-pitch*x)*y+offset[0], padSpan/2*y+offset[1]],dimensions=padDimensions,\
                    name=str(int(x+1 if y<0 else x+pinCount/2+1)),rotation=0 if y<0 else 180))

class footprintConnectorRasterKeyedTht(footprintConnectorRasterTht):
    """
    """
    pass