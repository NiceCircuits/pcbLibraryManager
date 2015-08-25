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
    def __init__(self, name, alternativeLibName, pinCount, pitch, padSpan, padDimensions,\
    bodyDimensions, padOffset = [0, 0], originMarkSize=0, leadDimensions=None, court=0.5,\
    bodyStyle="cube", firstPinMarker=True):
        originMarkSize = min(defaults.originMarkSize, bodyDimensions[0]*0.25, bodyDimensions[1]*0.25)
        super().__init__(name, alternativeLibName=alternativeLibName, originMarkSize=originMarkSize,)
        # body
        self.addSimple3Dbody([0,0,0], bodyDimensions, file=bodyStyle)
        if firstPinMarker:
            arcRadius=min(1,bodyDimensions[1]*0.2)
            self.primitives.append(pcbArc(pcbLayer.topAssembly,defaults.documentationWidth,\
                position=[-bodyDimensions[0]/2,0],radius=arcRadius, angles=[-90,90]))
        self.addCourtyardAndSilk([bodyDimensions[0], padSpan+padDimensions[1]], court)
        # pads
        x1 = pitch * (pinCount/4 - 0.5)
        if pinCount==3 or pinCount==5:
            x1 = pitch
        pin=1
        for y in [-1, 1]:
            if (pinCount%2 >0) and (y<0):
                delta=1 # generate additional pin in first row of pins in 3 or 5 pin cases
            else:
                delta=0
            for x in range(int((pinCount+delta)/2)):
                if (pinCount==3 and x==1 and y==-1) or (pinCount==5 and x==1 and y==1)\
                    or (pinCount==3 and x==0 and y==1):
                    correction = 1
                else:
                    correction = 0
                pos = [(x1-pitch*(x+correction))*y+padOffset[0], padSpan/2*y+padOffset[1]]
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=pos,\
                    dimensions=padDimensions, name=str(pin), rotation=0 if y<0 else 180))
                pin+=1
                if leadDimensions:
                    pos1=[a for a in pos]
                    pos1[1]=(bodyDimensions[1]/2+leadDimensions[0]/2)*y
                    self.addLead(pos1, leadDimensions, lead="gullwing", rotation=90 if y>0 else 270)
        # first pin marker, when body and leads are generated and pin count is even
        if leadDimensions and bodyDimensions and (pinCount%2==0) and firstPinMarker:
            r = min(leadDimensions[0]/2, defaults.firstPinMarkerR, bodyDimensions[1]/4)
            self.primitives.append(pcbCircle(pcbLayer.topSilk, defaults.silkWidth,\
                [-x1-r-0.7, -(bodyDimensions[1]+leadDimensions[0])/2], r))

class footprintSoic(footprintSmdDualRow):
    """
    
    """
    def __init__(self, pinCount, name="", alternativeLibName="", density="N", wide=False):
        if not name:
            name="SOIC-%d_%s"%(pinCount,density)
        if not alternativeLibName:
            alternativeLibName="niceSemiconductors"
        if pinCount>16:
            wide=True
        bodyDimensions=[pinCount/2*1.27, 4.04, 2.65 if wide else 1.75]
        super().__init__(name, alternativeLibName, pinCount=pinCount, pitch=1.27,\
            padSpan=5.2,padDimensions=[0.6,2.2], bodyDimensions=bodyDimensions,\
            leadDimensions=[1.3,0.41,1], court = defaults.court[density])

class footprintSot23(footprintSmdDualRow):
    """
    
    """
    def __init__(self, pinCount = 3, name = "", alternativeLibName = "", density="N"):
        if not name:
            name="SOT23-%d_%s"%(pinCount,density)
        if not alternativeLibName:
            alternativeLibName="niceSemiconductors"
        pitch = {3:0.95, 5:0.95, 6:0.95, 8:0.65}
        padSpan = {3:{"L":2.0, "N":2.1, "M":2.2}, 5:{"L":2.7, "N":2.8, "M":3.0},\
            6:{"L":2.7, "N":2.8, "M":3.0}, 8:{"L":2.7, "N":2.8, "M":3.0}}
        padDimensions = {3:{"L":[0.6,0.7], "N":[0.8,0.9], "M":[1,1.4]},\
            5:{"L":[0.6,0.7], "N":[0.75,0.9], "M":[0.75,1.4]},\
            6:{"L":[0.6,0.7], "N":[0.75,0.9], "M":[0.75,1.4]},\
            8:{"L":[0.48,0.7], "N":[0.5,0.9], "M":[0.5,1.4]}}
        bodyDimensions = {3:[3,1.4,1.2], 5:[3.1,1.8,1.45], 6:[3.1,1.8,1.45], 8:[3.1,1.8,1.45]}
        leadDimensions = {3:[0.55,0.5,0.7], 5:[0.7,0.5,0.8], 6:[0.7,0.5,0.8], 8:[0.7,0.38,0.8]}
        # name, alternativeLibName, pinCount, pitch, padSpan, padDimensions
        super().__init__(name, alternativeLibName, pinCount, pitch[pinCount],\
            padSpan[pinCount][density], padDimensions[pinCount][density] ,\
            bodyDimensions=bodyDimensions[pinCount],\
            leadDimensions=leadDimensions[pinCount], court = defaults.court[density])
        # tests
        self.nameObject.position=[0,0]
        self.valueObject.position=[0,\
            -bodyDimensions[pinCount][1]/2-leadDimensions[pinCount][0]-self.valueObject.height]