# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 22:19:20 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from footprints.footprintSmdChip import footprintSmdChip
from libraryManager.part import part
from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from symbols.symbolsRLC import *
from libraryManager.defaults import *
from math import ceil

class libraryRLC(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceRLC")
        self.parts.append(partR())
        self.parts.append(partC())
        self.parts.append(partResistorNetwork())

class partR(part):
    """
    Resistor part
    """
    def __init__(self):
        super().__init__("R", "R")
        self.symbols.append(symbolR("R"))
        for size in ["0402", "0603", "0805", "1206", "1210", "2010", "2512"]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSmdChip(size + "_" + density, \
                    size = size, density = density, alternativeLibName = "niceRLC"))

class partC(part):
    """
    Capacitor part
    """
    def __init__(self):
        super().__init__("C", "C")
        self.symbols.append(symbolC("C"))
        for size in ["0402", "0603", "0805", "1206", "1210", "2010", "2512"]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSmdChip(size + "_" + density, \
                    size = size, density = density, alternativeLibName = "niceRLC"))

class partResistorNetwork(part):
    """
    """
    def __init__(self):
        name = "R_Network_4"
        refDes = "RN"
        super().__init__(name, refDes)
        for i in range(4):
            self.symbols.append(symbolR(name, refDes, showPinNumbers=True, pinNumbers=[i+1, 8-i]))
        for size in ["0402", "0603"]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintResistorNetwork('4x' + size + "_" + density, \
                    size = size, density = density, alternativeLibName = "niceRLC"))

class footprintResistorNetwork(footprint):
    """
    SMT resistor networks (0402, 0603) x4
    """
    def __init__(self, name, size, density, alternativeLibName, networkType="convex"):
        """
        size: "0402", "0603"
        density: "L" - least, "N" - nominal, "M" - most
        networkType: "convex", "concave"
        """
        chipSize = {'0402':[2.1, 1.1], '0603':[3.4, 1.8]}
        leadSize = {'0402':[0.3, 0.2], '0603':[0.5, 0.3]}
        pitch = {'0402': 0.5, '0603': 0.8}
        padSize1 = {'0402':{'L':[0.25, 0.45], 'N':[0.3, 0.6], 'M':[0.3, 0.7]},\
            '0603':{'L':[0.55, 0.7], 'N':[0.55, 0.8], 'M':[0.6, 1]}}
        padSize2 = {'0402':{'L':[0.4, 0.45], 'N':[0.45, 0.6], 'M':[0.45, 0.7]},\
            '0603':{'L':[0.8, 0.7], 'N':[0.8, 0.8], 'M':[0.85, 1]}}
        padSpan = {'0402':{'L':0.65, 'N':0.8, 'M':0.9},'0603':{'L':1.35, 'N':1.45, 'M':1.65}}
        court = {'0402':{'L':0.1, 'N':0.15, 'M':0.2},'0603':{'L':0.1, 'N':0.25, 'M':0.5}}
        rCount = 4
        originMarkSize = min(defaults.originMarkSize, chipSize[size][1]*0.2)
        super().__init__(name, alternativeLibName, originMarkSize=originMarkSize)
        # pads
        x1 = pitch[size] * (rCount/2 - 0.5)
        for y in [-1, 1]:
            for x in range(int(rCount)):
                if (x==0) or (x==(rCount-1)): # outer leads
                    padSize=padSize2[size][density]
                    offset = (padSize2[size][density][0]-padSize1[size][density][0])/2 * (-1 if x>0 else 1)
                else:
                    padSize=padSize1[size][density]
                    offset=0
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=\
                    [(x1-pitch[size]*x+offset)*y, padSpan[size][density]/2*y],dimensions=padSize,\
                    name=str(int(x+1 if y<0 else x+rCount+1)),rotation=0 if y<0 else 180))
        # body
        self.primitives.append(pcbRectangle(pcbLayer.topAssembly, width=defaults.documentationWidth,\
            position=[0,0], dimensions=[chipSize[size][0],chipSize[size][1]-2*leadSize[size][1]]))
        # leads
        for y in [-1, 1]:
            for x in range(int(rCount)):
                x1 = pitch[size] * (rCount/2 - 0.5)
                y1 = chipSize[size][1]/2-leadSize[size][1]/2
                offset=0
                lead=list(leadSize[size])
                if (x==0) or (x==(rCount-1)): # outer leads
                    offset = (chipSize[size][0] - (rCount-1)*pitch[size] - leadSize[size][0])/4
                    lead[0]=lead[0]+offset*2
                    if x>0:
                        offset=-offset
                self.primitives.append(pcbRectangle(pcbLayer.topAssembly, defaults.documentationWidth,\
                    position=[(x1-pitch[size]*x+offset)*y, y*y1],dimensions=lead))
        # courtyard
        dim1=[ceil((max((rCount-1)*pitch[size]+2*padSize2[size][density][0]-padSize1[size][density][0],\
            chipSize[size][0])+2*court[size][density])*5)/5,\
            ceil((max(padSpan[size][density]+padSize1[size][density][1], chipSize[size][1])+2*court[size][density])*5)/5]
        self.primitives.append(pcbRectangle(pcbLayer.topCourtyard, width=defaults.documentationWidth,\
            position=[0,0], dimensions=dim1))
        # name, value
        y = self.valueObject.height + dim1[1]/2
        self.valueObject.position = [0, -y]
        self.nameObject.position = [0, y]
        # silkscreen
        if court[size][density]>defaults.silkWidth:
            dim1 = [dim1[0]-2*court[size][density]+2*defaults.silkWidth,\
                dim1[1]-2*court[size][density]+2*defaults.silkWidth]
            self.primitives.append(pcbRectangle(pcbLayer.topSilk, width=defaults.silkWidth,\
                position=[0,0], dimensions=dim1))
            