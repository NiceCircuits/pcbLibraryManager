# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:51:22 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from footprints.footprintSmdDualRow import *
from footprints.footprintSmdPower import *
from libraryManager.part import part
from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *
from libraryManager.defaults import *
from libraryManager.common import *


class libraryDiodes(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceDiodes")
        for dual in ["", "A", "C", "S"]:
            for diodeType in ["", "shottky", "zener"]:
                self.parts.append(partDiode(diodeType=diodeType, dual=dual))
            basPostfix={"":"", "S":"-04", "C":"-05", "A":"-06"}
            for name in ["BAS40", "BAS70"]:
                self.parts.append(partDiode(name=name+basPostfix[dual],\
                diodeType="shottky", dual=dual, footprint="SOT23"))
        self.parts.append(partDiode("BAV70", dual="C", footprint="SOT23"))
        self.parts.append(partDiode("BAV99", dual="S", footprint="SOT23"))
        for v in ["3V3", "5V2", "12V", "15V", "24V"]:
            self.parts.append(partDiode("PESD%sS2UT" % v, diodeType="zener",\
                dual="A", footprint="SOT23"))

class partDiode(part):
    """Diode generator
    
    :param diodeType: "", "shottky", "zener"
    :param name: name
    :param footprint: "DPak", "TP220", "D2Pak" or "" - all available packages
    :param pins: [A,C] pins, like [1,2]
    """
    def __init__(self, name="", diodeType="", footprint="", refDes=defaults.diodeRefDes,\
    pins=[], dual=""):
        if not name:
            name = "diode%s%s%s%s" % ("_" if diodeType else "", diodeType,\
                "_dual_" if dual else "", dual)
        super().__init__(name, refDes)
        defaultPins={"SOT23":[1,3,2]}
        if not pins:
            if footprint:
                pins=defaultPins[footprint]
            else:
                pins=[1,3,2]
        self.symbols.append(symbolDiode(diodeType=diodeType, pins=pins, dual=dual, refDes=refDes))
        for density in ["N", "L", "M"]:
            if footprint=="" or footprint == "SOT23":
                self.footprints.append(footprintSot23(density=density))
            else:
                raise ValueError("Invalid footprint %s" % footprint)

class symbolDiode(symbol):
    """Symbol for diode
    :param diodeType: "", "shottky", "zener"
    :param name: name
    :param footprint: "DPak", "TP220", "D2Pak" or "" - all available packages
    :param pins: [A,C] pins, like [1,2]
    :param dual: "" - single diode, "C", "A", "S" - common Cathode, Anode, Series connected diodes
    :param alternative: 0/1 - alternative symbol for dual diodes
    """
    def __init__(self, name="", refDes=defaults.diodeRefDes, diodeType="", pins=[],\
    dual="", showPinNames=False, showPinNumbers=False, alternative=0):
        if not name:
            name = "diode%s%s%s%s" % ("_" if diodeType else "", diodeType,\
                "_dual_" if dual else "", dual)
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        # pins
        if not pins:
            raise ValueError("No pins provided!")
        if dual=="A":
            pinNames=["C1", "A", "C2"]
        elif dual=="C":
            pinNames=["A1", "C", "A2"]
        elif dual=="S":
            pinNames=["A", "COM", "C"]
        else:
            pinNames=["C", "A"]
        if dual:
            sides=[-1,1]
        else:
            sides=[0]
        for i in sides:
            n=0 if i < 1 else 2
            self.pins.append(symbolPin(pinNames[n], pins[n], [100*i,100], 75 if dual else 50,\
                pinType.passive, 270))
        self.pins.append(symbolPin(pinNames[1], pins[1], [0,-200 if dual else -100],\
            75 if dual else 50, pinType.passive, 90))
        # drawing
        if diodeType=="":
            points=[[-55, 50], [55, 50]]
        elif diodeType=="zener":
            points=[[-55, 50], [55, 50], [55, 25]]
        elif diodeType=="shottky":
            points=[[-35, 70], [-55, 70], [-55, 50], [55, 50], [55, 30], [35, 30]]
        else:
            raise ValueError("Invalid diode type %s" % diodeType)
        for i in sides:
            if dual=="C" or (dual=="S" and i<0) or dual=="":
                rot=180
            else:
                rot=0
            self.primitives.append(symbolPolyline(defaults.symbolLineWidth,\
                translatePoints(rotatePoints(points, rot), [100*i, -25 if dual else 0])))
            self.primitives.extend(createSymbolArrow(defaults.symbolLineWidth,\
                points=translatePoints(rotatePoints([[0, -50], [0, 50]], rot),\
                [100*i, -25 if dual else 0]), headLength=100, filled=fillType.foreground))
        if dual:
            self.primitives.append(symbolPolyline(defaults.symbolLineWidth,\
                [[-100, -75], [-100, -125], [100, -125], [100, -75]]))
        # texts
        i=1
        for t in [self.nameObject, self.valueObject]:
            t.align = textAlign.centerLeft
            t.position = [175 if dual else 75, t.height*i -(25 if dual else 0)]
            i=-i
