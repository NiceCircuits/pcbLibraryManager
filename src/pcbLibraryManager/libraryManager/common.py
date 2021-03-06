# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 23:12:28 2015

@author: piotr at nicecircuits.com
"""

import datetime
import math

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def rectangleToPolyLinePoints(position, dimensions, rotation=0.0):
    # start with unit rectangle
    points = [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5], [-0.5, -0.5]]
    return translatePoints(scalePoints(rotatePoints(points, rotation), dimensions), position)

def rectangleCorners(position, dimensions):
    return [[position[0]-dimensions[0]/2, position[1] - dimensions[1]/2],\
        [position[0]+dimensions[0]/2, position[1] + dimensions[1]/2],]

def polylinePointsToLines(points):
    return [[points[i], points[i+1]] for i in range(len(points)-1)]

def scalePoint(point, scale):
    return scalePoints([point],scale)[0]    
    
def scalePoints(points, scale):
    if not type(scale) is list:
        scale = [scale, scale]
    return [[x*scale[0], y*scale[1]] for x,y in points]

def rotatePoint(point, rotation):
    return rotatePoints([point], rotation)[0]
    
def rotatePoints(points, rotation):
    ret=[]
    for p in points:
        if p:
            if len(p)==3:
                (x,y,z)=p
                p3d=True
            else:
                x,y=p
                p3d=False
            rho, phi = cart2pol(x, y)
            phi = phi + rotation
            x, y = pol2cart(rho, phi)
            if p3d:
                ret.append([x,y,z])
            else:
                ret.append([x,y])
        else:
            ret.append(p)
    return ret

def translatePoint(point, translation):
    if point:
        return translatePoints([point], translation)[0]
    else:
        return point

def translatePoints(points, translation):
    if len(points[0])==2:
        return [[x+translation[0], y+translation[1]] for x,y in points]
    elif len(points[0])==3:
        if len(translation)==2:
            translation.append(0)
        return [[x+translation[0], y+translation[1], z+translation[2]] for x,y,z in points]
    else:
        raise ValueError("invalid points")

def mirrorPoint(point, axis):
    if axis=="X":
        point[0]=-point[0]
    elif axis=="Y":
        point[1]=-point[1]
    else:
        raise ValueError("unsupported mirror axis %s" % axis)

def mirrorPoints(points, axis):
    return [mirrorPoint(p, axis) for p in points]

def cos(x):
    return math.cos(math.radians(x))

def sin(x):
    return math.sin(math.radians(x))

def almostEqual(a, b, thr=0.001):
    if (a > b-thr) and  (a < b+thr):
        return True
    else:
        return False
    
def cart2pol(x, y):
    rho = math.sqrt(x**2 + y**2)
    phi = math.degrees(math.atan2(y, x))
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * math.cos(math.radians(phi))
    y = rho * math.sin(math.radians(phi))
    return(x, y)

def mil(x):
    "Convert mil to mm"
    return x*0.0254

def mm2inch(x):
    "Convert mm to inch"
    return x/25.4

def isIterable(x):
    return hasattr(x, '__iter__')

def isArray(x):
    return not hasattr(x, "strip") and \
        (hasattr(x, "__getitem__") or hasattr(x, "__iter__"))


class textAlign:
    """
    """
    center, centerLeft, centerRight, topCenter, topLeft, topRight,\
        bottomCenter, bottomLeft, bottomRight = range(9)

if __name__ == "__main__":
    print(timestamp())