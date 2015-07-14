# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:10:58 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.cadPackage import cadPackage
from libraryManager.library import  libraryClass
import os.path
from libraryManager.common import *

class KiCad(cadPackage):
    """
    KiCad CAD package handling class
    """
    def __init__(self):
        super().__init__()
        
    def generateLibrary(self, library, path):
        super().generateLibrary(library, path)
        file = self.openFile(os.path.join(path, library.name + ".lib"))
            