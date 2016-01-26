# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 22:37:59 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.part import part
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults
from footprints.footprintSmdDualRow import footprintSoic
from libraries.libraryPinheaders import footprintPinheader
from libraries.libraryRLC import footprintSmdChip

class partOled128x64(part):
    """
    128x64 OLED module
    """
    def __init__(self, mount=False):
        if mount:
            mntString="_M"
        else:
            mntString=""
        name="Oled128x64%s" %(mntString)
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolOled128x64(name,mount=mount))
        for h in [2.54, 5.08]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintOled128x64(density = density,\
                    alternativeLibName = "niceModules", h=h,mount=mount))

class symbolOled128x64(symbolIC):
    """
    128x64 OLED module
    """
    def __init__(self, name="", mount=False):
        if mount:
            mntString="_M"
        else:
            mntString=""
        if not name:
            name="Oled128x64%s" %(mntString)
        pinsLeft=[
['VCC', 2, pinType.pwrIn],
['SDA', 7, pinType.IO],
['SCL', 6, pinType.input],
['GND', 5, pinType.pwrIn],
None
        ]
        if mount:
            pinsLeft[4]=['MNT', 0, pinType.passive]
        pinsRight=[
        ]
        super().__init__(name, pinsLeft, pinsRight, width=600)

class footprintOled128x64(footprintPinheader):
    """
    128x64 OLED module
    """
    def __init__(self, density, alternativeLibName, h=2.54, name="", mount=False):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if mount:
            mntString="_M"
        else:
            mntString=""
        if not name:
            name="Oled128x64%s_%1.2f%s" %( mntString,h, density)
        super().__init__(1, 4, density, name, alternativeLibName, pinLength=h+6,\
            bodyHeight=h)
        self.movePrimitives([0,12.1],90)
        # body
        self.addSimple3Dbody([0,0,h], [27.8,27.8,1], file="cube_green")
        self.addSimple3Dbody([0,0,h+1], [27,19.5,1.3])
        self.addCourtyardAndSilk([27.8,27.8], defaults.court[density])
        for x in [-1,1]:
            for y in [-1,1]:
                self.addCylinder3Dbody([23.3/2*x,23.7/2*y,h-0.05], [3.5, 3.5, 1.1],\
                    file="cylinder_metal", draw=False)
            if mount:
                self.primitives.append(pcbThtPad([23.3/2*x,-23.7/2], [5,5], 2.5, "0"))
        # transplant some parts - for fun and profit
        for y in [-13,-11,-7,-5,-1,1,3,5,7,9,11,13]:
            donor=footprintSmdChip("","0603","N","")
            donor.movePrimitives([0.87*y,-0.1, h],[0,180,90])
            self.primitives.extend(donor.get3DBody())
        