# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:06:39 2015

@author: piotr at nicecircuits.com
"""

class footprint:
    """
    """
    def __init__(self, cadPackage, fileName, name = ""):
        self.cadPackage = cadPackage
        self.fileName = fileName
        
class sot23(footprint):
    """
    """
    def __init__(self, cadPackage, fileName, pinCount):
        footprint.__init__(self,cadPackage, fileName)


if __name__ == "__main__":
    print(sot23(None,None,3))