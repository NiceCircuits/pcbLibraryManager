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
    """Describe part
    
    :param name: Name of part
    :refDes: Default reference designator, without number, like: "R", "C", "T"
    :description: Description of part to copy to library file
    :datasheet: Path to datasheet of part
    """
    def __init__(self, name, refDes, description="", datasheet=""):
        self.log=logging.getLogger("part")
        self.log.info("Creating part %s.", name)
        self.name = name
        self.refDes=refDes
        # can have many symbols (gates)
        self.symbols = []
        # can have many footprints
        self.footprints = []
        self.description=description
        self.datasheet=datasheet