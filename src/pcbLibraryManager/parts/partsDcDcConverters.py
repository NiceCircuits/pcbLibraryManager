# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 15:02:59 2016

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
from libraries.libraryPowerSupplies import symbolRegulator3Pin
from libraries.libraryRLC import footprintSmdChip

class partDcDcDsun3A(part):
    """
    D-SUN 3A DC-DC module
    """
    def __init__(self):
        name="DcDcDsun3A"
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolRegulator3Pin(name))
        for h in [2.54, 5.08]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintDcDcDsun3A(density = density,\
                    alternativeLibName = "niceModules", h=h))

class footprintDcDcDsun3A(footprint):
    """
    D-SUN 3A DC-DC module
    """
    def __init__(self, density, alternativeLibName, h=2.54, name=""):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            name="DcDcDsun3A_%1.2f%s" %(h, density)
        super().__init__(name, alternativeLibName)
        # pins - transplant some pinheaders
        pinNames=[[1,2],[3,2]]
        for x in [0,1]:
            for y in [0,1]:
                donor = footprintPinheader(1,2,density=density, textOnSilk=False,\
                    pinLength=h+6, bodyHeight=h)
                donor.renamePads([pinNames[x][y]]*2)
                donor.movePrimitives([mil(365)*(x*2-1),mil(210)*(y*2-1)])
                self.primitives.extend(donor.primitives)
        # body
        self.addSimple3Dbody([0,0,h], [mil(870),mil(660),1], file="cube_green")
        self.addSimple3Dbody([mil(140),mil(60),h+1], [7,7,2.8])
        self.addSimple3Dbody([mil(150),mil(-250),h+1], [3.5, 3, 1.9])
        self.addCylinder3Dbody([mil(150),mil(-250),h+2.9], [2.5, 2.5, 0.1], file="cylinder_metal")
        # transplant some parts - for fun and profit
        for x in [-1,1]:
            donor=footprintSmdChip("","1206","N","")
            donor.movePrimitives([mil(365)*x,0,h+1], 90)
            self.primitives.extend(donor.get3DBody())
        for y in range(4):
            donor=footprintSmdChip("","0603","N","")
            donor.movePrimitives([mil(-275), mil(-235)+mil(115)*y, h+1], 90)
            self.primitives.extend(donor.get3DBody())
        for x in range(2):
            donor=footprintSmdChip("","0603","N","")
            donor.movePrimitives([mil(60)+mil(150)*x, mil(-140), h+1])
            self.primitives.extend(donor.get3DBody())
            for y in range(2):
                donor=footprintSmdChip("","0603","N","")
                donor.movePrimitives([mil(-175)+mil(125)*x, mil(-260)+mil(60)*y, h+1])
                self.primitives.extend(donor.get3DBody())
        donor=footprintSoic(8)
        donor.movePrimitives([mil(-140),0,h+1])
        self.primitives.extend(donor.get3DBody())
        donor=footprintSmdChip("","SMA","N","")
        donor.movePrimitives([mil(-155),mil(220),h+1],180)
        self.primitives.extend(donor.get3DBody())
