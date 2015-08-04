# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:41:04 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from footprints.footprintSmdDualRow import *
from footprints.footprintSmdQuad import *
from libraryManager.symbol import symbol
from libraryManager.part import part

class librarySemiconductors(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSemiconductors")
        self.parts.append(partSemiconductorsDummy())

class symbolDummy(symbol):
    """
    """
    def __init__(self, name):
        super().__init__(name)

class partSemiconductorsDummy(part):
    """
    """
    def __init__(self):
        super().__init__("dummy", defaults.icRefDes)
        self.symbols.append(symbolDummy("dummy"))
        for density in ["L", "N", "M"]:
            self.log.debug("density %s" % density)
            for pinCount in [8,14]:
                self.footprints.append(footprintSoic(pinCount,density=density))
            for pinCount in [3,4,5,6,8]:
                self.footprints.append(footprintSot23(pinCount,density=density))
            for n in [32, 44, 64]:
                self.footprints.append(footprintQfp(n,0.8, density=density))
            for n in [48, 64, 100]:
                self.footprints.append(footprintQfp(n,0.5, density=density))
            for n in [80]:
                self.footprints.append(footprintQfp(n,0.65, density=density))
            