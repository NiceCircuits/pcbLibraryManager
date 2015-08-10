# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 22:17:59 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from libraryManager.common import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *
from libraryManager.footprint import footprint

class libraryPinheaders(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("nicePinheaders")
        for cols in [1,2,3]:
            for rows in range(1,21):
                self.parts.append(partPinheader(cols, rows))
        
class partPinheader(part):
    """
    Pinheader part generator
    """
    def __init__(self, cols, rows, name=""):
        if not name:
            name = "PIN-%dx%d" % (cols, rows)
        super().__init__(name, "CON")
        if cols<3:
            self.symbols.append(symbolPinheader(cols, rows, name))
        else:
            for i in range(cols):
                self.symbols.append(symbolPinheader(1, rows, name, offset=i*rows))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintPinheader(cols, rows, density))

class symbolPinheader(symbolIC):
    """
    Pinheader symbol
    """
    def __init__(self, cols, rows, name, refDes="CON", showPinNames=False,\
        showPinNumbers=True, offset=0):
        pinsRight = [(['%d' % (row * cols + 2), row * cols + 2, pinType.passive] if cols>1 else None) for row in range(rows)]
        pinsLeft = [['%d' % (row * cols + 1), row * cols + offset + 1, pinType.passive] for row in range(rows)]
        super().__init__(name, pinsLeft, pinsRight, 400, refDes, showPinNames, showPinNumbers)

class footprintPinheader(footprint):
    """
    Pinheader footprint
    """
    def __init__(self, cols, rows, density ="N", name=None, alternativeLibName="nicePinheaders",\
        originMarkSize=0, textOnSilk=True):
        court=0.5
        if not name:
            name = "PIN-%dx%d_%s" % (cols, rows, density)
        super().__init__(name, alternativeLibName, originMarkSize, textOnSilk)
        dim={"L":[1.3, 1.3],"N":[1.8, 1.4],"M":[2,2]}
        shape={"L":padShape.round, "N":padShape.roundRect, "M":padShape.round}
        # pins
        n=1
        if cols<3:
            for y in range(rows):
                for x in range(cols):
                    self.primitives.append(pcbThtPad([mil(100)*(x-(cols-1)/2),\
                        mil(100)*(-y+(rows-1)/2)], dim[density], 0.8, str(n),\
                        padShape.rect if n==1 else shape[density]))
                    n+=1
        else:
            for x in range(cols):
                for y in range(rows):
                    self.primitives.append(pcbThtPad([mil(100)*(x-(cols-1)/2),\
                        mil(100)*(-y+(rows-1)/2)], dim[density], 0.8, str(n),\
                        padShape.rect if n==1 else shape[density]))
                    n+=1
        # courtyard
        self.addCourtyardAndSilk([cols*mil(100), rows*mil(100)], court, silk=False)
        # silkscreen
        dim1=[cols*mil(100), rows*mil(100)]
        self.primitives.append(pcbRectangle(pcbLayer.topSilk, width=defaults.silkWidth,\
            position=[0,0], dimensions=dim1))
        self.primitives.append(pcbRectangle(pcbLayer.topSilk, width=defaults.silkWidth,\
            position=[-dim1[0]/2-defaults.silkWidth,dim1[1]/2-mil(50)],\
            dimensions=[defaults.silkWidth, mil(100)]))
        self.nameObject.position=[-dim1[0]/2-self.nameObject.height, 0]
        self.nameObject.rotation=90
        self.valueObject.position=[dim1[0]/2+self.valueObject.height, 0]
        self.valueObject.rotation=90
        