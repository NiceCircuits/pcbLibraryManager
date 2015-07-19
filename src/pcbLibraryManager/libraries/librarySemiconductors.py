# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 09:41:04 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from parts import partsSemiconductorsDummy

class librarySemiconductors(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSemiconductors")
        self.parts.append(partsSemiconductorsDummy.partSemiconductorsDummy())