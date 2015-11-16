# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 06:59:51 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from libraryManager.common import *
from libraryManager.symbolPrimitive import *
from libraryManager.symbol import symbol
from libraryManager.footprint import footprint
from math import sqrt

class libraryMechanical(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceMechanical")
        self.parts.append(partDummy())
        self.parts.append(partMountingHole(plated=True))
        for size in [2, 2.5, 3, 3.5, 4, 5, 6]:
            for din in [934, 439, 985]:
                pl=[False] if din==985 else [False, True]
                for plastic in pl:
                    self.parts.append(partNut(size, din, plastic))
        for [size, lengths] in [[2,[3,4,5,6,8,10,12,14,16,18,20]],\
        [2.5,[3,4,5,6,8,10,12,14,16,18,20]],\
        [3,[3,4,5,6,8,10,12,14,16,18,20,22,25,30,35,40]],\
        [3.5,[3,4,5,6,8,10,12,14,16,18,20,22,25,30,35,40]],\
        [4,[4,5,6,8,10,12,14,16,18,20,22,25,30,35,40]],\
        [5,[6,8,10,12,14,16,18,20,22,25,30,35,40]],\
        [6,[6,8,10,12,14,16,18,20,22,25,30,35,40]]]:
            for l in lengths:
                for din in [7985, 912]:
                    pl=[False] if din==912 else [False, True]
                    for plastic in pl:
                        self.parts.append(partScrew(size, l, din, plastic))
        for [size, lengths, lengthExts] in [[2,[2,3,4,5,6,8,10,12,14,15,16,18,20], [0,5]],\
        [2.5,[2,3,4,5,6,8,10,12,14,15,16,18,20], [0,6]],\
        [3,[2,3,4,5,6,8,10,12,14,15,16,18,20,22,25,30,35,40], [0,6]],\
        [4,[2,3,4,5,6,8,10,12,14,15,16,18,20,22,25,30,35,40], [0,8]],\
        [5,[2,3,4,5,6,8,10,12,14,15,16,18,20,22,25,30,35,40], [0,8]]]:
            for l in lengths:
                for threaded in [False, True]:
                    for lengthExt in lengthExts if threaded else [0]:
                        self.parts.append(partSpacer(size, l, lengthExt,\
                            threaded, plastic=not threaded))
        
class partMountingHole(part):
    """Mounting hole part generator
    """
    def __init__(self, plated, name="", refDes=defaults.mountingHoleRefDes):
        """:param plated: bool - generate copper Pad or not
        """
        if not name:
            name = "mounting_hole%s" % ("_plated" if plated else "")
        super().__init__(name, refDes)
        self.symbols.append(symbolMechanical(name, plated, refDes))
        for [drill,diameter] in [[3.2,7.5], [3.2,10]]:
            for vias in [False, True]:
                self.footprints.append(footprintMountingHole(drill, diameter, plated, vias))

class partDummy(part):
    """Dummy mechanical part generator
    """
    def __init__(self, name="", refDes=defaults.mechanicalRefDes):
        """
        """
        if not name:
            name = "dummy_mech"
        super().__init__(name, refDes)
        self.symbols.append(symbolMechanical(name, False, refDes))

class partNut(part):
    """Nut part generator
    """
    def __init__(self, size, din=934, plastic=False, name="", refDes=defaults.mechanicalRefDes):
        """:param size: metric size. 3 - M3 etc.
        :param din: din norm type: 934 - standard, 439 - low profile, 985 - lock nut
        :param plastic: if true, 3D body is black
        """
        if not name:
            name = "nut_M%g_DIN%d%s" % (size, din, "_plastic" if plastic else "")
        super().__init__(name, refDes)
        self.symbols.append(symbolMechanical(name, False, refDes))
        self.footprints.append(footprintNut(size, din, plastic))

class partScrew(part):
    """Screw part generator
    """
    def __init__(self, size, length, din, plastic=False, name="", refDes=defaults.mechanicalRefDes):
        """:param size: metric size. 3 - M3 etc.
        :param length: in mm
        :param din: din norm type: 7985 - standard cylindrical Philips, 912 - standard cylindrical hex socket
        :param plastic: if true, 3D body is black
        """
        if not name:
            name = "screw_M%gx%g_DIN%d%s" % (size, length, din, "_plastic" if plastic else "")
        super().__init__(name, refDes)
        self.symbols.append(symbolMechanical(name, False, refDes))
        self.footprints.append(footprintScrew(size, length, din, plastic))

class partSpacer(part):
    """Spacer part generator
    """
    def __init__(self, size, length, lengthExt=0, threaded=True, plastic=False,\
    name="", refDes=defaults.mechanicalRefDes):
        """:param size: metric size. 3 - M3 etc. or minimal internal diameter
        :param length: in mm
        :param lengthExt: length of external threaded segment - if 0, internal threaded from both sides
        :param threaded: If threaded (hex) or no (cylindrical)
        :param plastic: if true, 3D body is black
        """
        if not name:
            if lengthExt:
                extStr = "+%g" % lengthExt
            else:
                extStr = ""
            name = "spacer_%s%gx%g%s%s" % ("M" if threaded else "", size, length,\
                extStr, "_plastic" if plastic else "")
        super().__init__(name, refDes)
        self.symbols.append(symbolMechanical(name, False, refDes))
        self.footprints.append(footprintSpacer(size, length, lengthExt, threaded, plastic))

class symbolMechanical(symbol):
    """Mechanical element symbol
    """
    def __init__(self, name, plated, refDes):
        super().__init__(name, refDes, False, False)
        self.primitives.append(symbolRectangle(defaults.symbolLineWidth,\
            position=[0,0], dimensions=[400,100], filled=fillType.background))
        if plated:
            self.pins.append(symbolPin("1",1,[0,-100],50,pinType.passive,90))

class footprintMountingHole(footprint):
    """Mounting hole footprint
    """
    def __init__(self, drill, diameter, plated=False, vias=False, name="",\
        alternativeLibName="niceMechanical"):
        if not name:
            name = "mounting_hole_%1.1f_%1.1f%s%s" % (drill, diameter,\
                "_plated" if plated else "","_vias" if vias else "")
        super().__init__(name, alternativeLibName)
        if plated:
            self.primitives.append(pcbThtPad([0,0], [diameter,diameter], drill,\
                "1", padShape.round))
            if vias and ((diameter-drill)/2)>=defaults.viaDiam:
                for rot in range(8):
                    pos = rotatePoints([[(diameter+drill)/4, 0]], 45*rot)[0]
                    self.primitives.append(pcbThtPad(pos, [defaults.viaDiam,defaults.viaDiam],\
                        defaults.viaDrill, "1", padShape.round))
        else:
            pass             #TODO:

class footprintNut(footprint):
    """Nut footprint
    """
    def __init__(self, size, din, plastic=False, name="", alternativeLibName="niceMechanical"):
        if not name:
            name = "nut_M%g_DIN%d%s" % (size, din, "_plastic" if plastic else "")
        super().__init__(name, alternativeLibName)
        hexSizes={2:4, 2.5:5, 3:5.5, 3.5:6, 4:7, 5:8, 6:10}
        h={2:{934:1.6, 439:1.2, 985:1.6},\
            2.5:{934:2, 439:1.6, 985:2},\
            3:{934:2.4, 439:1.8, 985:2.4},\
            3.5:{934:2.8, 439:2, 985:2.6},\
            4:{934:3.2, 439:2.2, 985:2.9},\
            5:{934:4, 439:2.7, 985:3.2},\
            6:{934:5, 439:3.2, 985:4}}
        h985={2:2.5, 2.5:3.8, 3:4, 3.5:4.5, 4:5, 5:5, 6:6}
        hexSize = hexSizes[size]
        if size==2 and din==985: # one exception
            hexSize = 4.5
        hexBody="hex" if plastic else "hex_metal"
        self.addSimple3Dbody([0,0], [hexSize, hexSize, h[size][din]],\
            draw=False, file=hexBody)
        if din==985:
            cylinderBody="cylinder" if plastic else "cylinder_metal"
            self.addSimple3Dbody([0,0], [hexSize, hexSize, h985[size]],\
                draw=False, file=cylinderBody)
        self.primitives.append(pcbCircle(pcbLayer.topAssembly, defaults.documentationWidth,\
            [0,0], hexSize/sqrt(3)))
            
class footprintScrew(footprint):
    """Screw footprint
    """
    def __init__(self, size, length, din, plastic=False, name="", alternativeLibName="niceMechanical"):
        if not name:
            name = "screw_M%gx%g_DIN%d%s" % (size, length, din, "_plastic" if plastic else "")
        super().__init__(name, alternativeLibName)
        headDiam={2:{7985:4, 912:3.8},\
            2.5:{7985:5, 912:4.5},\
            3:{7985:6, 912:5.5},\
            3.5:{7985:7, 912:6.5},\
            4:{7985:8, 912:7},\
            5:{7985:10, 912:8.5},\
            6:{7985:12, 912:10}}
        h={2:{7985:1.72, 912:2},\
            2.5:{7985:2.12, 912:2.5},\
            3:{7985:2.52, 912:3},\
            3.5:{7985:2.82, 912:3.5},\
            4:{7985:3.25, 912:4},\
            5:{7985:3.95, 912:5},\
            6:{7985:4.75, 912:6}}
        cylinderBody="cylinder" if plastic else "cylinder_metal"
        self.addCylinder3Dbody([0,0,0], [headDiam[size][din], headDiam[size][din], h[size][din]],\
            draw=True, file=cylinderBody)
        self.addCylinder3Dbody([0,0,-length], [size, size, length],\
            draw=False, file=cylinderBody)
            
class footprintSpacer(footprint):
    """Spacer footprint
    """
    def __init__(self, size, length, lengthExt=0, threaded=True, plastic=False,\
    name="", alternativeLibName="niceMechanical"):
        if not name:
            if lengthExt:
                extStr = "+%g" % lengthExt
            else:
                extStr = ""
            name = "spacer_%s%gx%g%s%s" % ("M" if threaded else "", size, length,\
                extStr, "_plastic" if plastic else "")
        super().__init__(name, alternativeLibName)
        hexSizes={2:4, 2.5:5, 3:5.5, 4:7, 5:8}
        cylinderSizes={2:4, 2.5:5, 3:6, 4:8, 5:10}
        hexBody="hex" if plastic else "hex_metal"
        cylinderBody="cylinder" if plastic else "cylinder_metal"
        if threaded:
            self.addSimple3Dbody([0,0,0], [hexSizes[size], hexSizes[size], length],\
                draw=False, file=hexBody)
            self.primitives.append(pcbCircle(pcbLayer.topAssembly, defaults.documentationWidth,\
                [0,0], hexSizes[size]/sqrt(3)))
        else:
            self.addCylinder3Dbody([0,0,0], [cylinderSizes[size], cylinderSizes[size], length],\
                draw=True, file=cylinderBody)
        if lengthExt:
            self.addCylinder3Dbody([0,0,-lengthExt], [size, size, lengthExt],\
                draw=False, file=cylinderBody)

