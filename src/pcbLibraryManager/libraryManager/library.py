# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 22:08:36 2015

@author: piotr at nicecircuits.com

- Library contains some parts with defined footprint and symbols.
- 

"""

import logging

class libraryClass:
    """
    Create library files. Virtual class.
    """
    def __init__(self, name):
        self.log = logging.getLogger("library")
        self.log.info("Creating library %s.", name)
        self.name = name
        self.parts=[] # initialize list of parts to be filled by children
        