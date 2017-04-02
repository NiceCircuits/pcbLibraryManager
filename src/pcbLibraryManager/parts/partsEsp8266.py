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
from footprints.footprintSmdDualRow import footprintSmdDualRow, footprintSoic
from libraries.libraryPinheaders import footprintPinheader
from libraries.libraryRLC import footprintSmdChip

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

class symbolEsp03(symbolIC):
    """ESP-03 WiFi module
    """
    def __init__(self, name):
        pinsLeft=[
['WIFI_ANT', 14, pinType.passive],
None, 
['VCC', 1, pinType.pwrIn],
['CH_PD', 13, pinType.input],
None, 
None, 
None, 
None,
['GND', 8, pinType.pwrIn]
        ]
        pinsRight=[
['RxD', 11, pinType.input],
['TxD', 10, pinType.output],
['GPIO0/BOOT0', 7, pinType.IO],
['GPIO2/BOOT1', 6, pinType.IO],
['GPIO12', 3, pinType.IO],
['GPIO13', 4, pinType.IO],
['GPIO14', 2, pinType.IO],
['GPIO15/BOOT2', 5, pinType.IO],
['GPIO16', 12, pinType.IO],
        ]
        super().__init__(name, pinsLeft, pinsRight, width=1200)

class symbolEsp07(symbolIC):
    """ESP-07 WiFi module
    """
    def __init__(self, name):
        pinsLeft=[
['TxD', 8, pinType.output],
['RxD', 7, pinType.input],
['GPIO5', 6, pinType.IO],
['GPIO4', 5, pinType.IO],
['GPIO0/BOOT', 4, pinType.IO],
['GPIO2/BOOT1', 3, pinType.IO],
['GPIO15/BOOT2', 2, pinType.IO],
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

class partEsp03(part):
    """ESP-03 WiFi module 
    """
    def __init__(self):
        name="ESP-03"
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolEsp03(name))
        for density in ["N", "L", "M", "edge"]:
            self.footprints.append(footprintEsp03(density = density, \
                alternativeLibName = "niceModules"))

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
        
class footprintEsp03(footprintSmdDualRow):
    """ESP-03 WiFi module
    """
    def __init__(self, density, alternativeLibName, name="", ):
        """
        density: "L" - least, "N" - nominal, "M" - most, "edge" - special footprint
        for esp-servo project
        """
        if not name:
            name="ESP-03_%s" %(density)
        # pads
        padSizes={"L":[1.1, 1.6], "N":[1.2, 2.0], "M":[1.3, 2.2], "edge":[1.3, 1]}
        padSpan={"L":11.8, "N":12.2, "M":12.4, "edge":11.2}
        court = {'L':0.2, 'N':0.3, 'M':0.5, "edge":0.3}
        super().__init__( name, alternativeLibName=alternativeLibName, pinCount=14, pitch=2,\
            padSpan=padSpan[density], padDimensions=padSizes[density], bodyDimensions=[17.4, 12.2, 1.0],\
            padOffset = [1.55, 0], originMarkSize=defaults.originMarkSize, bodyStyle="cube_green",\
            firstPinMarker=False, court=court[density], leadDimensions=[1.2, 1.2, 1.02],\
            leadStyle="cube_gold", leadOffset=[0,-1.19,-0.01])
        # ESP8266
        self.addSimple3Dbody([-0.64,-1.25,1], [5, 5, 0.8], file="cube")
        # antenna
        self.addSimple3Dbody([-7.5,0,1], [1.5,10,1], file="cube_metal")
        # quartz
        self.addSimple3Dbody([3,3.4,1], [3.2, 2.5,0.5], file="cube_metal")
        # transplant some parts - for fun and profit
        x=[-4.35, -1.45, -0.6, 6.1]
        y=[3.75, 3.9, 3.9, 3.75]
        for k in range(4):
            donor=footprintSmdChip("0402","N","")
            donor.movePrimitives([x[k],y[k],1], 90)
            self.primitives.extend(donor.get3DBody())
        donor=footprintSmdChip("0603","N","")
        donor.movePrimitives([-5.5, 0, 1], 90)
        self.primitives.extend(donor.get3DBody())
        donor=footprintSoic(8)
        donor.movePrimitives([5.9,-1.5,1])
        self.primitives.extend(donor.get3DBody())

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
        court = {'L':0.2, 'N':0.3, 'M':0.5}
        super().__init__( name, alternativeLibName=alternativeLibName, pinCount=16, pitch=2,\
            padSpan=padSpan[density], padDimensions=padSizes[density], bodyDimensions=[22.0, 16.0, 1.0],\
            padOffset = [-2, 0], originMarkSize=defaults.originMarkSize, bodyStyle="cube_green",\
            firstPinMarker=False, court=court[density])
        # body
        self.addSimple3Dbody([-1.25,0,1], [15.3, 12.3, 2.5], file="cube_metal")
        self.addSimple3Dbody([9.5,-2,1], [2,9,1], file="cube_metal")
        self.addCylinder3Dbody([8.5,6,1], [2,2,1], file="cylinder_metal")
