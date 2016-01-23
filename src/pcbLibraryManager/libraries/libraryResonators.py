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
        self.parts.append(partResonator(2, "XT_2pin", ""))
        self.parts.append(partResonator(3, "XT_3pin", ""))
        self.parts.append(partQuartzHC49())
        for freq in ["8Mhz", "16MHz"]:
            for footprint in ["3.7x3.1"]:
                self.parts.append(partResonator(3, "Ceramic_%s_%s" %(footprint, freq), footprint))
            self.parts.append(partQuartzHC49(freq=freq))
        self.parts.append(partQuartzWatch(freq="32.768kHz"))

class partQuartzHC49(part):
    """
    HC49 part generator
    """
    def __init__(self, variant="", freq=""):
        name="QuartzHC49%s_%s" % (variant,freq)
        super().__init__(name, defaults.resonatorRefDes)
        self.symbols.append(symbolResonator(2))
        if not variant:
            variants=["U","S"]
        else:
            variants=[variant]
        for v in variants:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintHC49(v,density))

class partQuartzWatch(part):
    """
    Watch quartz part generator
    """
    def __init__(self, variant="", freq=""):
        name="QuartzWatch%s_%s" % (str(variant),freq)
        super().__init__(name, defaults.resonatorRefDes)
        self.symbols.append(symbolResonator(2))
        if not variant:
            variants=[2,3]
        else:
            variants=[variant]
        for v in variants:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintQuartzWatch(v,density))

class partResonator(part):
    """2/3 Pin resonator (ceramic or quartz)
    """
    def __init__(self, pins, name, footprint):
        super().__init__(name, defaults.resonatorRefDes)
        self.symbols.append(symbolResonator(pins))
        if footprint:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintResonator3Pin(footprint, density))

class symbolResonator(symbol):
    """2 or 3 Pin resonator (ceramic or quartz)
    """
    def __init__(self, pins=2, name="", refDes=defaults.resonatorRefDes, showPinNames=False,
    showPinNumbers=False, pinNumbers=[]):
        if not name:
            name = "Resonator_%dpin" % pins
            if not pinNumbers:
                if pins==3:
                    pinNumbers=[1,2,3]
                else:
                    pinNumbers=[1,0,2]
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in [-1,1]:
            self.pins.append(symbolPin(pinNumbers[i+1], pinNumbers[i+1], [200*i,0],\
                140, pinType.passive, rotation=180 if i>0 else 0))
            self.primitives.append(symbolLine(defaults.symbolThickLineWidth,\
                i*60, 75, i*60, -75))
        if pins==3:
            self.pins.append(symbolPin(2, pinNumbers[1], [0,-200],\
                100, pinType.passive, rotation=90))
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
            position=[0,0], dimensions=[70, 200]))
        self.nameObject.position=[0, 230]
        self.valueObject.position=[0, 150]

class footprintQuartzWatch(footprint):
    """
    32768Hz watch quartz cylindrical case
    size: 2/3 - diameter of case {2:2.1,3:3.2}
    """
    def __init__(self, size=2, density="N", name="", alternativeLibName="niceResonators"):
        if not name:
            name = "XT_cyl_%d_%s"%(size,density)
        D={2:2.1,3:3.2}
        H={2:6.2,3:8.2}
        span={2:1.2,3:1.2}
        drill={2:0.5,3:0.5}
        padTht = {2:{"L":[0.9,0.9], "N":[0.9,1.1], "M":[0.9,1.3]},\
                  3:{"L":[0.9,0.9], "N":[0.9,1.1], "M":[0.9,1.3]}}
        originMarkSize = min(defaults.originMarkSize, D[size]*0.25)
        super().__init__(name, alternativeLibName, originMarkSize=originMarkSize)
        # pads & body
        for x in [-1,1]:
            self.primitives.append(pcbThtPad([x*span[size]/2,0],padTht[size][density],\
                drill[size],int((x+3)/2)))
            self.addCylinder3Dbody([x*span[size]/2,0,-2],[0.4,0.4,3],\
                draw=False, silk=False,file="cylinder_metal")
        # body
        self.addCylinder3Dbody([0,0,1], [D[size],D[size],H[size]],\
            draw=True, silk=True, file="cylinder_metal")
        [dim1, dim2]=self.addCourtyardAndSilk(
            [max(D[size],span[size]+padTht[size][density][0]),\
            max(D[size],padTht[size][density][1])],\
            defaults.court[density],silk=False)
        # name, value
        if (self.valueObject.height + self.nameObject.height + 0.6) < D[size]:
            y = D[size]/2 - self.valueObject.height/2 - 0.2
        else:
            y = self.valueObject.height + dim1[1]/2
        self.valueObject.position = [0, -y]
        self.nameObject.position = [0, y]

class footprintHC49(footprint):
    """
    HC49 quartz footprint
    variant: "U", "S", "SM"
    """
    def __init__(self, variant="U", density="N", name="", alternativeLibName="niceResonators"):
        if not name:
            name = "HC49%s_%s"%(variant,density)
        padTht = {"L":[1.1,1.1], "N":[1.5,1.5], "M":[1.7,1.7]}
        spanTht=4.88
        drill=0.6
        L1=10.5
        L2=11.5
        W1=3.8
        W2=4.9
        H1={"U":13.5,"S":3.5,"SM":4.3}
        H2=1
        originMarkSize = min(defaults.originMarkSize, W2*0.25)
        super().__init__(name, alternativeLibName, originMarkSize=originMarkSize)
        # pads & body
        for x in [-1,1]:
            if variant=="U" or variant=="S":
                self.primitives.append(pcbThtPad([x*spanTht/2,0],padTht[density],\
                    drill,int((x+3)/2)))
                self.addCylinder3Dbody([x*spanTht/2,0,-2],[0.488,0.488,2],\
                    draw=False, silk=False,file="cylinder_metal")
                self.addCylinder3Dbody([(L1-W1)/2*x,0],[W1,W1,H1[variant]],\
                    draw=False, silk=False,file="cylinder_metal")                
                self.addCylinder3Dbody([(L2-W2)/2*x,0],[W2,W2,H2],\
                    draw=False, silk=False,file="cylinder_metal")                
            else:
                raise ValueError("Not imlemented yet") # TODO:
        # body
        self.addSimple3Dbody([0,0], [L1-W1,W1,H1[variant]], draw=False, silk=False, file="cube_metal")
        if variant=="SM":
            self.addSimple3Dbody([0,0], [L2,W2,H2], draw=False, silk=False, file="cube_metal")
        else:
            self.addSimple3Dbody([0,0], [L2-W2,W2,H2], draw=False, silk=False, file="cube_metal")
        [dim1, dim2]=self.addCourtyardAndSilk([L2,W2],defaults.court[density])
        # name, value
        if (self.valueObject.height + self.nameObject.height + 0.6) < W2:
            y = W2/2 - self.valueObject.height/2 - 0.2
        else:
            y = self.valueObject.height + dim1[1]/2
        self.valueObject.position = [0, -y]
        self.nameObject.position = [0, y]

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
