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

class footprintEsp07(footprint):
    """
    ESP-07 WiFi module
    """
    def __init__(self, name, density, alternativeLibName):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        super().__init__(name, alternativeLibName,originMarkSize=defaults.originMarkSize)
        self.nameObject.position=[-12.5, 0]
        self.nameObject.rotation=270
        self.valueObject.position=[9,0]
        self.valueObject.rotation=270
        # pads
        for y in [-1, 1]:
            for x in range(8):
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=\
                [(7.0-2.0*x)*y-2.0, 8.0*y],dimensions=[1.2, 2], name=str(x+1 if y<0 else x+9)))
        # body
        self.primitives.append(pcbRectangle(pcbLayer.topAssembly,\
            defaults.documentationWidth, position=[0,0], dimensions=[22.0, 16.0]))
        # silk
        silkX = 11.2
        silkY = 8.2
        for x in [-1, 1]:
            self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
                silkX*x, silkY, silkX*x, -silkY))
            for y in [-1, 1]:
                self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
                    silkX*x, silkY*y, (silkX-3)*x-2, silkY*y))

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
        super().__init__("ESP-07")
        self.symbol = symbolEsp07("ESP-07")
        for density in ["L", "N", "M"]:
            self.footprints.append(footprintEsp07("ESP-07_" + density, \
            density = density, alternativeLibName = "niceModules"))

