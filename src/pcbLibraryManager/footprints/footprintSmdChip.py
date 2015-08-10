# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 21:45:08 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.defaults import defaults
from libraryManager.footprintPrimitive import *

class footprintSmdChip(footprint):
    """
    Chip component (0603, 0805 etc.)
    """
    def __init__(self, name, size, density, alternativeLibName):
        """
        size: "0603", "0805"
        density: "L" - least, "N" - nominal, "M" - most
        """
        dimensions = {
            '0402':{'chip':[1.1, 0.6], 'pad':{'L':[0.4, 0.6], 'N':[0.5, 0.65], 'M':[0.6, 0.75]}, 'L':{'L':1.1, 'N':1.35, 'M':1.55}, 'court':{'L':0.1, 'N':0.15, 'M':0.2}},
            '0603':{'chip':[1.75, 0.95], 'pad':{'L':[0.8, 0.85], 'N':[1, 0.95], 'M':[1.2, 1.1]}, 'L':{'L':2.05, 'N':2.45, 'M':2.9}, 'court':{'L':0.1, 'N':0.25, 'M':0.5}},
            '0805':{'chip':[2.2, 1.45], 'pad':{'L':[1, 1.35], 'N':[1.2, 1.45], 'M':[1.4, 1.55]}, 'L':{'L':2.5, 'N':2.9, 'M':3.3}, 'court':{'L':0.1, 'N':0.25, 'M':0.5}},
            '1206':{'chip':[3.4, 1.8], 'pad':{'L':[1.1, 1.7], 'N':[1.3, 1.8], 'M':[1.5, 1.9]}, 'L':{'L':3.7, 'N':4.1, 'M':4.5}, 'court':{'L':0.1, 'N':0.25, 'M':0.5}},
            '1210':{'chip':[3.4, 2.7], 'pad':{'L':[1.1, 2.6], 'N':[1.3, 2.7], 'M':[1.5, 2.8]}, 'L':{'L':3.7, 'N':4.1, 'M':4.5}, 'court':{'L':0.1, 'N':0.25, 'M':0.5}},
            '2010':{'chip':[5.15, 2.65], 'pad':{'L':[1.1, 2.55], 'N':[1.3, 2.65], 'M':[1.5, 2.8]}, 'L':{'L':5.45, 'N':5.85, 'M':6.3}, 'court':{'L':0.1, 'N':0.25, 'M':0.5}},
            '2512':{'chip':[6.45, 3.35], 'pad':{'L':[1.1, 3.25], 'N':[1.3, 3.35], 'M':[1.5, 3.5]}, 'L':{'L':6.75, 'N':7.15, 'M':7.6}, 'court':{'L':0.1, 'N':0.25, 'M':0.5}}
            }
        originMarkSize = min(defaults.originMarkSize, dimensions[size]["chip"][1]*0.3)
        super().__init__(name, alternativeLibName, originMarkSize=originMarkSize)
        # pads
        x1=(dimensions[size]["L"][density] - dimensions[size]["pad"][density][0])/2
        for x in [-1,1]:
            self.primitives.append(pcbSmtPad(pcbLayer.topCopper, position=[x1*x,0],\
                dimensions=dimensions[size]["pad"][density], name="1" if x<0 else "2"))
        # body
        self.primitives.append(pcbRectangle(pcbLayer.topAssembly, width=defaults.documentationWidth,\
            position=[0,0], dimensions=dimensions[size]["chip"]))
        # courtyard and silk
        [dim1, dim2]=self.addCourtyardAndSilk([dimensions[size]["L"][density],\
            max(dimensions[size]["pad"][density][1],dimensions[size]["chip"][1])],\
            dimensions[size]["court"][density])
        # name, value
        y = self.valueObject.height + dim1[1]/2
        self.valueObject.position = [0, -y]
        self.nameObject.position = [0, y]
        

if __name__ == "__main__":
    a=footprintSmdChip(0,0,0,0)