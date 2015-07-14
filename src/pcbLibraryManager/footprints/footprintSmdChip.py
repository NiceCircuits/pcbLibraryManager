# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 21:45:08 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint

class footprintSmdChip(footprint):
    """
    Chip component (0603, 0805 etc.)
    """
    def __init__(self, name, size, density, alternativeLibName):
        """
        size: "0603", "0805"
        density: "L" - least, "N" - nominal, "M" - most
        """
        super().__init__(self, name, alternativeLibName)
        chipDimensions = {
        "0402":{"Lmax":1.7, "Wmax":0.9, "Hmax":0.55},
        "0402":{"Lmax":1.7, "Wmax":0.9, "Hmax":0.55},
        "0402":{"Lmax":1.7, "Wmax":0.9, "Hmax":0.55},
        "0402":{"Lmax":1.7, "Wmax":0.9, "Hmax":0.55}
        }
        dimensions = {
        "0402L":1
        }