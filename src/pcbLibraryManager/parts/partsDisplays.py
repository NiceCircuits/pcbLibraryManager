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
['SDA', 4, pinType.IO],
['SCL', 3, pinType.input],
['GND', 1, pinType.pwrIn],
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
            donor=footprintSmdChip("0603","N","")
            donor.movePrimitives([0.87*y,-0.1, h],[0,180,90])
            self.primitives.extend(donor.get3DBody())

class partTFT_1_8_ST7735(part):
    """
    1.8" SPI 128X160 TFT LCD with ST7735 driver
    """
    def __init__(self):
        name="TFT_1_8_ST7735"
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolTFT_1_8_ST7735(name))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintTFT_1_8_ST7735(density = density,\
                alternativeLibName = "niceModules"))

class symbolTFT_1_8_ST7735(symbolIC):
    """
    1.8" SPI 128X160 TFT LCD with ST7735 driver
    """
    def __init__(self, name=""):
        if not name:
            name="TFT_1_8_ST7735"
        pinsLeft=[
['NC', 1, pinType.NC],
['GND', 2, pinType.pwrIn],
['LED-', 3, pinType.passive],
['LED+', 4, pinType.passive],
['GND', 5, pinType.pwrIn],
['/RST', 6, pinType.input],
['A0', 7, pinType.input],
['SDA', 8, pinType.IO],
['SCK', 9, pinType.input],
['VCC', 10, pinType.pwrIn],
['VCCIO', 11, pinType.pwrIn],
['CS', 12, pinType.input],
['GND', 13, pinType.pwrIn],
['NC', 14, pinType.NC]
        ]
        pinsRight=[
        ]
        super().__init__(name, pinsLeft, pinsRight, width=600)

class footprintTFT_1_8_ST7735(footprint):
    """
    1.8" SPI 128X160 TFT LCD with ST7735 driver
    """
    def __init__(self, density, alternativeLibName, name=""):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            name="TFT_1_8_ST7735_%s" %(density)
        super().__init__(name, alternativeLibName)
        # body
        self.addSimple3Dbody([0,0,0.2], [46.9, 34.9, 2.7], file="cube_white")
        self.addSimple3Dbody([1.2,0,1.91], [41.42,31.83,1], file="cube")
        self.addSimple3Dbody([2.59,0,1.92], [35.04,28.03,1], file="cube_metal")
        self.addCourtyardAndSilk([46.9, 34.9], defaults.court[density])
        # flex
        self.addSimple3Dbody([-18.45, 1.2,0], [10, 27.3, 0.1], file="cube_orange")
        # pins
        size={"L":[2.5, 0.45], "N":[3, 0.45], "M":[4, 0.5]}
        x={"L":-14.15, "N":-14, "M":-13.65}
        for y in range(14):
            self.primitives.append(pcbSmtPad(pcbLayer.topCopper, \
                position=[x[density], (y-6.5)*0.8],\
                dimensions=size[density], name=str(y+1)))
        