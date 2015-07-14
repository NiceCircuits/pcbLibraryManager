# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 22:20:00 2015

@author: piotr at nicecircuits.com
"""
from libraryManager.library import libraryClass
from parts.partsDefaultMosfets import *

class libraryMosfet(libraryClass):
    """
    """
    def __init__(self):
        libraryClass.__init__(self, "niceMosfet")
        self.parts["2N2007"] = partDefaultMosfetSot23()
        

if __name__ == "__main__":
    lib = libraryMosfet()