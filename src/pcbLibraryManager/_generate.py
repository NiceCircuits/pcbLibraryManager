# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:56:14 2015

@author: piotr at nicecircuits.com
"""

from libraries import libraryModules, librarySemiconductors, librarySwitches,\
    libraryRLC, libraryAVR, libraryPinheaders, libraryMosfets, libraryPowerSupplies,\
    libraryTerminalBlocks, libraryResonators, libraryDiodes
from libraryManager import cadPackageKiCad
import logging

if __name__ == "__main__":
    #enable debug logs
    logging.basicConfig(level=logging.DEBUG, filemode='w', filename="debug.log",\
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
    logging.addLevelName(logging.DEBUG-1, "DEBUG1")
    logging.addLevelName(logging.DEBUG-2, "DEBUG2")
    logging.addLevelName(logging.DEBUG-3, "DEBUG3")
    logging.getLogger().setLevel(logging.DEBUG)
    # create CAD package
    CP = cadPackageKiCad.KiCad()
    path = r"D:\test\kicadLib"
    # generate libraries
    if True:
        libs = [libraryRLC.libraryRLC()]
    else:
        libs = [libraryTerminalBlocks.libraryTerminalBlocks(),  libraryRLC.libraryRLC(),\
            librarySemiconductors.librarySemiconductors(), librarySwitches.librarySwitches(),\
            libraryAVR.libraryAVR(), libraryPinheaders.libraryPinheaders(),\
            libraryMosfets.libraryMosfets(), libraryPowerSupplies.libraryPowerSupplies(),\
            libraryModules.libraryModules(), libraryResonators.libraryResonators()]
    for lib in libs:
        CP.generateLibrary(lib, path)