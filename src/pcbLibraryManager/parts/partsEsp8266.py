# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:29:13 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.part import part
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults
from footprints.footprintSmdDualRow import footprintSmdDualRow
from libraries.libraryPinheaders import footprintPinheader

class symbolEsp01(symbolIC):
    """ESP-01 WiFi module
    """
    def __init__(self, name):
        pinsLeft=[
['VCC', 2, pinType.pwrIn],
None, None, None,
['CH_PD', 6, pinType.input],
['GND', 7, pinType.pwrIn]
        ]
        pinsRight=[
['RxD', 1, pinType.input],
['TxD', 8, pinType.output],
None,
['GPIO0/BOOT', 3, pinType.IO],
['GPIO2', 5, pinType.IO],
['GPIO16', 4, pinType.IO],
        ]
        super().__init__(name, pinsLeft, pinsRight, width=1200)

class partEsp01(part):
    """ESP-01 WiFi module 
    """
    def __init__(self):
        name="ESP-01"
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolEsp01(name))
        for socket in [True, False]:
            for density in ["N", "L", "M"]:
                self.footprints.append(footprintEsp01(density = density, socket=socket,\
                    alternativeLibName = "niceModules"))

class symbolEsp07(symbolIC):
    """ESP-07 WiFi module
    """
    def __init__(self, name):
        pinsLeft=[
['TxD', 8, pinType.output],
['RxD', 7, pinType.input],
['GPIO4', 6, pinType.IO],
['GPIO5', 5, pinType.IO],
['GPIO0/BOOT', 4, pinType.IO],
['GPIO2', 3, pinType.IO],
['GPIO15', 2, pinType.IO],
['GND', 1, pinType.pwrIn]
        ]
        pinsRight=[
['REST', 9, pinType.input],
['ADC', 10, pinType.input],
['CH_PD', 11, pinType.input],
['GPIO16', 12, pinType.IO],
['GPIO14', 13, pinType.IO],
['GPIO12', 14, pinType.IO],
['GPIO13', 15, pinType.IO],
['VCC', 16, pinType.pwrIn],
        ]
        super().__init__(name, pinsLeft, pinsRight, width=1200)

class partEsp07(part):
    """ESP-07 WiFi module 
    """
    def __init__(self):
        name="ESP-07"
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolEsp07(name))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintEsp07(name+"_" + density, \
                density = density, alternativeLibName = "niceModules"))

class footprintEsp01(footprintPinheader):
    """ESP-01 WiFi module
    """
    def __init__(self, density, alternativeLibName, socket=False, name=""):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            name="ESP-01_%s%s" %(density,"_socket" if socket else "")
        h=2.5+8.5*socket
        super().__init__(2, 4, density, name, alternativeLibName,\
            pinLength=8.5+8.5*socket, bodyHeight=h)
        # body
        self.addSimple3Dbody([-9.7,0,h], [25,14.5,1], file="cube_green")
        self.addSimple3Dbody([-8.5,-1.8,h+1], [5,5,1], draw=False)
        self.addSimple3Dbody([-8.5,4.2,h+1], [4,5,1.4], draw=False)
        

class footprintEsp07(footprintSmdDualRow):
    """ESP-07 WiFi module
    """
    def __init__(self, name, density, alternativeLibName):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        # pads
        padSizes={"L":[1.1, 1.6], "N":[1.2, 2.0], "M":[1.3, 2.2]}
        padSpan={"L":15.6, "N":16.0, "M":16.2}
        super().__init__( name, alternativeLibName=alternativeLibName, pinCount=16, pitch=2,\
            padSpan=padSpan[density], padDimensions=padSizes[density], bodyDimensions=[22.0, 16.0, 1.0],\
            padOffset = [-2, 0], originMarkSize=defaults.originMarkSize, bodyStyle="cube_green")
        self.nameObject.position=[-12.5, 0]
        self.nameObject.rotation=270
        self.valueObject.position=[9,0]
        self.valueObject.rotation=270
        # body
        self.addSimple3Dbody([-1.25,0,1], [15.3, 12.3, 2.5], file="cube_metal")
        self.addSimple3Dbody([9.5,-2,1], [2,9,1], file="cube_metal")
        # silk
        silkX = 11.2
        silkY = 8.2
        for x in [-1, 1]:
            self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
                silkX*x, silkY, silkX*x, -silkY))
            for y in [-1, 1]:
                self.primitives.append(pcbLine(pcbLayer.topSilk, defaults.silkWidth,\
                    silkX*x, silkY*y, (silkX-3)*x-2, silkY*y))
        # TODO: courtyard
