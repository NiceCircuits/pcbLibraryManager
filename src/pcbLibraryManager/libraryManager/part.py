# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 23:31:59 2015

@author: piotr at nicecircuits.com

Assumptions:
Every part have one symbol
Each part can have multiple footprints

"""
import logging

class part:
    """
    """
    def __init__(self, name):
        self.log=logging.getLogger("part")
        self.log.info("Creating part %s.", name)
        self.name = name
        self.symbol = None
        self.footprints = []