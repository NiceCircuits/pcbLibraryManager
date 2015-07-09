# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 22:20:00 2015

@author: piotr at nicecircuits.com
"""
from libraryManager.library import libraryClass

class libraryMosfet(libraryClass):
    """
    """
    def __init__(self):
        libraryClass.__init__(self, "niceMosfet")
        self.parts.append()


if __name__ == "__main__":
    lib = libraryMosfet()