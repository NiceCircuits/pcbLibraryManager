# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:19:03 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.symbol import symbol

class symbolButton(symbol):
    """
    Standard symbol for button
    """
    def __init__(self, name):
        super().__init__(name)