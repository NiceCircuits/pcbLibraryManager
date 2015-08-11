# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:13:05 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.defaults import defaults
from libraryManager.footprintPrimitive import *

class footprintDPak(footprint):
    """
    D-Pak (TO 252)
    """
    def __init__(self, name="", density="N", alternativeLibName="niceSemiconductors"):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            name = "D-PAK_%s" % density
        super().__init__(name, alternativeLibName)
        bodyDimensions=[6.8, 6.3]
        padSize1 = {"L":[1.5,2.5], "N":[1.5,2.5], "M":[1.5,2.5]}
        padSize2 = {"L":[7.0,7.0], "N":[7.0,7.0], "M":[7.0,7.0]}
        padOffset1 ={"L":-5.1,"N":-5.1,"M":-5.1}
        padOffset2 ={"L":1.8,"N":1.8,"M":1.8}
        padSpan1=4.6
        court = {'L':0.15, 'N':0.26, 'M':0.5}
        # body
        self.primitives.append(pcbRectangle(pcbLayer.topAssembly, defaults.documentationWidth,\
            position=[0,0], dimensions=bodyDimensions))
        # pads
        self.primitives.append(pcbSmtPad(pcbLayer.topCopper,[0, padOffset2[density]],padSize2[density],2))
        self.primitives.append(pcbRectangle(pcbLayer.topAssembly, defaults.documentationWidth,\
            position=[0,3.75], dimensions=[5.65, 1.2]))
        for i in [-1,1]:
            self.primitives.append(pcbSmtPad(pcbLayer.topCopper,[padSpan1/2*i, padOffset1[density]],\
                padSize1[density],i+2))
            self.primitives.append(pcbRectangle(pcbLayer.topAssembly,defaults.documentationWidth,\
                position=[padSpan1/2*i,-4.625],dimensions=[0.95, 2.95]))
        # courtyard and silk
        dim=[max(bodyDimensions[0], padSize2[density][0]),\
            (padSize2[density][1]+padSize1[density][1])/2-padOffset1[density]+padOffset2[density]]
        offsetY=((padSize2[density][1]-padSize1[density][1])/2+padOffset1[density]+padOffset2[density])/2
        self.addCourtyardAndSilk(dim, court[density], offset=[0,offsetY])
        # name, value
        