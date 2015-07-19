# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:06:39 2015

@author: piotr at nicecircuits.com
"""

import logging
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults
from libraryManager.common import *

class footprint:
    """
    """
    layerTopN=0
    layerBottomN=7    
    
    def __init__(self, name, alternativeLibName, originMarkSize=0):
        """
        """
        self.log=logging.getLogger("footprint")
        self.log.debug("Creating footprint %s.", name)
        self.name = name
        self.alternativeLibName = alternativeLibName
        # fields to store name and value text objects - can be changed later
        self.nameObject = pcbText(pcbLayer.topNames, defaults.silkWidth, "REF**",\
            [0, defaults.textHeight * 2], defaults.textHeight, align = textAlign.center)
        self.valueObject = pcbText(pcbLayer.topValues, defaults.silkWidth, name,\
            [0, 0], defaults.textHeight, align = textAlign.center)
        # initialize empty list for storing primitives
        self.primitives = []
        if originMarkSize:
            self.addOriginMark(originMarkSize)
    
    def addOriginMark(self, size):
        """
        """
        for rotation in [0, 90]:
            self.primitives.append(pcbLine(pcbLayer.topAssembly, defaults.documentationWidth,\
                points=scalePoints(rotatePoints([[-1,0],[1,0]], rotation),size)))
        self.primitives.append(pcbCircle(pcbLayer.topAssembly, defaults.documentationWidth,\
            [0, 0], size*0.7))
        
if __name__ == "__main__":
    pass