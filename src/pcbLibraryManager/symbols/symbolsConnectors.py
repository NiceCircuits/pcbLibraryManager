# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 17:53:59 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.defaults import *
from libraryManager.common import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *

class symbolConnector(symbolIC):
    """Connector symbol
    
    :param rows: row count, 1..inf
    :param cols: column count - 1 (default) or 2
    :param name: name of symbol. Defults to "*CON-* **C** x **R**"
    :rtype: list of strings
    """
    def __init__(self, rows, cols=1, name="", refDes="CON", showPinNames=False,\
        showPinNumbers=True, offset=0):
        if not name:
            name="CON-%dx%d" % (cols, rows)
        pinsRight = [(['%d' % (row * cols + 2), row * cols + 2, pinType.passive] if cols>1 else None) for row in range(rows)]
        pinsLeft = [['%d' % (row * cols + 1), row * cols + offset + 1, pinType.passive] for row in range(rows)]
        super().__init__(name, pinsLeft, pinsRight, 400, refDes, showPinNames, showPinNumbers)