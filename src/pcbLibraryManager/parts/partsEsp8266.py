# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:29:13 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.part import part
from libraryManager.symbol import symbol
from libraryManager.footprintPrimitive import *

class footprintEsp07(footprint):
    """
    ESP-07 WiFi module
    """
    def __init__(self, name, density, alternativeLibName):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        super().__init__(name, alternativeLibName)
        self.primitives.append(pcbLine(pcbLayer.topSilk, 0.15, -10, -10, -10, 10))

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

