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
from libraries.libraryRLC import footprintSmdChip
from libraryManager.generateLibraries import generateLibraries

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
        self.parts.append(partDiode(diodeType="LED"))
        self.parts.append(partDiode("BAV70", dual="C", footprint="SOT23"))
        self.parts.append(partDiode("BAV99", dual="S", footprint="SOT23"))
        for v in ["3V3", "5V2", "12V", "15V", "24V"]:
            self.parts.append(partDiode("PESD%sS2UT" % v, diodeType="zener",\
                dual="A", footprint="SOT23"))
        for [name, fp] in [["SK1", "SMA"], ["SS1", "SMA"], ["SK2", "SMB"],\
        ["SS2", "SMB"], ["SK3", "SMC"], ["SS3", "SMC"]]:
            for v in [2, 3, 4, 5, 6, 8, 10]:
                self.parts.append(partDiode(name + str(v), diodeType="shottky",\
                    footprint=fp))
        self.parts.append(partLed("ASMB-MTB0-0A3A2", diodes=3, connection="CA",\
            footprint=footprintAvagoPLCC4(),pins=[1,2,3,4]))

class partDiode(part):
    """Diode generator
    
    :param diodeType: "", "shottky", "zener", "LED"
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
        defaultPins={"SOT23":[1,3,2],"SMA":[2,1], "SMB":[2,1], "SMC":[2,1]}
        if not footprint and dual:
            footprint = "SOT23"
        if not pins:
            if footprint:
                pins=defaultPins[footprint]
            else:
                pins=[2,1]
        self.log.debug("New diode: \"%s\", pins: %s, footprint: %s, dual: %s" %\
            (name, pins, footprint, dual))
        self.symbols.append(symbolDiode(diodeType=diodeType, pins=pins, dual=dual, refDes=refDes))
        footprintGenerated=False
        for density in ["N", "L", "M"]:
            defaultFootprints=["SMA", "SMB", "SMC"]
            if footprint=="" or footprint in defaultFootprints:
                for fp in defaultFootprints:
                    if footprint=="" or footprint==fp:
                        self.footprints.append(footprintSmdChip(\
                            size = fp, density = density, alternativeLibName = "niceSemiconductors",\
							body="R"))
                footprintGenerated=True
            if footprint == "SOT23" or footprint=="":
                self.footprints.append(footprintSot23(density=density))
                footprintGenerated=True
            if footprint == "SOD-323" or footprint=="":
                self.footprints.append(footprintSod323(density=density))
                footprintGenerated=True
            if not footprintGenerated:
                raise ValueError("Invalid footprint %s" % footprint)

class symbolDiode(symbol):
    """Symbol for diode
    :param diodeType: "", "shottky", "zener", "LED"
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
        if diodeType=="" or diodeType=="LED":
            points=[[-55, 50], [55, 50]]
        elif diodeType=="zener":
            points=[[-55, 50], [55, 50], [55, 25]]
        elif diodeType=="shottky":
            points=[[-35, 70], [-55, 70], [-55, 50], [55, 50], [55, 30], [35, 30]]
        else:
            raise ValueError("Invalid diode type %s" % diodeType)
        if diodeType=="LED":
            for i in range(2):
                self.primitives.extend(createSymbolArrow(defaults.symbolLineWidth,\
                    -75, 25-50*i, -125, 0-50*i, 25, fillType.foreground))
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
            if dual:
                t.position = [175, t.height*i -25]
            else:
                t.position = [75, t.height*i]
            i=-i

class partLed(part):
    """LED Diode generator
    
    :param name: name
    :param diodes: number of diodes in one package (1+)
    :param connection: diodes connection ("CA" or "CC")
    :param footprint: footprint object
    :param pins: if "CA": [A,C] or [A,C1,C2,C3..] pins, 
    if "CC": [C,A] or [C,A1,A2,A3..] pins, like [1,2]
    """
    def __init__(self, name="", diodes=1, connection="CA", footprint=None, \
    pins=[], refDes=defaults.diodeRefDes):
        if not name:
            if diodes==1:
                name = "led"
            else:
                name = "led_%d%s" %(diodes,connection)
        super().__init__(name, refDes)
        self.log.debug("New LED: \"%s\", pins: %s, footprint: %s, connection: %d %s" %\
            (name, pins, footprint, diodes, connection))
        self.symbols.append(symbolLed(name, diodes, connection,pins,refDes))
        if footprint:
            self.footprints.append(footprint)
        else:
            raise ValueError("Invalid footprint %s" % footprint)

class symbolLed(symbol):
    """LED Diode generator
    
    :param name: name
    :param diodes: number of diodes in one package (1+)
    :param connection: diodes connection ("CA" or "CC")
    :param pins: if "CA": [A,C] or [A,C1,C2,C3..] pins, 
    if "CC": [C,A] or [C,A1,A2,A3..] pins, like [1,2]
    """
    def __init__(self, name, diodes, connection,pins,refDes):
        super().__init__(name=name, refDes=refDes, showPinNames=False, showPinNumbers=True)
        for i in range(diodes):
            # drawing
            symbol = symbolDiode(diodeType="LED",pins=[1,2])
            symbol.movePrimitives([100*(i*2-diodes+1),-25 if connection=="CA" else 25])
            self.primitives.extend(symbol.primitives)
            # pins
            if connection=="CA":
                self.pins.append(symbolPin("C%d"%(i+1),pins[i+1],[100*(i*2-diodes+1),-200],\
                    75,pinType.passive,90))
                self.primitives.append(symbolLine(points=[[100*(i*2-diodes+1),-125],\
                    [100*(i*2-diodes+1),-75]]))
                self.primitives.append(symbolLine(points=[[100*(i*2-diodes+1),75],\
                    [100*(i*2-diodes+1),25]]))
            else:
                self.pins.append(symbolPin("A%d"%(i+1),pins[i+1],[100*(i*2-diodes+1),200],\
                    75,pinType.passive,270))
                self.primitives.append(symbolLine(points=[[100*(i*2-diodes+1),125],\
                    [100*(i*2-diodes+1),75]]))
                self.primitives.append(symbolLine(points=[[100*(i*2-diodes+1),-75],\
                    [100*(i*2-diodes+1),-25]]))
        # pin common
        if connection=="CA":
            self.pins.append(symbolPin("A",pins[0],[0,200],\
                75,pinType.passive,270))
            self.primitives.append(symbolLine(points=[[0,125],[0,25]]))
            if diodes>1:
                self.primitives.append(symbolLine(points=[[100*(diodes-1),75],\
                    [-100*(diodes-1),75]]))
                self.primitives.append(symbolCircle(20,[0,75],10))
        else:
            self.pins.append(symbolPin("C",pins[0],[0,-150],\
                75,pinType.passive,90))
            self.primitives.append(symbolLine(points=[[0,-125],[0,-25]]))
            if diodes>1:
                self.primitives.append(symbolLine(points=[[100*(diodes-1),-75],\
                    [-100*(diodes-1),-75]]))
                self.primitives.append(symbolCircle(20,[0,-75],10))
        self.nameObject.position[0]+=(100*(diodes-1)+50)
        self.valueObject.position[0]+=(100*(diodes-1)+50)
        self.primitives.append(symbolRectangle(width=defaults.symbolLineWidth,\
            position=[-25,0],\
            dimensions=[200*diodes+50, 250], filled=fillType.background))

class footprintSod323(footprintSmdDualRow):
    """
    
    """
    def __init__(self, name="", alternativeLibName="", density="N"):
        if not name:
            name="SOD-323_%s"%(density)
        if not alternativeLibName:
            alternativeLibName="niceSemiconductors"
        bodyDimensions=[1.35, 1.8, 1.1]
        super().__init__(name, alternativeLibName, pinCount=2, pitch=1,\
            padSpan=2.4,padDimensions=[0.6,0.8], bodyDimensions=bodyDimensions,\
            leadDimensions=[0.45,0.4,0.8], court = defaults.court[density])

class footprintAvagoPLCC4(footprintSmdDualRow):
    """
    
    """
    def __init__(self, name="", alternativeLibName="", density="N"):
        if not name:
            name="Avago_PLCC4_%s"%(density)
        if not alternativeLibName:
            alternativeLibName="niceSemiconductors"
        super().__init__(name, alternativeLibName, pinCount=4, pitch=1.7,\
            padSpan=3, padDimensions=[1.1,1.5], \
            bodyDimensions=[3,3.4,2.1], bodyStyle="cube_metal",\
            leadDimensions=[0.15,0.7,1.3], leadStyle="cube_metal", \
            court = defaults.court[density])

if __name__ == "__main__":
    generateLibraries([libraryDiodes()])