# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:51:04 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from parts import partsEsp8266, partsDcDcConverters, partsDisplays
from libraryManager.generateLibraries import generateLibraries

class libraryModules(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceModules")
        self.parts.append(partsEsp8266.partEsp07())
        self.parts.append(partsEsp8266.partEsp01())
        self.parts.append(partsEsp8266.partEsp03())
        self.parts.append(partsDcDcConverters.partDcDcDsun3A())
        self.parts.append(partsDisplays.partTFT_1_8_ST7735())
        for mnt in [False, True]:
            self.parts.append(partsDisplays.partOled128x64(mnt))

if __name__ == "__main__":
    generateLibraries([libraryModules()])