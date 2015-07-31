# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 18:57:55 2015

@author: piotr at nicecircuits.com


Assumptions:
default units are mm and degrees
"""

from libraryManager.library import  libraryClass
import logging
import os.path
from libraryManager.common import *

def convertRectangleCenterToVertices(position, dimensions):
    x1 = float(position(0)) - float(dimensions(0))/2.0
    x2 = float(position(0)) + float(dimensions(0))/2.0
    y1 = float(position(1)) - float(dimensions(1))/2.0
    y2 = float(position(1)) + float(dimensions(1))/2.0
    return ((x1, y1), (x2,y2))

def convertRectangleVerticiesToCenter(point1,point2):
    posX = (float(point1(0)) + float(point2(0)))/2.0
    posY = (float(point1(1)) + float(point2(1)))/2.0
    dimX = abs(float(point1(0)) - float(point2(0)))
    dimY = abs(float(point1(1)) - float(point2(1)))
    return ((posX, posY), (dimX,dimY))
    
def mil(val):
    """convert mil to mm"""
    return float(val) * 0.0254

def inch(val):
    """convert inch to mm"""
    return float(val) * 25.4

class cadPackage:
    """
    """
    def __init__(self):
        self.log = logging.getLogger("cadPackage")
    
    def generateLibrary(self, library, path):
        """
        Generate library from library class object
        path: path to top level library folder
        """
        if not isinstance(library, libraryClass):
            errMsg = "*generateLibrary*: *library* parameter is not an instance of *libraryClass*. " \
                "It's *%s*." % library.__class__.__name__
            self.log.error(errMsg)
            raise TypeError(errMsg)
        self.log.info("Generating library %s for %s in folder: \|%s\".", 
            library.name ,self.__class__.__name__, path)
    
    def openFile(self, path):
        """
        Create library file. If file exists, copy it to subfolder
        """
        if os.path.isfile(path):
            (directory, fileName) = os.path.split(path)
            oldDir = os.path.join(directory, "old")
            movePath = os.path.join(oldDir, fileName + "_" + timestamp())
            self.createFolder(oldDir)
            os.rename(path, movePath)
            self.log.info("Library %s exists. Old version moved to *old* directory.",\
                fileName)
        return open(path, mode="w")
        
    def createFolder(self, path):
        """
        create folder if not exists
        """
        if not os.path.exists(path):
            os.makedirs(path)

############## file handling ##############

