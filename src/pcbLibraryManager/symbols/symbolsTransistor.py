# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 23:50:39 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *
from libraryManager.defaults import *


class symbolBipolar(symbol):
    """
    Standard symbol for bipolar transistor
    """
    def __init__(self, name="", refDes=defaults.transistorRefDes, polarity="npn", pins=[1,2,3],\
        showPinNames=False, showPinNumbers=False):
        """
        polarity: npn, pnp
        diode: True, False
        pins: pin numbers for B,C,E, like: [1,2,3]
        """
        if not name:
            name = polarity
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        if polarity == "pnp":
            flip=-1
        else:
            flip=1
        # pins
        self.pins.append(symbolPin("B", pins[0], [-200,0], 100, pinType.passive, 0))
        self.pins.append(symbolPin("C", pins[1], [0,200*flip], 100, pinType.passive, 90*(2+flip)))
        self.pins.append(symbolPin("E", pins[2], [0,-200*flip], 100, pinType.passive, 90*(2-flip)))
        # drawing
        self.primitives.append(symbolLine(defaults.symbolThickLineWidth, -100, -133, -100, 133))
        self.primitives.append(symbolLine(defaults.symbolLineWidth, 0, 100*flip, -100+defaults.symbolThickLineWidth/2, 33*flip))
        if flip>0:
            (x1,y1,x2,y2)=(-100+defaults.symbolThickLineWidth/2, -33, 0, -100)
        else:
            (x1,y1,x2,y2)=(0, 100, -100+defaults.symbolThickLineWidth/2, 33)
        self.primitives.extend(createSymbolArrow(defaults.symbolLineWidth, x1,y1,x2,y2, 40, fillType.foreground))
        # texts
        i=1
        for t in [self.nameObject, self.valueObject]:
            t.align = textAlign.centerLeft
            t.position = [25, t.height*i]
            i=-i
