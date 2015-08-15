# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 22:18:17 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from footprints.footprintSmdDualRow import *
from footprints.footprintSmdQuad import *
from footprints.footprintSmdPower import *
from libraryManager.part import part
from symbols.symbolsTransistor import symbolMosfet

class libraryMosfets(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceMosfets")
        self.parts.append(partMosfetBig("N"))
        self.parts.append(partMosfetBig("P"))
        self.parts.append(partMosfetSmall("N"))
        self.parts.append(partMosfetSmall("P"))
        self.parts.append(partMosfetBig("N", "IRLR2905PBF", "DPak"))

class partMosfetBig(part):
    """MOSFET in TO-220, D-Pak, D2Pak, SOT223 package
    
    :param polarity: "N"/"P"
    :param name: name
    :param footprint: "DPak", "TP220", "D2Pak" or "" - all available packages
    """
    def __init__(self, polarity, name="", footprint="", refDes=defaults.transistorRefDes):
        if not name:
            name = "%s-MOS_big" %polarity
        super().__init__(name, refDes)
        self.symbols.append(symbolMosfet(polarity=polarity, pins=[1,2,3]))
        for density in ["L", "N", "M"]:
            if footprint=="" or footprint == "DPak":
                self.footprints.append(footprintDPak(density=density))
            else:
                raise ValueError("Invalid footprint %s" % footprint)

class partMosfetSmall(part):
    """MOSFET in SOT23 package
    
    :param polarity: "N"/"P"
    :param name: name
    :param footprint: "SOT23" or "" - all available packages
    """
    def __init__(self, polarity, name="", footprint="", refDes=defaults.transistorRefDes):
        if not name:
            name = "%s-MOS_small" %polarity
        super().__init__(name, refDes)
        self.symbols.append(symbolMosfet(polarity=polarity, pins=[1,3,2]))
        for density in ["N", "L", "M"]:
            if footprint=="" or footprint == "SOT23":
                self.footprints.append(footprintDPak(density=density))
            else:
                raise ValueError("Invalid footprint %s" % footprint)
