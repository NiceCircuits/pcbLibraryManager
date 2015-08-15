# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:29:13 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.part import part
from libraryManager.symbol import symbol
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults
from footprints.footprintSmdDualRow import footprintSmdDualRow

class footprintEsp07(footprintSmdDualRow):
    """
    ESP-07 WiFi module
    """
    def __init__(self, name, density, alternativeLibName):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        # pads
        padSizes={"L":[1.1, 1.6], "N":[1.2, 2.0], "M":[1.3, 2.2]}
        padSpan={"L":15.6, "N":16.0, "M":16.2}
        super().__init__( name, alternativeLibName=alternativeLibName, pinCount=16, pitch=2,\
            padSpan=padSpan[density], padDimensions=padSizes[density],
            offset = [-2, 0], originMarkSize=defaults.originMarkSize)
        self.nameObject.position=[-12.5, 0]
        self.nameObject.rotation=270
        self.valueObject.position=[9,0]
        self.valueObject.rotation=270
        # body
        self.addSimple3Dbody([0,0,0], [22.0, 16.0, 1.0])
        self.addSimple3Dbody([-1.25,0,1], [15.3, 12.3, 2.5])
        self.addSimple3Dbody([9.5,-2,1], [2,9,1])
        # silk
        silkX = 11.2
        silkY = 8.2
        for x in [-1, 1]:
            self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
                silkX*x, silkY, silkX*x, -silkY))
            for y in [-1, 1]:
                self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
                    silkX*x, silkY*y, (silkX-3)*x-2, silkY*y))
        # TODO: courtyard

class symbolEsp07(symbol):
    """
    ESP-07 WiFi module
    """
    def __init__(self, name):
        super().__init__(name)

class partEsp07(part):
    """
    ESP-07 WiFi module 
    """
    def __init__(self):
        super().__init__("ESP-07", defaults.icRefDes)
        self.symbols.append(symbolEsp07("ESP-07"))
        for density in ["L", "N", "M"]:
            self.footprints.append(footprintEsp07("ESP-07_" + density, \
                density = density, alternativeLibName = "niceModules"))

