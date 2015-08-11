# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 06:46:36 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from libraryManager.common import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *
from libraryManager.footprint import footprint

class libraryPowerSupplies(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("nicePowerSupplies")
        self.parts.append(partPinheader(cols, rows))
        
class partPinheader(part):
    """
    Pinheader part generator
    """
    def __init__(self, cols, rows, name=""):
        if not name:
            name = "PIN-%dx%d" % (cols, rows)
        super().__init__(name, "CON")
        if cols<3:
            self.symbols.append(symbolPinheader(cols, rows, name))
        else:
            for i in range(cols):
                self.symbols.append(symbolPinheader(1, rows, name, offset=i*rows))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintPinheader(cols, rows, density))

class symbolPinheader(symbolIC):
    """
    Pinheader symbol
    """
    def __init__(self, cols, rows, name, refDes="CON", showPinNames=False,\
        showPinNumbers=True, offset=0):
        pinsRight = [(['%d' % (row * cols + 2), row * cols + 2, pinType.passive] if cols>1 else None) for row in range(rows)]
        pinsLeft = [['%d' % (row * cols + 1), row * cols + offset + 1, pinType.passive] for row in range(rows)]
        super().__init__(name, pinsLeft, pinsRight, 400, refDes, showPinNames, showPinNumbers)