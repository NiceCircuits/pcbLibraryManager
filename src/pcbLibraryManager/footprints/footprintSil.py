# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 13:08:14 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.defaults import defaults
from libraryManager.footprintPrimitive import *

class footprintTO220(footprintSilWithTab):
    """
    TO220 footprint generator
    """
    def __init__(pinCount=3, version="H", density="N"):
        name = "TO220_%d%s_%s" % (pinCount, version, density)
        super().__init__(name=name, pinCount=pinCount, pitch=2.54,\
            bodySize=[], bodyOffset=[],\
            tabSize=[],\
            pinSize1=[], pinSize2=[],\
            density=density)
    pass

class footprintSilWithTab(footprint):
    """
    Generator for SIL packages with heatsink tab (TO220 etc.)
    """
    def __init__(self, name, pinCount, pitch, bodySize, bodyOffset, tabSize, \
    pinSize1, pinSize2, density="N", padSize=None, court=None, alternativeLibName="niceSemiconductors"):
        raise Exception("not implemented!")
        super().__init__(name, alternativeLibName)
        # body
        self.addSimple3Dbody(bodyOffset, bodySize)
        # tab
        self.addSimple3Dbody(\
            [bodyOffset[0],\
            bodyOffset[1]+bodySize[1]/2-tabSize[1]/2,\
            bodyOffset[3]+bodySize[3]],\
            tabSize, file="cube_metal")
        # pads
        if 0:
            iX = [-a for a in range(tabNumber-1,0,-1)] + [a for a in range(tabNumber)]
            stub = (pads%2)==0
            for i in iX:
                if i==0 and stub:
                    # stub
                    self.addSimple3Dbody([0,-(bodySize[1]+stubSize[1])/2,\
                        leadSize[2]-stubSize[2]], stubSize, file="cube_metal")
                else:
                    # pin
                    self.primitives.append(pcbSmtPad(pcbLayer.topCopper,[pitch*i, padOffset],\
                        padSize,i+tabNumber))
                    self.addLead([pitch*i,-(bodySize[1]+leadSize[0])/2], leadSize, rotation=270)
            # courtyard and silk
            dim=[max(bodySize[0], tabPadSize[0]),\
                (tabPadSize[1]+padSize[1])/2-padOffset+tabPadOffset]
            offsetY=((tabPadSize[1]-padSize[1])/2+padOffset+tabPadOffset)/2
            self.addCourtyardAndSilk(dim, court, offset=[0,offsetY])
            # name, value
