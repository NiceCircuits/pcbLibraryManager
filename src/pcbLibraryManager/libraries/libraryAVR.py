# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 18:04:03 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from math import ceil

class libraryAVR(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceAVR")
        self.parts.append(partAtmega48("ATmega48", "AU"))
        self.parts.append(partAtmega48("ATmega328"))
        
class partAtmega48(part):
    """
    Atmega48/88/168/328/P/A part
    """
    def __init__(self, name="ATmega48", version="AU"):
        super().__init__(name, "U")
        self.symbols.append(symbolR("R"))
        for size in ["0402", "0603", "0805", "1206", "1210", "2010", "2512"]:
            for density in ["L", "N", "M"]:
                self.footprints.append(footprintSmdChip(size + "_" + density, \
                    size = size, density = density, alternativeLibName = "niceRLC"))

class symbolAtmega48(symbol):
    """
    Atmega48/88/168/328/P/A symbol
    """
    def __init__(self, name, version, refDes="U", showPinNames=True, showPinNumbers=True):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in range(2):
            self.pins.append(symbolPin(i+1, pinNumbers[i], [300 if i else -300,0],\
                100, pinType.passive, rotation=180 if i else 0))
            self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
                position=[0,0], dimensions=[400, 150]))
        self.nameObject.position=[0, 150]
        self.valueObject.position=[0, 0]
        self.valueObject.height = defaults.symbolSmallTextHeight