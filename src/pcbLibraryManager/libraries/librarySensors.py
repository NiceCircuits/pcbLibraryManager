# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:23:46 2016

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
from libraries.libraryRLC import *
from footprints.footprintSmdDualRow import *
from symbols.symbolsIC import *

class librarySensors(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSensors")
        for v in ["V","H"]:
            self.parts.append(partThermistor(variant=v))
        self.parts.append(partMAG3110())

class partThermistor(part):
    """
    Thermistor part
    """
    def __init__(self, variant="V"):
        name="Thermistor_%s"%variant
        super().__init__(name, "Th")
        self.symbols.append(symbolThermistor(name, variant=variant))
        for size in ["0603", "0805"]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintSmdChip(\
                    size = size, density = density,body="R"))

class partMAG3110(part):
    """
    MAG3110  Three-Axis, Digital Magnetometer part
    """
    def __init__(self):
        name="MAG3110"
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolMAG3110(name))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintFreescaleDfnCol10(density))
    
class symbolThermistor(symbolR):
    """
    Thermistor symbol
    """
    def __init__(self, name, refDes="Th", variant="V", pinNumbers=[1,2]):
        super().__init__(name, refDes, pinNumbers=pinNumbers, variant=variant)
        points=[[80,-60],[-80,60],[-120,60]]
        if variant=="V":
            points=rotatePoints(points,90)
        self.primitives.append(symbolPolyline(defaults.symbolLineWidth,points))

class symbolMAG3110(symbolIC):
    """
    MAG3110  Three-Axis, Digital Magnetometer symbol
    """
    def __init__(self, name):
        pinsLeft = [
['VDD', 2, pinType.pwrIn],
['Cap-A', 1, pinType.passive],
['Cap-A', 4, pinType.passive],
None,
None,
['GND', 5, pinType.pwrIn],
['GND', 10, pinType.pwrIn]
        ]
        pinsRight = [
['VDDIO', 8, pinType.pwrIn],
None,
None,
None,
['SCL', 7,  pinType.input],
['SDA', 6,  pinType.IO],
['INT1', 9,  pinType.output]
        ]
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=1000)

class footprintFreescaleDfnCol10(footprintSmdDualRow):
    """
    Freescale DFN_COL 10pin
    """
    def __init__(self, density):
        name="Freescale_DFN-COL-10_%s"%density
        padLen={"L":0.6,"N":0.6,"M":0.8}
        super().__init__(name, alternativeLibName="niceSemiconductors",\
            pinCount=10, pitch=0.4, padSpan=1.8,padDimensions=[0.225,padLen[density]],\
            bodyDimensions=[2.2,2.2,0.9],leadDimensions=[0.01,0.25,0.2],\
            court = defaults.court[density], leadStyle="cube_metal")


if __name__ == "__main__":
    # generate libraries
    generateLibraries([librarySensors()])