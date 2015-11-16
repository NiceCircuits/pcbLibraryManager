# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 06:44:10 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *
from footprints.footprintSmdDualRow import footprintSoic
from footprints.footprintDip import footprintDip

class libraryLogic(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceLogic")
        for name in ["74HC4060D", "74HCT4060D", "CD4060BCM", "74HC4060N",\
        "74HCT4060N", "CD4060BCN"]:
            self.parts.append(partCD4060(name))
        
class partCD4060(part):
    """
    CD4060 part
    """
    def __init__(self, name="CD4060BCM"):
        """
        :param name: Name of part. Used to connect proper footprint too.
        Available: 74HC4060D, 74HCT4060D, CD4060BCM, 74HC4060DB, 74HCT4060DB
        """
        super().__init__(name, "U")
        self.symbols.append(symbolCD4060("CD4060"))
        for density in ["N", "L", "M"]:
            if name in ["74HC4060D", "74HCT4060D", "CD4060BCM"]:
                self.footprints.append(footprintSoic(16, density=density))
            if name in ["74HC4060N", "74HCT4060N", "CD4060BCN"]:
                self.footprints.append(footprintDip(16, density=density))

class symbolCD4060(symbolIC):
    """
    CD4060 symbol
    """
    def __init__(self, name, refDes="U", showPinNames=True, showPinNumbers=True):
        pinsLeft = [
['VCC', 16, pinType.pwrIn],
None,
None,
['GND', 8, pinType.pwrIn],
None,
['RESET', 12, pinType.input],
None,
['RS',  11, pinType.input],
['RTC', 10, pinType.output],
['CTC', 9, pinType.output],
        ]
        pinsRight = [
['Q3',  7,  pinType.output],
['Q4',  5,  pinType.output],
['Q5',  4,  pinType.output],
['Q6',  6,  pinType.output],
['Q7',  14, pinType.output],
['Q8',  13, pinType.output],
['Q9',  15, pinType.output],
['Q11', 1,  pinType.output],
['Q12', 2,  pinType.output],
['Q13', 3,  pinType.output]
        ]
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=1000)
