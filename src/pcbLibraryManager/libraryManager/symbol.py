# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 23:41:16 2015

@author: piotr at nicecircuits.com
"""

import logging

class symbol:
    """
    """
    def __init__(self, name):
        self.log=logging.getLogger("symbol")
        self.log.debug("Creating symbol %s.", name)
        self.name = name