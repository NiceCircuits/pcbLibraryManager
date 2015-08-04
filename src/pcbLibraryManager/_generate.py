# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:56:14 2015

@author: piotr at nicecircuits.com
"""

from libraries import libraryModules, librarySemiconductors, librarySwitches,\
    libraryRLC, libraryAVR, libraryPinheaders
from libraryManager import cadPackageKiCad
import logging

if __name__ == "__main__":
    #enable debug logs
    logging.basicConfig(level=logging.DEBUG, filemode='w', filename="debug.log",\
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
    logging.addLevelName(logging.DEBUG-1, "DEBUG1")
    logging.addLevelName(logging.DEBUG-2, "DEBUG2")
    logging.addLevelName(logging.DEBUG-3, "DEBUG3")
    logging.getLogger().setLevel(logging.WARNING)
    # create CAD package
    CP = cadPackageKiCad.KiCad()
    path = r"D:\test\kicadLib"
    # generate libraries
    libs = [libraryRLC.libraryRLC(), libraryModules.libraryModules(),\
        librarySemiconductors.librarySemiconductors(), librarySwitches.librarySwitches(),\
        libraryAVR.libraryAVR(), libraryPinheaders.libraryPinheaders()]
    for lib in libs:
        CP.generateLibrary(lib, path)