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
    def __init__(self, cols, rows, pitch, padSize, shape, drill, name, bodySize=None,\
        alternativeLibName="niceConnectors", court=0.5, bodyOffset=[0,0], alternativeNumbering=False,\
        originMarkSize=0, textOnSilk=True, keySize=None, keyOnBack=True,\
        pinDimensions=[0,0,0], pinZOffset=0, bodyHeight=1):
        super().__init__(name, alternativeLibName, originMarkSize, textOnSilk)
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
                    pos =[pitch[0]*(x-(cols-1)/2), pitch[1]*(-y+(rows-1)/2)]
                    self.primitives.append(pcbThtPad(pos, padSize, drill, str(n),\
                        padShape.rect if n==1 else shape))
                    pos=pos+[pinZOffset]
                    self.addSimple3Dbody(pos, pinDimensions)
                    n+=1
        else:
            for x in range(cols):
                for y in range(rows):
                    pos=[pitch[0]*(x-(cols-1)/2), pitch[1]*(-y+(rows-1)/2)]
                    self.primitives.append(pcbThtPad(pos, padSize, drill, str(n),\
                        padShape.rect if n==1 else shape))
                    pos=pos+[pinZOffset]
                    self.addSimple3Dbody(pos, pinDimensions)
                    n+=1
        # courtyard
        self.addCourtyardAndSilk(bodySize, court, silk=False, offset=bodyOffset)
        # silkscreen
        self.primitives.append(pcbRectangle(pcbLayer.topSilk, width=defaults.silkWidth,\
            position=bodyOffset, dimensions=bodySize))
        self.addSimple3Dbody(bodyOffset, bodySize+[bodyHeight])
        # if keyed connector
        if keySize:
            # TODO: key, like in NS25
            pass
        elif keySize==-1:
            # no key, no first pin marker
            pass
        else:
            # default first pin marker
            self.primitives.append(pcbRectangle(pcbLayer.topSilk, width=defaults.silkWidth,\
                position=[-bodySize[0]/2-defaults.silkWidth+bodyOffset[0],bodySize[1]/2-pitch[1]/2+bodyOffset[1]],\
                dimensions=[defaults.silkWidth, pitch[1]]))
        # align texts
        i=-1
        for text in [self.nameObject, self.valueObject]:
            text.position=[i*(bodySize[0]/2+text.height)+bodyOffset[0], bodyOffset[1]]
            text.rotation=90
            if textOnSilk:
                text.layer=pcbLayer.topSilk
            i=-i
        