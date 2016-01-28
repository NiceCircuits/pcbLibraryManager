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
from libraryManager.generateLibraries import generateLibraries

class librarySwitches(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSwitches")
        for v in ["H","V"]:
            for h in [4.3, 5, 7, 9.5, 13, 19]:
                self.parts.append(partMicroswitchSmt(h,v))
            self.parts.append(partMicroswitchSmt6x4(v))

class partMicroswitchSmt(part):
    """
    Default SMT microswitch
    """
    def __init__(self, height, variant="H"):
        variantStr = "_V" if variant=="V" else ""
        name = "MicroswitchSmt-%1.1f%s" % (height, variantStr)
        super().__init__(name, defaults.switchRefDes)
        self.symbols.append(symbolButton(variant=variant))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintMicroswitchSmt(density, height))
            
class partMicroswitchSmt6x4(part):
    """
    SMT microswitch 6x4mm
    """
    def __init__(self,variant="H"):
        variantStr = "_V" if variant=="V" else ""
        name = "MicroswitchSmt6x4%s" % variantStr
        super().__init__(name, defaults.switchRefDes)
        self.symbols.append(symbolButton(variant=variant))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintMicroswitchSmt6x4(density))
            

class symbolButton(symbol):
    """Button symbol
    """
    def __init__(self, name="button", refDes=defaults.switchRefDes, showPinNames=False,\
    showPinNumbers=False, pinNumbers=[1,2], variant="H"):
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
        if variant=="H":
            self.nameObject.position=[0, 120]
            self.valueObject.position=[0, -80]
        elif variant=="V":
            self.movePrimitives([0,0],90)
            self.nameObject.position=[50, 50]
            self.nameObject.align=textAlign.centerLeft
            self.valueObject.position=[50, -50]            
            self.valueObject.align=textAlign.centerLeft
        else:
            raise ValueError("unsupported variant %s" % variant)

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
        
class footprintMicroswitchSmt6x4(footprintSmdDualRow):
    """
    SMT microswitch 6x4mm
    """
    def __init__(self, density, name="", alternativeLibName="niceSwitches"):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            name="MicroswitchSmd6x4_%s" % ( density)
        # pads
        padSizes={"L":[1.2,1.3], "N":[1.4,1.5], "M":[1.6,1.7]}
        padSpan={"L":7.7, "N":7.8, "M":7.9}
        super().__init__(name, alternativeLibName,\
            pinCount= 2,\
            pitch=4.5,\
            padSpan=padSpan[density],\
            padDimensions=padSizes[density],\
            bodyDimensions=[3.9,6.3,2],\
            originMarkSize=defaults.originMarkSize,
            leadDimensions=[1, 0.6, 1],\
            court=defaults.court[density],\
            firstPinMarker=False)
        self.addSimple3Dbody([0,0,0], [1.2,2.6,2.5],file="cube_metal")
            
if __name__ == "__main__":
    generateLibraries([librarySwitches()])