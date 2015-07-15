# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:06:39 2015

@author: piotr at nicecircuits.com
"""

import logging

class footprint:
    """
    """
    layerTopN=0
    layerBottomN=7    
    
    def __init__(self, name, alternativeLibName = ""):
        self.log=logging.getLogger("footprint")
        self.log.debug("Creating footprint %s.", name)
        self.name = name
        self.alternativeLibName = alternativeLibName
        # fields to store name and value text objects
        self.nameObject = []
        self.valueObject = []
        # initialize empty list for storing primitives
        self.primitives = []
        
if __name__ == "__main__":
    pass