# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 18:36:14 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from footprints.footprintSmdDualRow import *
from footprints.footprintSmdQuad import *
from footprints.footprintSmdPower import *
from libraryManager.part import part
from libraryManager.symbolPrimitive import *
from libraries.libraryMosfets import *
from libraryManager.generateLibraries import generateLibraries

class libraryDrivers(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceDrivers")
        self.parts.append(partLsDriver("BTS142D", "DPak"))
        self.parts.append(partLsDriver())
        self.parts.append(partHsDriverDpak("BTS5012SDA", "DPak"))
        self.parts.append(partHsDriverDpak("BTS6143D", "DPak"))
        self.parts.append(partHsDriverDpak("BTS6133D", "DPak"))
        self.parts.append(partHsDriverDpak())

class partLsDriver(part):
    """
    LS driver in D-Pak package
    :param name: name
    :param footprint: "DPak" or "" - all available packages
    """
    def __init__(self, name="", footprint="", refDes=defaults.icRefDes):
        if not name:
            name = "LS_driver"
        super().__init__(name, refDes)
        self.symbols.append(symbolLsDriver(pins=[1,2,3]))
        for density in ["N", "L", "M"]:
            if footprint=="" or footprint == "DPak":
                self.footprints.append(footprintDPak(density=density))
            else:
                raise ValueError("Invalid footprint %s" % footprint)

class symbolLsDriver(symbolMosfet):
    """
    MOSFET LS driver
    """
    def __init__(self, name="", refDes=defaults.icRefDes,pins=[1,2,3],diode=True):
        """
        diode: True, False
        pins: pin numbers for G,D,S, like: [1,2,3]
        """
        if not name:
            name = "LS_driver" 
        super().__init__(name, refDes, "N", pins, diode, showPinNames=False,\
            showPinNumbers=False)
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
            -150, -175, 125, 175, filled=fillType.background))

class partHsDriverDpak(part):
    """
    HS driver in D-Pak 5 package
    :param name: name
    :param footprint: "DPak" or "" - all available packages
    """
    def __init__(self, name="", footprint="", refDes=defaults.icRefDes):
        if not name:
            name = "HS_driver_DPAK5"
        super().__init__(name, refDes)
        self.symbols.append(symbolHsDriverDpak(pins=[3,2,4,1,5]))
        for density in ["N", "L", "M"]:
            if footprint=="" or footprint == "DPak":
                self.footprints.append(footprintDPak(pins=5, density=density))
            else:
                raise ValueError("Invalid footprint %s" % footprint)

class symbolHsDriverDpak(symbolMosfet):
    """
    MOSFET HS in D-Pak 5 package
    """
    def __init__(self, name="", refDes=defaults.icRefDes,pins=[3,2,4,1,5],diode=True):
        """
        diode: True, False
        pins: pin numbers for VBB, IN, IS, OUT, OUT like: [3,2,4,1,5]
        """
        if not name:
            name = "HS_driver_DPAK5" 
        super().__init__(name, refDes, "N", pins="", diode=diode, showPinNames=False,\
            showPinNumbers=False)
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
            -300, -300, 300, 300, filled=fillType.background))
        self.pins.append(symbolPin("IN", pins[1], [-400,100], 100, pinType.input,0))
        self.pins.append(symbolPin("IS", pins[2], [-400,-100], 100, pinType.passive,0))
        self.pins.append(symbolPin("VBB", pins[0], [400,200], 100, pinType.output,180))
        self.pins.append(symbolPin("OUT", pins[3], [400,-100], 100, pinType.output,180))
        self.pins.append(symbolPin("OUT", pins[4], [400,-200], 100, pinType.output,180))
        self.showPinNames=True
        self.showPinNumbers=True
        self.nameObject.position=[0,350]
        self.valueObject.position=[0,-350]
        self.nameObject.align=textAlign.center
        self.valueObject.align=textAlign.center

if __name__ == "__main__":
    generateLibraries([libraryDrivers()])