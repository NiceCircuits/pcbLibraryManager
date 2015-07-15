# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 21:27:32 2015

@author: piotr at nicecircuits.com
"""

class pcbLayer:
    """
    """
    topCopper, bottomCopper, topSilk, bottomSilk, topMask, bottomMask,\
        thtPads, thtVias, edges, topNames, bottomNames, topValues, bottomValues,\
        topPaste, bottomPaste, topGlue, bottomGlue, topKeepout, bottomKeepout,\
        topRestrict, bottomRestrict, thtRestrict, thtHoles, topAssembly,\
        bottomAssembly, topDocumentation, bottomDocumentation = range(1, 28)

class pcbPrimitive:
    """
    """
    def __init__(self, layer, width, position, dimensions = [0.0, 0.0], rotation=0.0, filled = False):
        self.layer = layer
        self.width = width
        self.position = position
        self.dimensions = dimensions
        self.rotation = rotation
        self.filled = filled

class pcbPolyline(pcbPrimitive):
    """
    """
    def __init__(self, layer, width, points):
        """
        """
        super().__init__(layer, width, position = None)
        self.points = points

class pcbLine(pcbPolyline):
    """
    """
    def __init__(self, layer, width,x1 = None, y1 = None, x2 = None, y2 = None,  points = []):
        """
        Initialize with points or x1, y1, x2, y2
        """
        if not points:
            points = [[x1, y1], [x2, y2]]
        super().__init__(layer, width, points)

class pcbRectangle(pcbPrimitive):
    """
    """
    def __init__(self, layer, width, position = [], dimensions = [], rotation = 0.0,\
        points = [], x1 = None, y1 = None, x2 = None, y2 = None):
        """
        Initialize with one of options:
        * position and dimensions 
        * points
        * x1, y1, x2, y2
        """
        if not position:
            if points:
                [[x1, y1], [x2, y2]] = points
            position = [(x1 + x2)/2, (y1 + y2)/2]
            dimensions = [abs(x1-x2), abs(y1-y2)]
        super().__init__(layer, width, position, dimensions, rotation=rotation)
