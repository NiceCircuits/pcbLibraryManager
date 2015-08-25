# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 22:19:20 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *


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
        for size in ["0603", "0402", "0805", "1206", "1210", "2010", "2512"]:
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
        for size in ["0603", "0402", "0805", "1206", "1210", "2010", "2512"]:
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
        for size in ["0603", "0402"]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintResistorNetwork('4x' + size + "_" + density, \
                    size = size, density = density, alternativeLibName = "niceRLC"))

class symbolR(symbol):
    """Resistor symbol
    """
    def __init__(self, name, refDes="R", showPinNames=False, showPinNumbers=False, pinNumbers=[1,2]):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in range(2):
            self.pins.append(symbolPin(i+1, pinNumbers[i], [200 if i else -200,0],\
                100, pinType.passive, rotation=180 if i else 0))
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
            position=[0,0], dimensions=[200, 80]))
        self.nameObject.position=[0, 80]
        self.valueObject.position=[0, 0]
        self.valueObject.height = defaults.symbolSmallTextHeight

class symbolC(symbol):
    """Capacitor symbol
    """
    def __init__(self, name, refDes="C", showPinNames=False, showPinNumbers=False, pinNumbers=[1,2]):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in range(2):
            self.pins.append(symbolPin(i+1, pinNumbers[i], [0, -100 if i else 100],\
                70, pinType.passive, rotation=90 if i else 270))
            self.primitives.append(symbolLine(defaults.symbolThickLineWidth,\
                -80, 30 if i else -30, 80, 30 if i else -30))
        self.nameObject.position=[20, 100]
        self.nameObject.align=textAlign.centerLeft
        self.valueObject.position=[20, -100]
        self.valueObject.align=textAlign.centerLeft

class footprintSmdChip(footprint):
    """
    Chip component (0603, 0805 etc.)
    """
    def __init__(self, name, size, density, alternativeLibName):
        """
        size: "0603", "0805"
        density: "L" - least, "N" - nominal, "M" - most
        """
        dimensions = {
            '0402':{'chip':[1.1, 0.6, 0.6], 'pad':{'L':[0.4, 0.6], 'N':[0.5, 0.65], 'M':[0.6, 0.75]}, 'L':{'L':1.1, 'N':1.35, 'M':1.55}, 'court':{'L':0.1, 'N':0.15, 'M':0.26}},
            '0603':{'chip':[1.75, 0.95, 0.85], 'pad':{'L':[0.8, 0.85], 'N':[1, 0.95], 'M':[1.2, 1.1]}, 'L':{'L':2.05, 'N':2.45, 'M':2.9}, 'court':{'L':0.1, 'N':0.26, 'M':0.5}},
            '0805':{'chip':[2.2, 1.45, 1.1], 'pad':{'L':[1, 1.35], 'N':[1.2, 1.45], 'M':[1.4, 1.55]}, 'L':{'L':2.5, 'N':2.9, 'M':3.3}, 'court':{'L':0.1, 'N':0.26, 'M':0.5}},
            '1206':{'chip':[3.4, 1.8, 1.35], 'pad':{'L':[1.1, 1.7], 'N':[1.3, 1.8], 'M':[1.5, 1.9]}, 'L':{'L':3.7, 'N':4.1, 'M':4.5}, 'court':{'L':0.1, 'N':0.26, 'M':0.5}},
            '1210':{'chip':[3.4, 2.7, 1.35], 'pad':{'L':[1.1, 2.6], 'N':[1.3, 2.7], 'M':[1.5, 2.8]}, 'L':{'L':3.7, 'N':4.1, 'M':4.5}, 'court':{'L':0.1, 'N':0.26, 'M':0.5}},
            '2010':{'chip':[5.15, 2.65, 0.71], 'pad':{'L':[1.1, 2.55], 'N':[1.3, 2.65], 'M':[1.5, 2.8]}, 'L':{'L':5.45, 'N':5.85, 'M':6.3}, 'court':{'L':0.1, 'N':0.26, 'M':0.5}},
            '2512':{'chip':[6.45, 3.35, 0.71], 'pad':{'L':[1.1, 3.25], 'N':[1.3, 3.35], 'M':[1.5, 3.5]}, 'L':{'L':6.75, 'N':7.15, 'M':7.6}, 'court':{'L':0.1, 'N':0.26, 'M':0.5}}
            }
        originMarkSize = min(defaults.originMarkSize, dimensions[size]["chip"][1]*0.3)
        super().__init__(name, alternativeLibName, originMarkSize=originMarkSize)
        # pads
        x1=(dimensions[size]["L"][density] - dimensions[size]["pad"][density][0])/2
        for x in [-1,1]:
            self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=[x1*x,0],\
                dimensions=dimensions[size]["pad"][density], name="1" if x<0 else "2"))
        # body
        self.addSimple3Dbody([0,0], dimensions[size]["chip"], file="cube_orange")
        # courtyard and silk
        [dim1, dim2]=self.addCourtyardAndSilk([dimensions[size]["L"][density],\
            max(dimensions[size]["pad"][density][1],dimensions[size]["chip"][1])],\
            dimensions[size]["court"][density])
        # name, value
        y = self.valueObject.height + dim1[1]/2
        self.valueObject.position = [0, -y]
        self.nameObject.position = [0, y]
   
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
        height={'0402':0.6, '0603':0.7}
        pitch = {'0402': 0.5, '0603': 0.8}
        padSize1 = {'0402':{'L':[0.25, 0.45], 'N':[0.3, 0.6], 'M':[0.3, 0.7]},\
            '0603':{'L':[0.55, 0.7], 'N':[0.55, 0.8], 'M':[0.6, 1]}}
        padSize2 = {'0402':{'L':[0.4, 0.45], 'N':[0.45, 0.6], 'M':[0.45, 0.7]},\
            '0603':{'L':[0.8, 0.7], 'N':[0.8, 0.8], 'M':[0.85, 1]}}
        padSpan = {'0402':{'L':0.65, 'N':0.8, 'M':0.9},'0603':{'L':1.35, 'N':1.45, 'M':1.65}}
        court = {'0402':{'L':0.1, 'N':0.15, 'M':0.2},'0603':{'L':0.1, 'N':0.26, 'M':0.5}}
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
        self.addSimple3Dbody([0,0], [chipSize[size][0],chipSize[size][1]-2*leadSize[size][1],height[size]])
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
                self.addSimple3Dbody([(x1-pitch[size]*x+offset)*y, y*y1],lead + [height[size]], file="cube_metal")
        # courtyard and silkscreen
        [dim1, dim2]=self.addCourtyardAndSilk([max((rCount-1)*pitch[size]+2*padSize2[size][density][0]-\
            padSize1[size][density][0], chipSize[size][0]), max(padSpan[size][density]+\
            padSize1[size][density][1], chipSize[size][1])], court[size][density])
        # name, value
        y = self.valueObject.height + dim2[1]/2
        self.valueObject.position = [0, -y]
        self.nameObject.position = [0, y]
            