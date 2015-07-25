# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:17:33 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from parts import partsSwitches

class librarySwitches(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSwitches")
        self.parts.append(partsSwitches.partMicroswitchSmt())