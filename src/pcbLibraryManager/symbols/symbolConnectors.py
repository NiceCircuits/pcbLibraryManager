# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 23:09:31 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.symbol import symbol

class symbolConnector(symbol):
    """
    Standard symbol for button
    """
    def __init__(self, name, circuits):
        super().__init__(name)