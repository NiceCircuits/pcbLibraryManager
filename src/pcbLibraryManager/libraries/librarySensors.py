# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:23:46 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *
from libraryManager.generateLibraries import generateLibraries
from libraries.libraryRLC import *

class librarySensors(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSensors")
        for v in ["V","H"]:
            self.parts.append(partThermistor(variant=v))

class partThermistor(part):
    """
    Thermistor part
    """
    def __init__(self, variant="V"):
        name="Thermistor_%s"%variant
        super().__init__(name, "Th")
        self.symbols.append(symbolThermistor(name, variant=variant))
        for size in ["0603", "0805"]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSmdChip(size + "_" + density, \
                    size = size, density = density))

class symbolThermistor(symbolR):
    """
    Thermistor symbol
    """
    def __init__(self, name, refDes="Th", variant="V", pinNumbers=[1,2]):
        super().__init__(name, refDes, pinNumbers=pinNumbers, variant=variant)
        points=[[80,-60],[-80,60],[-120,60]]
        if variant=="V":
            points=rotatePoints(points,90)
        self.primitives.append(symbolPolyline(defaults.symbolLineWidth,points))

if __name__ == "__main__":
    # generate libraries
    generateLibraries([librarySensors()])