# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:17:33 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from footprints.footprintSmdDualRow import footprintSmdDualRow
from libraryManager.part import part
from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults

class librarySwitches(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSwitches")
        for h in [4.3, 5, 7, 9.5, 13, 19]:
            self.parts.append(partMicroswitchSmt(h))

class partMicroswitchSmt(part):
    """
    Default SMT microswitch
    """
    def __init__(self, height):
        name = "MicroswitchSmt-%1.1f" % height
        super().__init__(name, defaults.switchRefDes)
        self.symbols.append(symbolButton())
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintMicroswitchSmt(density, height))

class symbolButton(symbol):
    """Button symbol
    """
    def __init__(self, name="button", refDes=defaults.switchRefDes, showPinNames=False,\
    showPinNumbers=False, pinNumbers=[1,2]):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in range(2):
            self.pins.append(symbolPin(i+1, pinNumbers[i], [200 if i else -200,0],\
                100, pinType.passive, rotation=180 if i else 0))
            self.primitives.append(symbolCircle(defaults.symbolLineWidth,\
                [75 if i else -75, 0], 25))
        self.primitives.append(symbolLine(defaults.symbolThickLineWidth,\
            -100, 50, 100, 50))
        self.primitives.append(symbolRectangle(0, -25, 50, 25, 75,\
            filled=fillType.foreground))
        self.nameObject.position=[0, 120]
        self.valueObject.position=[0, -80]

class footprintMicroswitchSmt(footprintSmdDualRow):
    """Default SMT microswitch
    """
    def __init__(self, density, height=4.3, name="", alternativeLibName="niceSwitches"):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            name="MicroswitchSmd-%1.1f_%s" % (height, density)
        # pads
        padSizes={"L":[1.3,2], "N":[1.3,2], "M":[1.4,2.5]}
        padSpan={"L":8.5, "N":8.5, "M":9}
        super().__init__(name, alternativeLibName,\
            pinCount= 4,\
            pitch=4.5,\
            padSpan=padSpan[density],\
            padDimensions=padSizes[density],\
            bodyDimensions=[6.2, 6.2, 3.6],\
            originMarkSize=defaults.originMarkSize,
            leadDimensions=[1.9, 0.7, 1],\
            court=defaults.court[density],\
            firstPinMarker=False)
        self.addCylinder3Dbody([0,0,0], [3.5,3.5,height])
        self.renamePads([1,2,2,1])
            
