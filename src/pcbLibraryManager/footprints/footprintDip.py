# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:04:38 2015

@author: piotr at nicecircuits.com
"""
from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import defaults

class footprintDip(footprint):
    """
    Footprint generator for DIP packages. First pin in bottom left corner. 
    """
    def __init__(self, pinCount, name="", alternativeLibName="", density="N", wide=False):
        if not name:
            name="DIP-%d_%s"%(pinCount,density)
        if not alternativeLibName:
            alternativeLibName="niceSemiconductors"
        if pinCount>=32:
            wide=True
        super().__init__(name, alternativeLibName=alternativeLibName)

