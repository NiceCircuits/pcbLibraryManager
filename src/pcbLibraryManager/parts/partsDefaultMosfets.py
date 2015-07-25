# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 23:36:58 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.part import part
from symbols.symbolsTransistor import *
from libraryManager.defaults import defaults

class partDefaultMosfetSot23(part):
    """
    Default mosfet in SOT23 package 
    """
    def __init__(self):
        part.__init__(self, "NMOS", defaults.transistorRefDes)
        self.symbol = symbolMosfet()
    
if __name__ == "__main__":
    partDefaultMosfetSot23()