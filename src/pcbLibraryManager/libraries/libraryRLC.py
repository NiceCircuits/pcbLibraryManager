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
from libraryManager.generateLibraries import generateLibraries

class libraryRLC(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceRLC")
        for v in ["H", "V"]:
            self.parts.append(partR(variant=v))
        self.parts.append(partC())
        self.parts.append(partCPolar())
        self.parts.append(partResistorNetwork())

class partR(part):
    """Resistor part
    """
    def __init__(self, variant="H"):
        if variant=="H":
            name="R"
        else:
            name="R_%s" % variant
        super().__init__(name, "R")
        self.symbols.append(symbolR(name,variant=variant))
        for size in ["0603", "0402", "0805", "1206", "1210", "2010", "2512"]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSmdChip(size + "_" + density, \
                    size = size, density = density, alternativeLibName = "niceRLC"))

class partC(part):
    """Capacitor part
    """
    def __init__(self):
        super().__init__("C", "C")
        self.symbols.append(symbolC("C"))
        for size in ["0603", "0402", "0805", "1206", "1210", "2010", "2512"]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSmdChip(size + "_" + density, \
                    size = size, density = density, alternativeLibName = "niceRLC"))

class partCPolar(part):
    """Polarized capacitor part
    """
    def __init__(self):
        super().__init__("Cpol", "C")
        self.symbols.append(symbolC("Cpol", polar=True))
        for density in ["N", "L", "M"]:
            for size in ['Tantal_A', 'Tantal_B', 'Tantal_C', 'Tantal_D', 'Tantal_E', 'Tantal_X']:
                self.footprints.append(footprintSmdChip(size + "_" + density,\
                    size, density, alternativeLibName = "niceRLC"))
            for [D, heights] in [[4,[5,7]],[5,[5,7,11,12,15]], [6.3,[5,7,11,12]],\
            [8,[7,11.5,12,15,20]], [10,[12.5,16,20,25,31.5,35,40]], [12.5,[20,25,30,31.5,35,40,45,50]],\
            [16,[20,25,30,31.5,35.5,40]], [18,[20,25,31.5,35.5,40]], [20,[40]], [22,[40,50]],\
            [25,[50]]]:
                for H in heights:
                    for variant in ["V","HR","HL"]:
                        self.footprints.append(footprintCapElecTht(D, H, density,\
                            variant=variant))

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
    """
    Resistor symbol
    variant = H(orizontal), V(ertical)
    """
    def __init__(self, name, refDes="R", variant="H", showPinNames=False, showPinNumbers=False, pinNumbers=[1,2]):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        for i in range(2):
            self.pins.append(symbolPin(i+1, pinNumbers[i], [200 if i else -200,0],\
                100, pinType.passive, rotation=180 if i else 0))
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
            position=[0,0], dimensions=[200, 80]))
        if variant=="H":
            self.nameObject.position=[0, 80]
            self.valueObject.position=[0, 0]
        elif variant=="V":
            self.movePrimitives([0,0],90)
            self.nameObject.position=[60, 40]
            self.nameObject.align=textAlign.centerLeft
            self.valueObject.position=[60, -40]
            self.valueObject.align=textAlign.centerLeft
        else:
            raise ValueError("Invalid variant %s" % variant)    
        self.valueObject.height = defaults.symbolSmallTextHeight

class symbolC(symbol):
    """Capacitor symbol
    """
    def __init__(self, name, refDes="C", showPinNames=False, showPinNumbers=False,\
    pinNumbers=[1,2], polar=False):
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
        if polar:
            self.primitives.append(symbolLine(defaults.symbolLineWidth, -50, 100, -50, 50))
            self.primitives.append(symbolLine(defaults.symbolLineWidth, -75, 75, -25, 75))

class footprintSmdChip(footprint):
    """Chip component (0603, 0805, SMA, SMB etc.)
    """
    def __init__(self, name, size, density, alternativeLibName="niceRLC"):
        """
        size: "0402", "0603", "0805", "1206", "1210", "2010", "2512",
            "SMA", "SMB", "SMC", 'Tantal_A', 'Tantal_B', 'Tantal_C', 'Tantal_D',
            'Tantal_E', 'Tantal_X'
        density: "L" - least, "N" - nominal, "M" - most
        """
        # TODO: 0603 etc. in R, L, and D versions
        chipSize = {'0402':[1.1, 0.6, 0.6],
            '0603':[1.75, 0.95, 0.85],
            '0805':[2.2, 1.45, 1.1],
            '1206':[3.4, 1.8, 1.35],
            '1210':[3.4, 2.7, 1.35],
            '2010':[5.15, 2.65, 0.71],
            '2512':[6.45, 3.35, 0.71],
            'SMA':[4.6, 2.92, 2.4],
            'SMB':[4.57, 3.94, 2.5],
            'SMC':[7.11, 6.22, 2.5],
            'Tantal_A':[3, 1.8, 1.8],
            'Tantal_B':[3.5, 3, 2.1],
            'Tantal_C':[6.1, 3.5, 2.8],
            'Tantal_D':[7.4, 4.6, 3.1],
            'Tantal_E':[7.4, 6.3, 3.8],
            'Tantal_X':[7.4, 4.6, 4.3]}
        leadSize = {'0402':0.3,
            '0603':0.5,
            '0805':0.75,
            '1206':0.75,
            '1210':0.75,
            '2010':0.85,
            '2512':0.85,
            'SMA':[0.5, 1.63, 1.2],
            'SMB':[0.5, 2.21, 1.25],
            'SMC':[0.5, 3.18, 1.25],
            'Tantal_A':[0.2, 1.3, 0.9],
            'Tantal_B':[0.2, 2.3, 1.05],
            'Tantal_C':[0.2, 2.3, 1.4],
            'Tantal_D':[0.2, 2.5, 1.55],
            'Tantal_E':[0.2, 4.2, 1.9],
            'Tantal_X':[0.2, 2.5, 4.15]}
        padSize = {'0402':{'L':[0.4, 0.6], 'N':[0.5, 0.65], 'M':[0.6, 0.75]},
            '0603':{'L':[0.8, 0.85], 'N':[1, 0.95], 'M':[1.2, 1.1]},  
            '0805':{'L':[1, 1.35], 'N':[1.2, 1.45], 'M':[1.4, 1.55]}, 
            '1206':{'L':[1.1, 1.7], 'N':[1.3, 1.8], 'M':[1.5, 1.9]},  
            '1210':{'L':[1.1, 2.6], 'N':[1.3, 2.7], 'M':[1.5, 2.8]},  
            '2010':{'L':[1.1, 2.55], 'N':[1.3, 2.65], 'M':[1.5, 2.8]},
            '2512':{'L':[1.1, 3.25], 'N':[1.3, 3.35], 'M':[1.5, 3.5]},
            'SMA':{'L':[2, 1.45], 'N':[2.1, 1.55], 'M':[2.3, 1.85]},
            'SMB':{'L':[1.9, 2], 'N':[2.1, 2.15], 'M':[2.3, 2.45]},
            'SMC':{'L':[1.8, 3], 'N':[1.9, 3.1], 'M':[2.1, 3.4]},
            'Tantal_A':{'L':[1.4, 1.1], 'N':[1.5, 1.25], 'M':[1.6, 1.55]},
            'Tantal_B':{'L':[1.4, 2.1], 'N':[1.5, 2.25], 'M':[1.6, 2.55]},
            'Tantal_C':{'L':[2.0, 2.1], 'N':[2.1, 2.25], 'M':[2.2, 2.55]},
            'Tantal_D':{'L':[2.0, 2.3], 'N':[2.1, 2.45], 'M':[2.2, 2.75]},
            'Tantal_E':{'L':[2.0, 4.0], 'N':[2.1, 4.15], 'M':[2.2, 4.45]},
            'Tantal_X':{'L':[2.0, 2.3], 'N':[2.1, 2.45], 'M':[2.2, 2.75]}}
        L = {'0402':{'L':1.1, 'N':1.35, 'M':1.55},
            '0603':{'L':2.05, 'N':2.45, 'M':2.9},
            '0805':{'L':2.5, 'N':2.9, 'M':3.3},  
            '1206':{'L':3.7, 'N':4.1, 'M':4.5},  
            '1210':{'L':3.7, 'N':4.1, 'M':4.5},  
            '2010':{'L':5.45, 'N':5.85, 'M':6.3},
            '2512':{'L':6.75, 'N':7.15, 'M':7.6},
            'SMA': {'L':5.75, 'N':5.9, 'M':6.1},
            'SMB': {'L':5.75, 'N':5.9, 'M':6.1},
            'SMC': {'L':8.3, 'N':8.45, 'M':8.65},
            'Tantal_A':{'L':3.55, 'N':3.7, 'M':3.9},
            'Tantal_B':{'L':3.85, 'N':4.0, 'M':4.2},
            'Tantal_C':{'L':6.45, 'N':6.6, 'M':6.8},
            'Tantal_D':{'L':7.75, 'N':7.9, 'M':8.1},
            'Tantal_E':{'L':7.75, 'N':7.9, 'M':8.1},
            'Tantal_X':{'L':7.75, 'N':7.9, 'M':8.1}}
        court = {'0402':defaults.courtSmall,
            '0603':defaults.court,
            '0805':defaults.court,
            '1206':defaults.court,
            '1210':defaults.court,
            '2010':defaults.court,
            '2512':defaults.court,
            'SMA':defaults.court,
            'SMB':defaults.court,
            'SMC':defaults.court,
            'Tantal_A':defaults.court,
            'Tantal_B':defaults.court,
            'Tantal_C':defaults.court,
            'Tantal_D':defaults.court,
            'Tantal_E':defaults.court,
            'Tantal_X':defaults.court}
        originMarkSize = min(defaults.originMarkSize, chipSize[size][1]*0.3)
        super().__init__(name, alternativeLibName, originMarkSize=originMarkSize)
        polar=False
        bodyStyle="cube_orange"
        if size in ["SMA", "SMB", "SMC"]:
            polar=True
            bodyStyle="cube"
        elif size in ['Tantal_A', 'Tantal_B', 'Tantal_C', 'Tantal_D', 'Tantal_E', 'Tantal_X']:
            polar=True
        # pads
        x1=(L[size][density] - padSize[size][density][0])/2
        b =[x for x in chipSize[size]]
        if isIterable(leadSize[size]):
            x2=(b[0]+leadSize[size][0])/2
            lead=leadSize[size]
        else:
            x2=(b[0]-leadSize[size])/2
            b[0]-=2*leadSize[size]
            lead =[x for x in chipSize[size]]
            lead[0]=leadSize[size]
        for x in [-1,1]:
            self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=[x1*x,0],\
                dimensions=padSize[size][density], name="1" if x<0 else "2"))
            self.addLead([x2*x, 0], lead, lead="cube_metal")
        # body
        self.addSimple3Dbody([0,0], b, file=bodyStyle)
        [dim1, dim2]=self.addCourtyardAndSilk([L[size][density],\
            max(padSize[size][density][1],chipSize[size][1])],\
            court[size][density], silk=not polar)
        if polar:
            dim = [chipSize[size][0]/10, chipSize[size][1], 0.05]
            pos = [-chipSize[size][0]*0.35, 0, chipSize[size][2]]
            self.addSimple3Dbody(pos,dim,file="cube_metal")
            if density!="L":
                for y in [-1,1]:
                    self.primitives.append(pcbPolyline(pcbLayer.topSilk, defaults.silkWidth,\
                        [[0, y*(chipSize[size][1]+defaults.silkWidth)/2],\
                        [-(chipSize[size][0]+defaults.silkWidth)/2,\
                        y*(chipSize[size][1]+defaults.silkWidth)/2],
                        [-(chipSize[size][0]+defaults.silkWidth)/2,\
                        y*((padSize[size][density][1]+defaults.silkWidth)/2+defaults.silkExtend)]]))
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
            
class footprintCapElecTht(footprint):
    """Electrolytic THT capacitor
    :param D: body diameter: 4, 5, 6.3, 8, 10, 12.5, 16, 18, 20, 22, 25
    :param variant: "V" (horizontal), "HL","HR" (rorizontal left/right)
    """
    def __init__(self, D, H, density="N", pitch=0, variant="V", name="", dPin=0):
        pitches={4:1.5, 5:2, 6.3:2.5, 8:3.5, 10:5, 12.5:5, 16:7.5, 18:7.5, 20:10, 22:10, 25:12.5}
        diameters={4:0.45, 5:0.5, 6.3:0.5, 8:0.6, 10:0.6, 12.5:0.8, 16:0.8, 18:0.8, 20:1, 22:1, 25:1}
        ring={"L":0.3, "N":0.4, "M":0.7}
        if pitch:
            pitchText="_%1.1f" % pitch
        else:
            pitchText=""
            pitch = pitches[D]
        if not dPin:
            dPin = diameters[D]
        if not name:
            name="Cpol_%1.1f_%1.1f%s_%s_%s" % (D, H, pitchText, variant, density)
        super().__init__(name, "niceRLC", originMarkSize=defaults.originMarkSize)
        #tolerance
        D+=0.5
        H+=(1.5 if H<=20 else 2)
        # pins
        dPadY= dPin+2*ring[density]
        dPadX=min(dPadY, pitch-mil(10))
        if variant != "V":
            zOffset=D/2
            bodyOffset=dPadY/2+0.3
            if variant=="HR":
                side=1
            elif variant=="HL":
                side=-1
            else:
                raise ValueError("invalid variant %s" % variant)
            rotation=[90*side,0,0]
        else:
            side=0
            zOffset=0
            bodyOffset=0
            rotation=[0,0,0]
        for i in [-1, 1]:
            #pad
            self.primitives.append(pcbThtPad([pitch/2*i, 0], [dPadX, dPadY],\
                dPin+0.2, 1 if i<0 else 2, padShape.rect if i<0 else padShape.roundRect))
            #pin
            self.addCylinder3Dbody([pitch/2*i, 0, -2.5], [dPin, dPin, 2.5+zOffset],\
                file="cylinder_metal")
            if side!=0:
                #horizontal pin part
                self.addCylinder3Dbody([pitch/2*i, -dPin/2*side, zOffset],\
                    [dPin, dPin, dPin/2+bodyOffset], file="cylinder_metal", rotation=rotation)
        # body
        self.addCylinder3Dbody([0,bodyOffset*side,zOffset], [D,D,H], silk=True, \
            file="cylinder_blue", rotation=rotation)
        if side==0:
            self.primitives.append(pcbCircle(pcbLayer.topCourtyard, defaults.documentationWidth,\
                [0,0],D/2+defaults.courtTht[density]))
            # minus terminal mark
            for i in range(-2,3):
                self.primitives.append(pcbArc(pcbLayer.topSilk, defaults.silkWidth,\
                    [0,0], D/2-i*defaults.silkWidth*0.9, [-80,80]))
            # "+" sign
            self.addPlus(-D/2-1.2, 1, 2)
        else:
            y=(H/2)*side
            hC=H+2*bodyOffset
            self.addCourtyardAndSilk([D,hC], defaults.court[density], silk=False,\
                offset=[0,y])
            # minus terminal mark
            for i in range(1,8):
                x=D/2-defaults.silkWidth*i*0.9
                self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
                    x, bodyOffset*side, x, (bodyOffset+H)*side))
            # "+" sign
            self.addPlus(-pitch/2-1.5-dPadX/2, (bodyOffset-1.5)*side, 2)
            self.nameObject.position=[0,(bodyOffset+2)*side+1]
            self.valueObject.position=[0,(bodyOffset+2)*side]

    def addPlus(self,x,y,l):
        self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
            x-l/2, y, x+l/2, y))
        self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
            x, y-l/2, x, y+l/2))
        

if __name__ == "__main__":
    generateLibraries([libraryRLC()])