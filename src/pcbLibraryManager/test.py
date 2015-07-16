# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:46:18 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.common import *
import math

points = [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [-0.5, -0.5]]

print(polylinePointsToLines(points))
