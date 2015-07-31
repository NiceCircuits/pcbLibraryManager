# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:18:41 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.part import part
from libraryManager.symbol import symbol
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults
from symbols.symbolsSwitches import *

class footprintMicroswitchSmt(footprint):
    """
    Default SMT microswitch
    """
    def __init__(self, name, density, alternativeLibName):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        super().__init__( name, alternativeLibName=alternativeLibName,\
            originMarkSize=defaults.originMarkSize)
        # pads
        padSizes={"L":[2.5, 1.4], "N":[2.5, 1.4], "M":[2.5, 1.4]}
        for x in [-4.5, 4.5]:
            for y in [-2.25, 2.25]:
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=[x,y],\
                    dimensions=padSizes[density],name= 1 if y<0 else 2))
        # Name & Value
        self.nameObject.position=[0, 4]
        self.valueObject.position=[0,-4]
        # body
        self.primitives.append(pcbRectangle(pcbLayer.topAssembly,\
            defaults.documentationWidth, position=[0,0], dimensions=[6.0, 6.0]))
        self.primitives.append(pcbCircle(pcbLayer.topAssembly,\
            defaults.documentationWidth, position=[0,0], radius=3.5/2))
        # TODO: silk
            
class partMicroswitchSmt(part):
    """
    Default SMT microswitch
    """
    def __init__(self):
        super().__init__("MicroswitchSmt", defaults.switchRefDes)
        self.symbols.append(symbolButton("Button"))
        for density in ["L", "N", "M"]:
            self.footprints.append(footprintMicroswitchSmt("MicroswitchSmd_" + density, \
                density = density, alternativeLibName = "niceSwitches"))

