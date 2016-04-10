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
from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *

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
        self.parts.append(partMosfetSmall("N", "IRLML6244TRPBF", "SOT23"))
        self.parts.append(partMosfetSmall("P", "IRLML6402PBF", "SOT23"))

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
        for density in ["N", "L", "M"]:
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
                self.footprints.append(footprintSot23(density=density))
            else:
                raise ValueError("Invalid footprint %s" % footprint)

class symbolMosfet(symbol):
    """
    Standard symbol for mosfet (3 pin with/without diode)
    """
    def __init__(self, name="", refDes=defaults.transistorRefDes, polarity="N", pins=[1,2,3],\
        diode=True, showPinNames=False, showPinNumbers=False):
        """
        polarity: N, P
        diode: True, False
        pins: pin numbers for G,D,S, like: [1,2,3]
        """
        if not name:
            name = "%s-MOS" % polarity
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        if polarity == "P":
            flip=-1
        else:
            flip=1
        # pins
        if pins:
            self.pins.append(symbolPin("G", pins[0], [-200,-100*flip], 100, pinType.passive, 0))
            self.pins.append(symbolPin("D", pins[1], [0,200*flip], 100, pinType.passive, 90*(2+flip)))
            self.pins.append(symbolPin("S", pins[2], [0,-200*flip], 100, pinType.passive, 90*(2-flip)))
        # drawing
        self.primitives.append(symbolLine(defaults.symbolThickLineWidth, -100, -133, -100, 133))
        for i in range(3):
            self.primitives.append(symbolLine(defaults.symbolThickLineWidth, -67, -133+100*i, -67, -67+100*i))
            self.primitives.append(symbolLine(defaults.symbolLineWidth, -67, -100+100*i, 0, -100+100*i))
        self.primitives.append(symbolLine(defaults.symbolLineWidth, 0, -100*flip, 0, 0))
        self.primitives.extend(createSymbolArrow(defaults.symbolLineWidth,\
            -33, 0, -33*(1+flip), 0, 33, fillType.foreground))
        if diode:
            self.primitives.append(symbolPolyline(defaults.symbolLineWidth,\
                [[0,-100], [67,-100], [67,100], [0,100]]))
            self.primitives.append(symbolLine(defaults.symbolLineWidth, 33, 33, 100, 33))
            self.primitives.extend(createSymbolArrow(defaults.symbolLineWidth,\
                67, -33, 67, 33, 66, fillType.foreground))
        # texts
        i=1
        for t in [self.nameObject, self.valueObject]:
            t.align = textAlign.centerLeft
            t.position = [25 + 100*diode, t.height*i]
            i=-i
