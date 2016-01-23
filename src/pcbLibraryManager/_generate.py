# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 20:56:14 2015

@author: piotr at nicecircuits.com
"""

from libraries import libraryModules, librarySwitches,\
    libraryRLC, libraryAVR, libraryPinheaders, libraryMosfets, libraryPowerSupplies,\
    libraryTerminalBlocks, libraryResonators, libraryDiodes, libraryMechanical,\
    libraryLogic, libraryCommunicationIC, libraryConnectorsOther, librarySTM32
from libraryManager import cadPackageKiCad
import logging
from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.defaults import *
from symbols.symbolsIC import symbolICquad
from libraryManager.symbolPrimitive import pinType

class _libraryTest(libraryClass):
    def __init__(self):
        super().__init__("_test_")
        self.parts.append(_partTest())

class _partTest(part):
    def __init__(self):
        super().__init__("_test_","TEST")
        pins=[[["%d"%(i+j*7),"%d"%(i+j*4),pinType.IO] for i in range(7)] for j in range(4)]
        self.symbols.append(symbolICquad("_test_",pins))

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
        libs = [libraryModules.libraryModules()]
    else:
        libs = [libraryTerminalBlocks.libraryTerminalBlocks(),  libraryRLC.libraryRLC(),\
            librarySwitches.librarySwitches(),\
            libraryAVR.libraryAVR(), libraryPinheaders.libraryPinheaders(),\
            libraryMosfets.libraryMosfets(), libraryPowerSupplies.libraryPowerSupplies(),\
            libraryModules.libraryModules(), libraryResonators.libraryResonators(),\
            libraryDiodes.libraryDiodes(), libraryMechanical.libraryMechanical(),\
            libraryLogic.libraryLogic(), libraryCommunicationIC.libraryCommunicationIC(),\
            libraryConnectorsOther.libraryConnectorsOther(), librarySTM32.librarySTM32()]
    for lib in libs:
        CP.generateLibrary(lib, path)
        print(lib.name)