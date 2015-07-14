# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:56:14 2015

@author: piotr at nicecircuits.com
"""

import libraryManager
from libraries import libraryModules
from libraryManager import cadPackageKiCad
import logging

if __name__ == "__main__":
    #enable debug logs
    logging.basicConfig(level=logging.DEBUG, filemode='w', filename="debug.log",\
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
    logging.addLevelName(logging.DEBUG-1, "DEBUG1")
    logging.addLevelName(logging.DEBUG-2, "DEBUG2")
    logging.addLevelName(logging.DEBUG-3, "DEBUG3")
    logging.getLogger().setLevel(logging.DEBUG-3)
    # create CAD package
    CP = cadPackageKiCad.KiCad()
    # generate libraries
    niceModules = libraryModules.libraryModules()
    CP.generateLibrary(niceModules, r"D:\test\kicadLib")
    