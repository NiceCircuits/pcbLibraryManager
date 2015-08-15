# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 21:27:32 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.common import textAlign

class pcbLayer:
    """
    """
    topCopper, bottomCopper, topSilk, bottomSilk, topMask, bottomMask,\
        thtPads, thtVias, edges, topNames, bottomNames, topValues, bottomValues,\
        topPaste, bottomPaste, topGlue, bottomGlue, topKeepout, bottomKeepout,\
        topRestrict, bottomRestrict, thtRestrict, thtHoles, topAssembly,\
        bottomAssembly, topDocumentation, bottomDocumentation, topCourtyard,\
        bottomCourtyard= range(1, 30)

class padShape:
    """
    """
    rect, round, roundRect = range(3)

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
    def __init__(self, layer, width, x1 = None, y1 = None, x2 = None, y2 = None,\
        position = [], dimensions = [], rotation = 0.0, points = []):
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

class pcbText(pcbPrimitive):
    """
    """
    def __init__(self, layer, width, text, position, height, rotation = 0.0,\
        align=textAlign.center, mirror=False):
        """
        """
        self.text = text
        self.align = align
        self.mirror = mirror
        self.height = height
        super().__init__(layer, width, position, rotation=rotation)
        
class pcbSmtPad(pcbPrimitive):
    """
    """
    def __init__(self, layer, position, dimensions, name, rotation = 0.0):
        """
        """
        super().__init__(layer, width=0, position=position, dimensions=dimensions,\
            rotation=rotation, filled=True)
        self.name=name

class pcbThtPad(pcbPrimitive):
    """
    """
    def __init__(self, position, dimensions, drill, name, shape=padShape.round, rotation = 0.0):
        """
        """
        super().__init__([], width=0, position=position, dimensions=dimensions,\
            rotation=rotation, filled=True)
        self.name=name
        self.shape = shape
        self.drill = drill

class pcbCircle(pcbPrimitive):
    """
    """
    def __init__(self, layer, width, position, radius, filled=False):
        """
        """
        super().__init__(layer, width, position, filled=filled)
        self.radius=radius

class pcbArc(pcbPrimitive):
    """
    """
    def __init__(self, layer, width, position, radius, angles):
        """
        """
        super().__init__(layer, width, position)
        self.radius=radius
        self.angles=angles

class pcb3DBody(pcbPrimitive):
    """3D Body
    """
    def __init__(self, name, position, dimensions, rotations=[0,0,0]):
        """
        """
        if len(position)==2:
            position=position + [0]
        if len(dimensions)==2:
            dimensions=dimensions+[1]
        super().__init__(None, 0, position)
        self.dimensions=dimensions
        self.rotations=rotations
        self.name=name