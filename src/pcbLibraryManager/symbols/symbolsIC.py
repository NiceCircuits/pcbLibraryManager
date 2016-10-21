# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 19:02:52 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *
from libraryManager.defaults import defaults
from libraryManager.common import *

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
            width = (width//200+1) * 200
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
                    if isinstance(p[2],str):
                        p[2]=pinType.fromStr[p[2]]
                    self.pins.append(symbolPin(str(p[0]), str(p[1]), [(width/2+pinLength)*(1 if x>0 else -1),y],\
                        pinLength, p[2], rotation=180 if x>0 else 0))
                y = y-100
        self.nameObject.position=[0, height/2 + self.nameObject.height + offset]
        self.valueObject.position=[0, -(height/2 + self.valueObject.height) + offset]

class symbolICquad(symbol):
    """
    Quad IC symbol generator
    Generate symbol with pins[] on each side
    pins: list of 0..4 lists of ["pin name", "pin number", type]
        top, right, bottom, left, clockwise
    size: size of symbol rectangle (auto if 0)
    """
    def __init__(self, name, pins, size=0, refDes=defaults.icRefDes,\
        showPinNames=True, showPinNumbers=True):
        super().__init__(name, refDes, showPinNames, showPinNumbers)
        # body
        if size==0:
            size = (len(pins[0])+5)*100
        offset = 50 if (size % 200) > 0 else 0
        self.log.debug("IC quad symbol body: pins: %d; size: %d, offset: %d" %\
            (sum([len(p) for p in pins]), size, offset))
        self.primitives.append(symbolRectangle(0, position=[offset,offset],\
            dimensions=[size, size], filled=fillType.background))
        # pins
        pinLength = 200
        for side in range(4):
            pos = [-len(pins[0])*50+50, size/2+pinLength]
            rot = -side*90
            for p in pins[side]:
                if p:
                    self.pins.append(symbolPin(p[0], p[1], 
                        translatePoints(rotatePoints([pos],rot),[offset,offset])[0],\
                        pinLength, p[2], rotation=(rot-90)%360))
                pos[0] = pos[0]+100
#        self.nameObject.position=[0, height/2 + self.nameObject.height + offset]
#        self.valueObject.position=[0, -(height/2 + self.valueObject.height) + offset]
