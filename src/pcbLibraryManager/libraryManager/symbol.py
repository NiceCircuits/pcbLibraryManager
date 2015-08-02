# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 23:41:16 2015

@author: piotr at nicecircuits.com
"""

import logging
from libraryManager.symbolPrimitive import *
from libraryManager.defaults import defaults
from libraryManager.common import *


class symbol:
    """
    """
    def __init__(self, name, refDes="U", showPinNames=True, showPinNumbers=True):
        self.log=logging.getLogger("symbol")
        self.log.debug("Creating symbol %s.", name)
        self.name = name
        self.showPinNames=showPinNames
        self.showPinNumbers=showPinNumbers
        # fields to store name and value text objects - can be changed later
        self.nameObject = symbolText(refDes,\
            [0, defaults.symbolTextHeight * 2], defaults.symbolTextHeight, align = textAlign.center)
        self.valueObject = symbolText(name,\
            [0, 0], defaults.symbolTextHeight, align = textAlign.center)
        # initialize empty list for storing primitives and pins
        self.primitives = []
        self.pins = []

if __name__ == "__main__":
    pass