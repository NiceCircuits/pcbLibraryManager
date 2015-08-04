# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 22:17:59 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *

class libraryPinheaders(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("nicePinheaders")
        for cols in [1,2]:
            for rows in range(1,21):
                self.parts.append(partPinheader(cols, rows))
        
class partPinheader(part):
    """
    Pinheader part generator
    """
    def __init__(self, cols, rows, name=""):
        if not name:
            name = "PIN-%dx%d" % (cols, rows)
        super().__init__(name, "CON")
        self.symbols.append(symbolPinheader(cols, rows, name))

class symbolPinheader(symbolIC):
    """
    Pinheader symbol
    """
    def __init__(self, cols, rows, name, refDes="CON", showPinNames=False, showPinNumbers=True):
        pinsRight = [(['%d' % (row * cols + 2), row * cols + 1, pinType.passive] if cols>1 else None) for row in range(rows)]
        pinsLeft = [['%d' % (row * cols + 1), row * cols + 1, pinType.passive] for row in range(rows)]
        super().__init__(name, pinsLeft, pinsRight, 400, refDes, showPinNames, showPinNumbers)
