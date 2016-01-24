# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 23:41:16 2015

@author: piotr at nicecircuits.com
"""

import logging
from libraryManager.symbolPrimitive import *
from libraryManager.defaults import defaults
from libraryManager.common import *


class symbol:
    """
    """
    def __init__(self, name, refDes="U", showPinNames=True, showPinNumbers=True):
        self.log=logging.getLogger("symbol")
        self.log.debug("Creating symbol %s.", name)
        self.name = name
        self.showPinNames=showPinNames
        self.showPinNumbers=showPinNumbers
        # fields to store name and value text objects - can be changed later
        self.nameObject = symbolText(refDes,\
            [0, defaults.symbolTextHeight * 2], defaults.symbolTextHeight, align = textAlign.center)
        self.valueObject = symbolText(name,\
            [0, 0], defaults.symbolTextHeight, align = textAlign.center)
        # initialize empty list for storing primitives and pins
        self.primitives = []
        self.pins = []

    def movePrimitives(self, translation, rotation=0):
        for p in self.primitives+self.pins:
            n = p.__class__.__name__
            if n in ["symbolPin", "symbolRectangle", "symbolText", "symbolCircle"]:
                p.position=translatePoint(rotatePoint(p.position, rotation), translation)
                p.rotation = p.rotation + rotation
            elif n == "symbolPolyline" or n=="symbolLine":
                p.points=translatePoints(rotatePoints(p.points,rotation),translation)
            elif n=="symbolArc":
                p.position=translatePoint(rotatePoint(p.position,rotation),translation)
                p.angles=[(a+rotation)%360 for a in p.angles]

if __name__ == "__main__":
    pass