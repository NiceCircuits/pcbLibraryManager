# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 06:41:54 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.symbol import symbol
from footprints.footprintSmdDualRow import footprintSoic, footprintSot23
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from libraryManager.symbolPrimitive import *
import os.path
from libraryManager.generateLibraries import generateLibraries

class libraryOpamps(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceOpamps")
        for name in ["OpAmp_SOIC1", "TL071CD"]:
            self.parts.append(partOpamp(name,parts=1,package="SOIC"))
        for name in ["OpAmp_SOIC2", "TL072CD", "LM358AM"]:
            self.parts.append(partOpamp(name,parts=2,package="SOIC"))
        for name in ["OpAmp_SOT23", "LMV116MF", "MCP6051T-E/OT"]:
            self.parts.append(partOpamp(name,parts=1,package="SOT23"))

class partOpamp(part):
    """
    Op-amp part
    """
    def __init__(self, name, refDes=defaults.icRefDes, parts=1, package="SOIC"):
        super().__init__(name, refDes)
        if package=="SOIC" and parts==1:
            pinNumbers=[3,2,6,4,7,1,8,5]
            self.symbols.append(symbolOpamp(name,pinNumbers=pinNumbers, variant=2))
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSoic(8,density=density))
        elif package=="SOT23" and parts==1:
            pinNumbers=[3,4,1,2,5]
            self.symbols.append(symbolOpamp(name,pinNumbers=pinNumbers, variant=1))
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSot23(5,density=density))
        elif package=="SOIC" and parts==2:
            pinNumbers=[3,2,1]
            self.symbols.append(symbolOpamp(name,pinNumbers=pinNumbers, variant=0))
            pinNumbers2=[5,6,7]
            self.symbols.append(symbolOpamp(name,pinNumbers=pinNumbers2, variant=0))
            pinNumbers3=[4,8]
            self.symbols.append(symbolOpampPower(name,pinNumbers=pinNumbers3))
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSoic(8,density=density))
        else:
            raise ValueError("Invalid combnation: package=%s, parts=%d"%(package, parts))

class symbolOpamp(symbol):
    """
    Opamp symbol
    """
    def __init__(self, name="", refDes=defaults.icRefDes, pinNumbers=[3,2,6,4,7,1,8,5],\
        pinNames=["+","-","OUT","GND","VCC","AUX1","AUX2","AUX3"], variant=0):
        """
        param pinNumbers: pin numbers for +IN, -IN, OUT, GNC, VCC, AUX1, AUX2, AUX3,
            like: [3,2,1] or [3,2,6,4,7] or [3,2,6,4,7,1,8,5]
        param pinNames: pin names for +IN, -IN, OUT, GNC, VCC, AUX1, AUX2, AUX3,
            like: ["+","-","OUT","GND","VCC",]
        """
        super().__init__(name, refDes=refDes, showPinNames=False, showPinNumbers=True)
        points=[[-150,-200],[-150,200],[-200,0],[-200,-150]]
        self.primitives.append(symbolPolyline(defaults.symbolLineWidth,points,\
            filled=fillType.background))
        self.pins.append(symbolPin(pinNames[0], pinNumbers[0], [-200,100], 50,\
            pinType.input,0))
        self.pins.append(symbolPin(pinNames[1], pinNumbers[1], [-200,-100], 50,\
            pinType.input,0))
        self.pins.append(symbolPin(pinNames[2], pinNumbers[2], [300,0], 100,\
            pinType.input,180))
        self.nameObject.position=[100,100]
        self.nameObject.align=textAlign.centerLeft
        self.valueObject.position=[100,-100]
        self.valueObject.align=textAlign.centerLeft
        if variant >= 1:
            # power pins
            self.pins.append(symbolPin(pinNames[3], pinNumbers[3], [0,-200], 50,\
                pinType.input,90))
            self.pins.append(symbolPin(pinNames[4], pinNumbers[4], [0,200], 50,\
                pinType.input,270))

class symbolOpampPower(symbol):
    """
    Opamp power symbol
    """
    def __init__(self, name="", refDes=defaults.icRefDes, pinNumbers=[4,8],\
        pinNames=["GND","VCC",]):
        """
        param pinNumbers: pin numbers for GNC, VCC, like: [4, 8]
        param pinNames: pin names for GNC, VCC, like: ["GND","VCC"]
        """
        super().__init__(name, refDes=refDes, showPinNames=False, showPinNumbers=True)
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,position=[0,0],\
            dimensions=[100,300], filled=fillType.background))
        # power pins
        self.pins.append(symbolPin(pinNames[0], pinNumbers[0], [0,-200], 50,\
            pinType.input,90))
        self.pins.append(symbolPin(pinNames[1], pinNumbers[1], [0,200], 50,\
            pinType.input,270))

if __name__ == "__main__":
    generateLibraries([libraryOpamps()])