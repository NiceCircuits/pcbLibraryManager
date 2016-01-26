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
from footprints.footprintConnectors import footprintConnectorTht
from libraryManager.generateLibraries import generateLibraries

class libraryPinheaders(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("nicePinheaders")
        for gender in ["M", "F"]:
            for angled in [False, True]:
                for cols in [1,2,3]:
                    for rows in range(1,21):
                        self.parts.append(partPinheader(cols, rows, gender=gender, angled=angled))
        
class partPinheader(part):
    """Pinheader part generator
    """
    def __init__(self, cols, rows, angled=False, gender = "M", name=""):
        """:param cols: columns - 1,2,3 or more
        :param rows: rows, 1..inf
        :param angled: right angle version if True
        :param gender: **"M"**:male, **"F"**: female
        """
        if not name:
            name = "PIN-%dx%d%s%s" % (cols, rows, "_F" if gender=="F" else "",\
                "_angled" if angled else "")
        super().__init__(name, "CON")
        if cols<3:
            self.symbols.append(symbolPinheader(cols, rows, name))
        else:
            for i in range(cols):
                self.symbols.append(symbolPinheader(1, rows, name, offset=i*rows))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintPinheader(cols, rows, density, angled=angled,\
                gender=gender))

class symbolPinheader(symbolIC):
    """Pinheader symbol
    """
    def __init__(self, cols, rows, name, refDes="CON", showPinNames=False,\
        showPinNumbers=True, offset=0):
        pinsRight = [(['%d' % (row * cols + 2), row * cols + 2, pinType.passive] if cols>1 else None) for row in range(rows)]
        pinsLeft = [['%d' % (row * cols + 1), row * cols + offset + 1, pinType.passive] for row in range(rows)]
        super().__init__(name, pinsLeft, pinsRight, 400, refDes, showPinNames, showPinNumbers)

class footprintPinheader(footprintConnectorTht):
    """Pinheader footprint
    """
    def __init__(self, cols, rows, density ="N", name=None, alternativeLibName="nicePinheaders",\
        originMarkSize=0, textOnSilk=True, pinLength=-1, bodyHeight=-1, angled=False,
        gender = "M", alternative=False):
        dim={"L":[1.3, 1.3],"N":[1.8, 1.4],"M":[2,2]}
        shape={"L":padShape.round, "N":padShape.roundRect, "M":padShape.round}
        if bodyHeight<0:
            if gender=="F":
                bodyHeight=8.5
            else:
                bodyHeight=2.5
        if pinLength<0:
            if gender=="F":
                pinLength=3
            else:
                pinLength=11.75
        if not name:
            name = "PIN-%dx%d%s%s_%s" % (cols, rows, "_F" if gender=="F" else "",\
                "_angled" if angled else "", density)
        super().__init__(cols, rows, mil(100), dim[density], shape[density], 1.0,\
            name=name, alternativeLibName=alternativeLibName, court=defaults.courtConn[density],\
            bodyHeight=bodyHeight, pinDimensions=[0.64, 0.64, pinLength], pinZOffset=-3,\
            angled=angled, angledOffset=-1.4,gender=gender)

if __name__ == "__main__":
    generateLibraries([libraryPinheaders()])