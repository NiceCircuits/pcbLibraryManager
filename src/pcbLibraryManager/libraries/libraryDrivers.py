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

if __name__ == "__main__":
    generateLibraries([libraryDrivers()])