# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 22:08:36 2015

@author: piotr at nicecircuits.com

- Library contains some parts with defined footprint and symbols.
- 

"""

class libraryClass:
    """
    Create library files. Virtual class.
    """
    def __init__(self, name):
        self.parts={} # initialize dictionary of parts to be filled by children
        