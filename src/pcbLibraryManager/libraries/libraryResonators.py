# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 06:39:59 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from math import ceil
from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *


class libraryResonators(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceResonators")
        for footprint in ["3.7x3.1"]:
            for freq in ["8Mhz", "16MHz"]:
                self.parts.append(partResonator3Pin("Ceramic_%s_%s" %(footprint, freq), footprint))

class partResonator3Pin(part):
    """3 Pin resonator (ceramic or quartz)
    """
    def __init__(self, name, footprint):
        super().__init__(name, defaults.resonatorRefDes)
        self.symbols.append(symbolResonator3Pin())
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintResonator3Pin(footprint, density))

class symbolResonator3Pin(symbol):
    """3 Pin resonator (ceramic or quartz)
    """
    def __init__(self, name="Resonator_3pin", refDes=defaults.resonatorRefDes, showPinNames=False,
    showPinNumbers=False, pinNumbers=[1,2,3]):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in [-1,1]:
            self.pins.append(symbolPin(i+2, pinNumbers[i+1], [200*i,0],\
                140, pinType.passive, rotation=180 if i>0 else 0))
            self.primitives.append(symbolLine(defaults.symbolThickLineWidth,\
                i*60, 75, i*60, -75))
        self.pins.append(symbolPin(2, pinNumbers[1], [0,-200],\
            100, pinType.passive, rotation=90))
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
            position=[0,0], dimensions=[70, 200]))
        self.nameObject.position=[0, 230]
        self.valueObject.position=[0, 150]

class footprintResonator3Pin(footprint):
    """3 Pin resonator (ceramic or quartz), SMT or THT
    """
    def __init__(self, size, density, name="", alternativeLibName="niceResonators"):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            name = "%s_%s"%(size,density)
        tht = {"3.7x3.1":False}
        body = {"3.7x3.1":[3.9,3.3,1.5]}
        pad1 = {"3.7x3.1":{"L":[0.7,4.1], "N":[0.7,4.1], "M":[0.7,4.1]}}
        pad2 = {"3.7x3.1":{"L":[1.0,4.1], "N":[1.0,4.1], "M":[1.0,4.1]}}
        padSpan = {"3.7x3.1":{"L":1.5, "N":1.5, "M":1.5}}
        court = {"3.7x3.1":defaults.court}
        
        originMarkSize = min(defaults.originMarkSize, body[size][1]*0.25)
        super().__init__(name, alternativeLibName, originMarkSize=originMarkSize)
        # pads
        for x in [-1,1]:
            if tht[size]:
                raise ValueError("Not imlemented yet") # TODO:
            else:
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper,\
                    position=[padSpan[size][density]*x,0], dimensions=pad1[size][density],\
                    name=x+2))
        if tht[size]:
            raise ValueError("Not imlemented yet") # TODO:
        else:
            self.primitives.append(pcbSmtPad(pcbLayer.topCopper,\
                position=[0,0], dimensions=pad2[size][density], name=2))
            [dim1, dim2]=self.addCourtyardAndSilk(\
                [max(pad1[size][density][0]+2*padSpan[size][density], body[size][0]),\
                pad1[size][density][1]], court[size][density])
        # body
        self.addSimple3Dbody([0,0], body[size], file="cube_orange")
        # name, value
        if (self.valueObject.height + self.nameObject.height + 0.6) < body[size][1]:
            y = body[size][1]/2 - self.valueObject.height/2 - 0.2
        else:
            y = self.valueObject.height + dim1[1]/2
        self.valueObject.position = [0, -y]
        self.nameObject.position = [0, y]
