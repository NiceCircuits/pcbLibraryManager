# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 23:13:18 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from libraryManager.common import *
from libraryManager.footprint import footprint

class footprintConnectorTht(footprint):
    """Footprint generator for THT raster connetors.
    First pin in top left corner. 
    """
    def __init__(self, cols, rows, pitch, padSize, shape, drill, name, gender="M",bodySize=None,\
    alternativeLibName="niceConnectors", court=0.5, bodyOffset=[0,0], alternativeNumbering=False,\
    originMarkSize=0, textOnSilk=True, keySize=None, keyOnBack=True, pinDimensions=[0,0,0],\
    pinZOffset=0, bodyHeight=1, angled=False, angledOffset=0, bodyStyle="cube"):
        super().__init__(name, alternativeLibName, originMarkSize, textOnSilk)
        self.log.debug(["body offset", bodyOffset])
        if not isinstance(pitch,list):
            pitch = [pitch, pitch]
        if not bodySize:
            bodySize=[pitch[0]*cols, pitch[1]*rows]
        if len(padSize)!=2 or len(bodySize)!=2:
            raise ValueError("Invalid parameters!")
        # pins
        n=1
        if cols<3 and not alternativeNumbering:
            for y in range(rows):
                for x in range(cols):
                    self.addPin(pitch, x, y, cols, rows, gender, padSize, drill, n, shape,\
                    pinDimensions, pinZOffset, angled, angledOffset, bodySize, bodyOffset)
                    n+=1
        else:
            for x in range(cols):
                for y in range(rows):
                    self.addPin(pitch, x, y, cols, rows, gender, padSize, drill, n, shape,\
                    pinDimensions, pinZOffset, angled, angledOffset, bodySize, bodyOffset)
                    n+=1
        # body
        pos=[x for x in bodyOffset]
        if angled:
            pos[0]= pos[0]+angledOffset-bodyHeight/2-(cols-1)*pitch[1]/2
            self.addSimple3Dbody(pos, [bodyHeight, bodySize[1], bodySize[0]], silk=True)
            if pinDimensions[2]>pinZOffset+bodyHeight:
                for y in range(rows):
                    l = pinDimensions[2]+pinZOffset-bodyHeight
                    self.primitives.append(pcbRectangle(pcbLayer.topSilk, defaults.silkWidth,\
                        position=[pos[0]-bodyHeight/2-l/2, pitch[1]*(-y+(rows-1)/2)],\
                        dimensions=[l, pinDimensions[1]]))
        else:
            self.addSimple3Dbody(bodyOffset, bodySize+[bodyHeight], silk=True, file=bodyStyle)
        # courtyard
        pos=[x for x in bodyOffset]
        size=[x for x in bodySize]
        if pinDimensions[2]>pinZOffset+bodyHeight:
            pos[0]+=(angledOffset+bodyHeight/2-pinDimensions[2]-pinZOffset)/2*angled
            size[0]+=(-angledOffset-bodyHeight/2+pinDimensions[2]+pinZOffset)*angled
        else:
            pos[0]+=(angledOffset-bodyHeight+bodySize[0]/2-pitch[0]/2*(cols-1))/2*angled
            size[0]+=(-angledOffset+bodyHeight-bodySize[0]/2+pitch[0]/2*(cols-1))*angled
        self.addCourtyardAndSilk(size, court, silk=False, offset=pos)
        # if keyed connector
        if keySize:
            # TODO: key, like in NS25
            pass
        elif keySize==-1:
            # no key, no first pin marker
            pass
        else:
            # default first pin marker
            if gender=="M":
                # male - first pin on left side
                flip=1
            elif gender=="F":
                # female - left pin on right side
                flip=-1
            else:
                raise ValueError("Unsupported gender %s" % gender)
            pos=[x for x in bodyOffset]
            pos[0]+=(bodySize[0]/2-bodyHeight+angledOffset-pitch[0]*(cols-1)/2)*angled
            self.primitives.append(pcbRectangle(pcbLayer.topSilk, width=defaults.silkWidth,\
                position=[(-bodySize[0]/2-defaults.silkWidth)*flip+pos[0],\
                    bodySize[1]/2-pitch[1]/2+pos[1]],\
                dimensions=[defaults.silkWidth, pitch[1]]))
        # align texts
        i=-1
        for text in [self.nameObject, self.valueObject]:
            text.position=[i*(bodySize[0]/2+text.height)+bodyOffset[0], bodyOffset[1]]
            text.rotation=90
            if textOnSilk:
                text.layer=pcbLayer.topSilk
            i=-i
        self.nameObject.visible = False

    def addPin(self, pitch, x, y, cols, rows, gender, padSize, drill, number, shape,\
    pinDimensions, pinZOffset, angled, angledOffset, bodySize, bodyOffset):
        if gender=="M":
            # male - first pin on left side
            flip=1
        elif gender=="F":
            # female - left pin on right side
            flip=-1
        else:
            raise ValueError("Unsupported gender %s" % gender)
        pos=[pitch[0]*(x-(cols-1)/2)*flip, pitch[1]*(-y+(rows-1)/2)]
        self.primitives.append(pcbThtPad(pos, padSize, drill, str(number),\
            padShape.rect if number==1 else shape))
        dim = [a for a in pinDimensions]
        if angled:
            dim[2]=-pinZOffset+bodySize[0]/2-bodyOffset[0]+pitch[0]*(x*2-cols+1)/2-pinDimensions[0]/2
            dim1=[pinDimensions[2]+pinZOffset-angledOffset+pitch[0]*x+pinDimensions[0]/2,\
                pinDimensions[1], pinDimensions[0]]
            pos1=[-dim1[0]/2+pinDimensions[1]/2+(x-(cols-1)/2)*pitch[0], pos[1], dim[2]+pinZOffset]
            self.addSimple3Dbody(pos1, dim1, file="cube_metal")
        self.addSimple3Dbody(pos+[pinZOffset], dim, file="cube_metal")
