# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:51:04 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from parts import partsEsp8266, partsDcDcConverters

class libraryModules(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceModules")
        self.parts.append(partsEsp8266.partEsp07())
        self.parts.append(partsEsp8266.partEsp01())
        self.parts.append(partsDcDcConverters.partDcDcDsun3A())