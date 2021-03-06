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
from footprints.footprintSmdPower import *
from libraryManager.generateLibraries import generateLibraries

class libraryPowerSupplies(libraryClass):
    """Power supply parts library
    
    Regulators
    """
    def __init__(self):
        super().__init__("nicePowerSupplies")
        self.parts.append(partRegulator3PinBig("78M05CDT", "DPak"))
        self.parts.append(partRegulator3PinBig("78M06CDT", "DPak"))
        self.parts.append(partRegulator3PinBig("AMS1117", "Sot223", pins=[3,1,2], adj=True))
        self.parts.append(partRegulator3PinBig("L78L33ACUTR", "Sot89", pins=[3,2,1]))
        for v in ["1.5", "1.8", "2.5", "2.85", "3.3", "5.0"]:
            self.parts.append(partRegulator3PinBig("AMS1117-%s" %v, "Sot223", pins=[3,1,2]))
        
class partRegulator3PinBig(part):
    """3 Pin regulator part
    
    :param name: Part name, like 78M05CDT
    :param refDes: Part reference designator
    :param footprint: "TO220", "DPak"
    :param positive: True/False - if regulator is positive or negative voltage
    :param adj: if adjustable (pin ADJ) or constant (pin GND)
    """
    def __init__(self, name, footprint, refDes=defaults.icRefDes, positive=True,\
    pins=[1,2,3], adj=False):
        super().__init__(name, refDes)
        self.symbols.append(symbolRegulator3Pin(name, refDes, positive, pins=pins, adj=adj))
        for density in ["N", "L", "M"]:
            if footprint=="DPak":
                self.footprints.append(footprintDPak(density=density))
            elif footprint=="Sot223":
                self.footprints.append(footprintSot223(density=density))
            elif footprint=="Sot89":
                self.footprints.append(footprintSot89(density=density))
            else:
                raise ValueError("Invalid footprint %s" % footprint)

class symbolRegulator3Pin(symbolIC):
    """3 Pin regulator symbol
    
    :param positive: True/False - if regulator is positive or negative voltage
    :param pins: pin numbers for IN, GND, OUT, like: [1,2,3]
    :param adj: if adjustable (pin ADJ) or constant (pin GND)
    """
    def __init__(self, name, refDes=defaults.icRefDes, positive=True, pins=[1,2,3], adj=False):
        pinsLeft = [["IN", pins[0], pinType.pwrIn], None]
        pinsRight = [["OUT", pins[2], pinType.pwrOut], None]
        if not positive:
            pinsRight.reverse()
            pinsLeft.reverse()
        super().__init__(name, pinsLeft, pinsRight, 600, refDes, showPinNames=True, showPinNumbers=True)
        self.pins.append(symbolPin("ADJ" if adj else "GND", pins[1], [0, -200], 100, pinType.pwrIn, 90))
        self.valueObject.position=[x for x in self.nameObject.position]
        self.nameObject.position[1]+=self.nameObject.height*1.5

if __name__ == "__main__":
    generateLibraries([libraryPowerSupplies()])