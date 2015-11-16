# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 22:29:32 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from footprints.footprintSmdDualRow import footprintSoic
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *

class libraryCommunicationIC(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceCommunicationIC")
        self.parts.append(partCH340G())
        
class partCH340G(part):
    """
    CH340G part
    """
    def __init__(self, name="CH340G"):
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolCH340G(name))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintSoic(16, density=density))

class symbolCH340G(symbolIC):
    """
    CH340G symbol
    """
    def __init__(self, name, refDes=defaults.icRefDes, showPinNames=True,
    showPinNumbers=True):
        pinsRight = [
['VCC', 16, pinType.pwrIn],
['RS232', 15, pinType.input],
['RTS', 14, pinType.output],
['DTR', 13, pinType.output],
['DCD', 12, pinType.input],
['RI', 11, pinType.input],
['DSR', 10, pinType.input],
['CTS', 9, pinType.input]
        ]
        pinsLeft = [
['GND', 1, pinType.pwrIn],
['TxD', 2, pinType.output],
['RxD', 3, pinType.input],
['3V', 4, pinType.pwrOut],
['D+', 5, pinType.IO],
['D-', 6, pinType.IO],
['XI', 7, pinType.input],
['XO', 8, pinType.output]
        ]
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=1000)
