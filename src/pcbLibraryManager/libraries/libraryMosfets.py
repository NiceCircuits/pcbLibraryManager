# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 22:18:17 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from footprints.footprintSmdDualRow import *
from footprints.footprintSmdQuad import *
from footprints.footprintSmdPower import *
from libraryManager.symbol import symbol
from libraryManager.part import part

class libraryMosfets(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceMosfets")
        self.parts.append(partNMosUniversal())
        self.parts.append(partPMosUniversal())

class symbolMosfet(symbol):
    """
    """
    def __init__(self, name="", polarity="N"):
        """
        Polarity: N, P
        """
        super().__init__(name)

class partNMosUniversal(part):
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
            self.footprints.append(footprintDPak(density=density))
            
class partPMosUniversal(part):
    """
    """
    def __init__(self):
        pass