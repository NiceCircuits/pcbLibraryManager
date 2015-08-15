# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 18:28:24 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.common import textAlign
from libraryManager.defaults import defaults
import math
from libraryManager.common import *
import logging 

class pinType:
    """
    """
    input, output, IO, tristate, passive, OC, NC, pwrIn, pwrOut=range(9)

class fillType:
    """
    """
    none, background, foreground = range(3)

class symbolPrimitive:
    """
    """
    def __init__(self, width, position, dimensions = [0.0, 0.0], rotation=0.0, filled = fillType.none):
        self.width = width
        self.position = position
        self.dimensions = dimensions
        self.rotation = rotation
        self.filled = filled
        self.log=logging.getLogger("symbol")

class symbolPin(symbolPrimitive):
    """
    """
    def __init__(self, name, number, position, length, pinType, rotation = 0, heightNumber=None, heightName=None):
        """
        """
        super().__init__(width=0, position = position, rotation=rotation)
        if not heightNumber:
            heightNumber = defaults.symbolPinTextHeight
        if not heightName:
            heightName = defaults.symbolPinTextHeight
        self.heightName = heightName
        self.heightNumber = heightNumber
        self.name=name
        self.number=number
        self.length=length
        self.type = pinType

class symbolPolyline(symbolPrimitive):
    """
    """
    def __init__(self, width, points, filled=fillType.none):
        """
        """
        super().__init__(width, position = None)
        self.points = points 
        self.filled = filled

class symbolLine(symbolPolyline):
    """
    """
    def __init__(self, width,x1 = None, y1 = None, x2 = None, y2 = None,  points = []):
        """
        Initialize with points or x1, y1, x2, y2
        """
        if not points:
            points = [[x1, y1], [x2, y2]]
        super().__init__(width, points)

class symbolRectangle(symbolPrimitive):
    """
    """
    def __init__(self, width, x1 = None, y1 = None, x2 = None, y2 = None,\
        position = [], dimensions = [], rotation = 0.0, points = [], filled=fillType.none):
        """
        Initialize with one of options:
         * position and dimensions 
         * points
         * x1, y1, x2, y2
        """
        if not position:
            if points:
                [[x1, y1], [x2, y2]] = points
            position = [(x1 + x2)/2, (y1 + y2)/2]
            dimensions = [abs(x1-x2), abs(y1-y2)]
        super().__init__(width, position, dimensions, rotation=rotation, filled=filled)

class symbolText(symbolPrimitive):
    """
    """
    def __init__(self, text, position, height, rotation = 0.0,\
        align=textAlign.center, mirror=False, visible = True):
        """
        """
        self.text = text
        self.align = align
        self.mirror = mirror
        self.height = height
        self.visible=visible
        super().__init__(0, position, rotation=rotation)
        
class symbolCircle(symbolPrimitive):
    """
    """
    def __init__(self, width, position, radius, filled=False):
        """
        """
        super().__init__(width, position, filled=filled)
        self.radius=radius

class symbolArc(symbolPrimitive):
    """
    """
    def __init__(self, width, position, radius, angles):
        """
        """
        super().__init__(width, position)
        self.radius=radius
        self.angles=angles

def createSymbolArrow(width, x1, y1, x2, y2, headLength, filled = fillType.none):
    """
    Create arrow as a list of primitives (line + polyline) from x1,y1 to x2,y2
    arrLen: headLength: length of arrow head
    If headLength<= _arrow length_, return only head pointing to x2, y2
    """
    ret = []
    length = math.sqrt((x2-x1)**2+(y2-y1)**2)
    if length>headLength + 0.1:
        ret.append(symbolLine(width, x1, y1, x2, y2))
    rotation = math.degrees(math.atan2(y2-y1, x2-x1))
    points = [[0,0], [-1, 1/2], [-1, -1/2], [0,0]]
    log=logging.getLogger("symbol")
    log.debug(points)
    points = translatePoints(scalePoints(rotatePoints(points,rotation), headLength), [x2,y2])
    log.debug(points)
    ret.append(symbolPolyline(width, points, filled))
    return ret