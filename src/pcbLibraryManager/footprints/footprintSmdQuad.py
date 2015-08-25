# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 06:52:50 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults
from libraryManager.common import *

class footprintSmdQuad(footprint):
    """
    Footprint generator for quad SMD packages.
    """
    def __init__(self, name, alternativeLibName, pinCount, pitch, padSpan, padDimensions, 
        bodyDimensions, court, leadDimensions=None, offset = [0, 0], originMarkSize=-1):
        if originMarkSize<0:
            originMarkSize = min(defaults.originMarkSize, bodyDimensions[0]*0.3, bodyDimensions[1]*0.3)    
        super().__init__(name, alternativeLibName=alternativeLibName, originMarkSize=originMarkSize)
        # pads, leads
        y1 = pitch * (pinCount/8 - 0.5)
        for side in range(4):
            for y in range(int(pinCount/4)):
                pos = translatePoints(rotatePoints([[-padSpan[0]/2, y1-pitch*y]], side*90), offset)[0]
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=pos,\
                    dimensions=padDimensions, name=str(int(y+1+side*pinCount/4)),\
                    rotation=side*90))
                if leadDimensions:
                    self.addLead(rotatePoints(\
                        [[(-bodyDimensions[side%2]/2-leadDimensions[0]/2), y1-pitch*y]], side*90)[0],\
                        leadDimensions, rotation=side*90+180, lead="gullwing")
        # body
        self.addSimple3Dbody([0,0], bodyDimensions)
        radius = min(bodyDimensions[0]*0.05, bodyDimensions[1]*0.05, 0.5)
        self.primitives.append(pcbCircle(pcbLayer.topAssembly, defaults.documentationWidth,\
            rotatePoints(scalePoints([bodyDimensions[0:2]], 0.4),90)[0], radius))
        # courtyard
        self.addCourtyardAndSilk([s+max(padDimensions) for s in padSpan], court, silk=False)
        # texts
        if originMarkSize:
            y = originMarkSize + defaults.documentationTextHeight
            self.nameObject.position=[0,y]
            self.valueObject.position=[0,-y]

class footprintQfp(footprintSmdQuad):
    """
    QFP (0.5, 0.65, 0.8, 1.0mm pitch). Based on Atmel datasheets.
    """
    def __init__(self, pinCount, pitch, name="", alternativeLibName="", density="N"):
        if not name:
            name="QFP-%d-%1.1f_%s"%(pinCount, pitch, density)
        if not alternativeLibName:
            alternativeLibName="niceSemiconductors"
        bodyDimensions={0.5:{32:[5.1,5.1, 1.2], 48:[7.1,7.1, 1.2], 64:[10.1,10.1, 1.2], 80:[12.1,12.1, 1.2],\
            100:[14.1,14.1, 1.2], 144:[20.1, 20.1, 1.2], 176:[24.1,24.1, 1.2], 208:[28.1, 28.1, 1.2],},\
            0.65:{20:[4.1,4.1, 1.2], 40:[7.1, 7.1, 1.2], 52:[10.1, 10.1, 1.2], 64:[12.1, 12.1, 1.2],\
            80:[14.1,14.1, 1.2], 112:[20.1,20.1, 1.2], 160:[28,28, 1.2]},\
            0.8:{32:[7.1,7.1, 1.2], 44:[10.1,10.1, 1.2], 52:[12.1,12.1, 1.2], 64:[14.1,14.1, 1.2]},\
            1.0:{36:[10.1,10.1, 1.2], 44:[12.1,12.1, 1.2], 52:[14.1,14.1, 1.2]}}
        leadDimensions={0.5:[1,0.27, 0.6], 0.65:[1, 0.38, 0.6], 0.8:[1,0.45, 0.6], 1.0:[1, 0.5, 0.6]}
        padSpan={0.5:{48:{"L":[8.4, 8.4], "N":[8.4, 8.4], "M":[8.4, 8.4]},\
            64:{"L":[11.4, 11.4], "N":[11.4, 11.4], "M":[11.4, 11.4]},\
            100:{"L":[15.4, 15.4], "N":[15.4, 15.4], "M":[15.4, 15.4]}},\
            0.65:{80:{"L":[15.4, 15.4], "N":[15.4, 15.4], "M":[15.4, 15.4]}},\
            0.8:{32:{"L":[8.4, 8.4], "N":[8.4, 8.4], "M":[8.4, 8.4]},\
            44:{"L":[11.4, 11.4], "N":[11.4, 11.4], "M":[11.4, 11.4]},\
            64:{"L":[15.4, 15.4], "N":[15.4, 15.4], "M":[15.4, 15.4]}}}
        padDimensions={0.5:{"L":[1.5, 0.3], "N":[1.5, 0.3], "M":[1.5, 0.3]},\
            0.65:{"L":[1.5, 0.45], "N":[1.5, 0.45], "M":[1.5, 0.45]},\
            0.8:{"L":[1.5,0.55], "N":[1.5,0.55], "M":[1.5,0.55]}}
        super().__init__(name, alternativeLibName, pinCount=pinCount, pitch=pitch,\
            padSpan=padSpan[pitch][pinCount][density],\
            padDimensions=padDimensions[pitch][density],\
            bodyDimensions=bodyDimensions[pitch][pinCount], court = defaults.court[density],\
            leadDimensions=leadDimensions[pitch])

