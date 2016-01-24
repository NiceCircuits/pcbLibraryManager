# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:18:41 2016

@author: piotr at nicecircuits.com
"""
from libraryManager import cadPackageKiCad
import logging

def generateLibraries(libs):
    #enable debug logs
    logging.basicConfig(level=logging.DEBUG, filemode='w', \
        filename=r"D:\pcbLibraryManager\src\pcbLibraryManager\debug.log",\
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
    logging.addLevelName(logging.DEBUG-1, "DEBUG1")
    logging.addLevelName(logging.DEBUG-2, "DEBUG2")
    logging.addLevelName(logging.DEBUG-3, "DEBUG3")
    logging.getLogger().setLevel(logging.DEBUG)
    # create CAD package
    CP = cadPackageKiCad.KiCad()
    path = r"D:\test\kicadLib"
    # generate libraries
    for lib in libs:
        CP.generateLibrary(lib, path)
        print(lib.name)
