# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:41:58 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.part import part
from libraryManager.symbol import symbol
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults
from footprints.footprintSmdDualRow import *


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
        self.symbol = symbolDummy("dummy")
        for density in ["L", "N", "M"]:
            for pinCount in [8,14]:
                self.footprints.append(footprintSoic(pinCount,density=density))
        for density in ["L", "N", "M"]:
            for pinCount in [3,4,5,6,8]:
                self.footprints.append(footprintSot23(pinCount,density=density))