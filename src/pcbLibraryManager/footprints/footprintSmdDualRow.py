# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 06:37:54 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint

class footprintSmdDualRow(footprint):
    """
    Footprint generator for dual row SMD packages: SOIC, TSSOP, SOT23 etc.
    First pin in bottom left corner. 
    """
    def __init__(self, name, pinCount, pitch, padSpan, padDimensions, \
    bodyDimensions, leadDimensions, alternativeLibName = ""):
        if not alternativeLibName:
            alternativeLibName = "niceSemiconductors"
        super().__init__(self, name, alternativeLibName)

class footprintSot23(footprintSmdDualRow):
    """
    Sot23 footprint for reflow soldering. Based on http://www.nxp.com/packages/SOT23.html
    """
    def __init__(self, name, pinCount = 3, alternativeLibName = ""):
        footprintSmdDualRow.__init__(name, pinCount, pitch = 0.95, 
        padSpan = 2.0, padDimensions = (0.6, 0.7))