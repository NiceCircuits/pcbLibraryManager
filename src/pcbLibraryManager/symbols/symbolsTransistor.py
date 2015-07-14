# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 23:50:39 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.symbol import symbol

class symbolMosfet(symbol):
    """
    Standard symbol for mosfet (3 pin with diode)
    """
    def __init__(self, name):
        super().__init__(self, name)