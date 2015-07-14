# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 21:27:32 2015

@author: piotr at nicecircuits.com
"""

class primitive:
    """
    """
    def __init__(self, width, position, dimensions = [0.0, 0.0], rotation=0.0, filled = False):
        self.width = width
        self.position = position
        self.dimensions = dimensions
        self.rotation = rotation
        self.filled = filled

class polyline(primitive):
    """
    """
    def __init__(self, width, points):
        """
        """
        super().__init__(self, width, position = None)
        self.points = points

class line(polyline):
    """
    """
    def __init__(self, width, points = [], x1 = None, y1 = None, x2 = None, y2 = None):
        """
        Initialize with points or x1, y1, x2, y2
        """
        if not points:
            points = [[x1, y1], [x2, y2]]
        super().__init__(self, width, points)

class rectangle(primitive):
    """
    """
    def __init__(self, width, position = [], dimensions = [], points = [], 
                 x1 = None, y1 = None, x2 = None, y2 = None):
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
        super().__init__(self, width, position, dimensions)
