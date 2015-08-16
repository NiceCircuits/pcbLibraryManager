# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 16:13:24 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *
from libraryManager.defaults import defaults

class symbolR(symbol):
    """Resistor symbol
    """
    def __init__(self, name, refDes="R", showPinNames=False, showPinNumbers=False, pinNumbers=[1,2]):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in range(2):
            self.pins.append(symbolPin(i+1, pinNumbers[i], [200 if i else -200,0],\
                100, pinType.passive, rotation=180 if i else 0))
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
            position=[0,0], dimensions=[200, 80]))
        self.nameObject.position=[0, 80]
        self.valueObject.position=[0, 0]
        self.valueObject.height = defaults.symbolSmallTextHeight

class symbolC(symbol):
    """Capacitor symbol
    """
    def __init__(self, name, refDes="C", showPinNames=False, showPinNumbers=False, pinNumbers=[1,2]):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in range(2):
            self.pins.append(symbolPin(i+1, pinNumbers[i], [0, -100 if i else 100],\
                70, pinType.passive, rotation=90 if i else 270))
            self.primitives.append(symbolLine(defaults.symbolThickLineWidth,\
                -80, 30 if i else -30, 80, 30 if i else -30))
        self.nameObject.position=[20, 100]
        self.nameObject.align=textAlign.centerLeft
        self.valueObject.position=[20, -100]
        self.valueObject.align=textAlign.centerLeft
