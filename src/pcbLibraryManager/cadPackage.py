# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 18:57:55 2015

@author: piotr at nicecircuits.com


Assumptions:
default units are mm and degrees

"""

def convertRectangleCenterToVertices(position, dimensions):
    x1 = float(position(0)) - float(dimensions(0))/2.0
    x2 = float(position(0)) + float(dimensions(0))/2.0
    y1 = float(position(1)) - float(dimensions(1))/2.0
    y2 = float(position(1)) + float(dimensions(1))/2.0
    return ((x1, y1), (x2,y2))

def convertRectangleVerticiesToCenter(point1,point2):
    posX = (float(point1(0)) + float(point2(0)))/2.0
    posY = (float(point1(1)) + float(point2(1)))/2.0
    dimX = abs(float(point1(0)) - float(point2(0)))
    dimY = abs(float(point1(1)) - float(point2(1)))
    return ((posX, posY), (dimX,dimY))
    
def mil(val):
    """convert mil to mm"""
    return float(val) * 0.0254

def inch(val):
    """convert inch to mm"""
    return float(val) * 25.4

class cadPackage:
    """
    """
    def __init__(self):
        pass
    
    def line(self, layer, width, point1, point2):
        pass
    
    def polygon(self, layer, width, points, filled = False):
        pass
    
    def rectangle(self, layer, width, point1, point2, rotation = 0.0, filled = False):
        pass
    
    def rectangle2(self, layer, width, position, dimensions, rotation=0.0, filled = False):
        (point1, point2) = convertRectangleCenterToVertices(position, dimensions)
        self.rectangle(layer, point1, point2, rotation, filled)
    
    def circle(self, layer, width, position, radius, filled = False):
        pass
    
    def arc(self, layer, width, position, radius, angle1, angle2, filled = False):
        pass
    
    def padSmdRect(self, layer, position, dimensions, rotation = 0.0, \
    roundness = 0.0, maskClearance = None, pasteClearance = None, thermals = False):
        pass

    def padSmdRound(self, layer, position, radius, maskClearance = None, \
    pasteClearance = None, thermals = False):
        pass

class KiCad(cadPackage):
    """
    """
    def __init__(self):
        cadPackage.__init__(self)


if __name__ == "__main__":
    a = KiCad()
    print(a.rectangle)