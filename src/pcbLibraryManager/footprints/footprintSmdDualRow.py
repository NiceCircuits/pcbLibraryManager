# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 06:37:54 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults

class footprintSmdDualRow(footprint):
    """
    Footprint generator for dual row SMD packages. Generate only pads
    First pin in bottom left corner. 
    """
    def __init__(self, name, alternativeLibName, pinCount, pitch, padSpan, padDimensions, 
        offset = [0, 0], originMarkSize=0):
        super().__init__(name, alternativeLibName=alternativeLibName, originMarkSize=originMarkSize)
        x1 = pitch * (pinCount/4 - 0.5)
        for y in [-1, 1]:
            delta=0
            if (pinCount%2 >0) and (y<0):
                delta=1 # generate additional pin in first row of pins in 3 or 5 pin cases
            for x in range(int((pinCount+delta)/2)):
                pos = [(x1-pitch*x)*y+offset[0], padSpan/2*y+offset[1]]
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=pos,\
                    dimensions=padDimensions, name=str(int(x+1 if y<0 else x+pinCount/2+1)),\
                    rotation=0 if y<0 else 180))


class footprintSmdDualRowLeaded(footprintSmdDualRow):
    """
    Footprint generator for dual row SMD packages: SOIC, TSSOP, SOT23 etc.
    First pin in bottom left corner. 
    """
    def __init__(self, name, alternativeLibName, pinCount, pitch, padSpan, padDimensions, 
        bodyDimensions, leadDimensions):
        originMarkSize = min(defaults.originMarkSize, bodyDimensions[0]*0.5, bodyDimensions[1]*0.5)
        # pads
        super().__init__(name, alternativeLibName, pinCount=pinCount, pitch=pitch,
            padSpan=padSpan, padDimensions=padDimensions, originMarkSize=originMarkSize)
        # body
        self.primitives.append(pcbRectangle(pcbLayer.topAssembly,defaults.documentationWidth,\
            position=[0,0], dimensions=bodyDimensions))
        arcRadius=min(1,bodyDimensions[1]*0.2)
        self.primitives.append(pcbArc(pcbLayer.topAssembly,defaults.documentationWidth,\
            position=[-bodyDimensions[0]/2,0],radius=arcRadius, angles=[-90,90]))
        # leads
        for y in [-1, 1]:
            for x in range(int(pinCount/2)):
                x1 = pitch * (pinCount/4 - 0.5)
                y1 = bodyDimensions[1]/2+leadDimensions[1]/2
                self.primitives.append(pcbRectangle(pcbLayer.topAssembly,defaults.documentationWidth,\
                    position=[(x1-pitch*x)*y,y*y1],dimensions=leadDimensions))


class footprintSoic(footprintSmdDualRowLeaded):
    """
    
    """
    def __init__(self, pinCount, name="", alternativeLibName="", density="N", wide=False):
        if not name:
            name="SOIC-%d_%s"%(pinCount,density)
        if not alternativeLibName:
            alternativeLibName="niceSemiconductors"
        bodyDimensions=[pinCount/2*1.27,4.04]
        super().__init__(name, alternativeLibName, pinCount=pinCount, pitch=1.27,\
            padSpan=5.2,padDimensions=[0.6,2.2], bodyDimensions=bodyDimensions,\
            leadDimensions=[0.41,1.3])

class footprintSot23(footprintSmdDualRowLeaded):
    """
    
    """
    def __init__(self, pinCount = 3, name = "", alternativeLibName = "", density="N"):
        if not name:
            name="SOT23-%d_%s"%(pinCount,density)
        if not alternativeLibName:
            alternativeLibName="niceSemiconductors"
        super().__init__(name, alternativeLibName, pinCount, pitch = 0.95,\
            padSpan = 2.0, padDimensions = (0.6, 0.7), bodyDimensions=[3, 1.4], leadDimensions=[0.46, 0.6])