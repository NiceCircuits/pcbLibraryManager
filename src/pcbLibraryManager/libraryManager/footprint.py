# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:06:39 2015

@author: piotr at nicecircuits.com
"""

import logging
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults
from libraryManager.common import *
from math import  ceil

class footprint:
    """
    """
    
    def __init__(self, name, alternativeLibName, originMarkSize=0, textOnSilk=False, variantName=""):
        """
        """
        self.log=logging.getLogger("footprint")
        self.log.debug("Creating footprint %s.", name)
        self.name = name
        self.alternativeLibName = alternativeLibName
        self.variantName=variantName # to be used with Eagle
        # fields to store name and value text objects - can be changed later
        if textOnSilk:
            textHeight = defaults.silkTextHeight
            width = defaults.silkWidth
        else:
            textHeight = defaults.documentationTextHeight
            width = defaults.documentationWidth
        self.nameObject = pcbText(pcbLayer.topNames, width, "REF**",\
            [0, textHeight * 2], textHeight, align = textAlign.center)
        self.valueObject = pcbText(pcbLayer.topValues, width, name,\
            [0, 0], textHeight, align = textAlign.center)
        # initialize empty list for storing primitives
        self.primitives = []
        if originMarkSize:
            self.addOriginMark(originMarkSize)
    
    def addOriginMark(self, size):
        """
        """
        for rotation in [0, 90]:
            self.primitives.append(pcbLine(pcbLayer.topCourtyard, defaults.documentationWidth,\
                points=scalePoints(rotatePoints([[-1,0],[1,0]], rotation),size)))
        self.primitives.append(pcbCircle(pcbLayer.topCourtyard, defaults.documentationWidth,\
            [0, 0], size*0.7))
    
    def addSimple3Dbody(self, position, dimensions, draw=True, silk=False, file="cube",\
        rotation=0):
        """Add simple cuboid (or other) 3D body.
        
        :param position: position - 2D or 3D
        :param dimensions: dimensions, 3D
        :param draw: If True, drawing on topAssembly is added
        :param silk: If True, drawing on topSilk is added
        :param file: name of wrl file to be used, without extension, default is "cube"
        :param rotations: rotations of 3D body
        """
        # do not add anything if one of dimensions is zero
        for x in dimensions:
            if x==0:
                return
        self.primitives.append(pcb3DBody(file, position, dimensions, [0,0,rotation]))
        if draw:
            self.primitives.append(pcbRectangle(pcbLayer.topAssembly, defaults.documentationWidth,\
                position=position[0:2], dimensions=dimensions[0:2], rotation=rotation))
        if silk:
            self.primitives.append(pcbRectangle(pcbLayer.topSilk, defaults.silkWidth,\
                position=position[0:2], dimensions=dimensions[0:2], rotation=rotation))

    def addCylinder3Dbody(self, position, dimensions, draw=True, silk=False, file="cylinder",\
        rotation=0):
        """Add simple cylinder (or other) 3D body.
        
        :param position: position - 2D or 3D
        :param dimensions: dimensions, 3D
        :param draw: If True, drawing on topAssembly is added
        :param silk: If True, drawing on topSilk is added
        :param file: name of wrl file to be used, without extension, default is "cube"
        :param rotations: rotations of 3D body
        """
        # do not add anything if one of dimensions is zero
        for x in dimensions:
            if x==0:
                return
        self.primitives.append(pcb3DBody(file, position, dimensions, [0,0,rotation]))
        if draw:
            self.primitives.append(pcbCircle(pcbLayer.topAssembly, defaults.documentationWidth,\
                position=position[0:2], radius=dimensions[0]/2))
        if silk:
            self.primitives.append(pcbCircle(pcbLayer.topSilk, defaults.silkWidth,\
                position=position[0:2], radius=dimensions[0]/2))

    def addLead(self, position, dimensions, draw=True, silk=False, lead="gullwing",\
    rotation=0):
        dim=[x for x in dimensions]
        if lead == "gullwing":
            dim[2]=dim[2]/0.8 # height correction
        self.addSimple3Dbody(position, dim, draw, silk, lead, rotation%360)
    
    def addCourtyardAndSilk(self, dimensions, court, silk=True, offset=[0,0]):
        """
        Add courtyard, extend to fit in 0.1mm grid. If silk==true add silkscreen
        rectangle with default extend - if fits in courtyard.
        Return courtyard size and silkscreen size
        """
        # round to 0.2mm
        # (x-0.01) - to cut float rounding error
        courtDim = [ceil((x-0.01+court*2)*5)/5 for x in dimensions]
        # round to 0.1mm
        offset = [round(x,1) for x in offset]
        self.primitives.append(pcbRectangle(pcbLayer.topCourtyard, defaults.documentationWidth,\
            position=offset, dimensions=courtDim))
        self.log.debug("Courtyard %s -> %s" %(dimensions, courtDim))
        if silk and court > defaults.silkWidth/2 + defaults.silkExtend:
            if court<=0.3:
                silkDim = courtDim
            else:
                silkDim = [x + defaults.silkWidth + defaults.silkExtend*2 for x in dimensions]
            self.log.debug("Silkscreen %s -> %s" %(dimensions, silkDim))
            self.primitives.append(pcbRectangle(pcbLayer.topSilk, width=defaults.silkWidth,\
                position=offset, dimensions=silkDim))
        else:
            silkDim=courtDim
        return [courtDim, silkDim]
    
    def renamePads(self, names):
        i=0
        for p in self.primitives:
            n = p.__class__.__name__
            if n == "pcbThtPad" or n == "pcbSmtPad":
                p.name=names[i]
                i+=1

        
if __name__ == "__main__":
    pass