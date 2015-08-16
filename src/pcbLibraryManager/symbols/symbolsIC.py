# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 19:02:52 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *
from libraryManager.defaults import defaults

class symbolIC(symbol):
    """
    IC symbol generator
    Generate symbol with pinsLeft, pinsRight pins on each side
    pinsLeft, pinsRight: list of ["pin name", "pin number", type]
    width: width of symbol rectangle
    """
    def __init__(self, name, pinsLeft, pinsRight, width, refDes=defaults.icRefDes,\
        showPinNames=True, showPinNumbers=True):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        # body
        height = (max(len(pinsLeft), len(pinsRight))+1)*100
        offset = 50 if (height % 200) > 0 else 0
        if width % 200 >0:
            width = width//200 + 200
        self.log.debug("IC symbol body: pins: %d, %d; height: %d, offset: %d" %\
            (len(pinsLeft), len(pinsRight), height, offset))
        self.primitives.append(symbolRectangle(0, position=[0,offset],\
            dimensions=[width, height], filled=fillType.background))
        # pins
        pinLength = 200
        pins = [pinsLeft, pinsRight]
        for x in range(2):
            y = height/2-100+offset
            for p in pins[x]:
                if p:
                    self.pins.append(symbolPin(p[0], p[1], [(width/2+pinLength)*(1 if x>0 else -1),y],\
                        pinLength, p[2], rotation=180 if x>0 else 0))
                y = y-100
        self.nameObject.position=[0, height/2 + self.nameObject.height + offset]
        self.valueObject.position=[0, -(height/2 + self.valueObject.height) + offset]
