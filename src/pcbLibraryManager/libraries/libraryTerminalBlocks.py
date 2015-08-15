# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 17:51:53 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from libraryManager.common import *
from symbols.symbolsConnectors import symbolConnector
from footprints.footprintConnectors import footprintConnectorTht
from math import sqrt

class libraryTerminalBlocks(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceTerminalBlocks")
        for rows in range(1,11):
            for pitch in [3.5, 5.0]:
                self.parts.append(partScrewTerminal(rows, pitch))
            for pitch in [5.08]:
                self.parts.append(partEDG(rows, pitch))
        
class partScrewTerminal(part):
    """Screw terminal block connector part generator
    """
    def __init__(self, rows, pitch, name=""):
        if not name:
            name = "Screw_Terminal-%1.2fmm-%d" % (pitch, rows)
        super().__init__(name, "CON")
        self.symbols.append(symbolConnector(rows))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintScrewTerminal(rows, pitch, density))

class partEDG(part):
    """Pluggable terminal block connector part generator
    """
    def __init__(self, rows, pitch, name=""):
        if not name:
            name = "EDG-%1.2fmm-%d" % (pitch, rows)
        super().__init__(name, "CON")
        self.symbols.append(symbolConnector(rows))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintEDG(rows, pitch, density))

class footprintScrewTerminal(footprintConnectorTht):
    """Screw terminal block connector footprint generator
    """
    def __init__(self, rows, pitch, density ="N", name="", alternativeLibName="niceTerminalBlocks",\
        originMarkSize=0, textOnSilk=True):
        court={"L":0.7, "N":0.7, "M":1}
        dim={3.5:{"L":[1.7, 1.7],"N":[2.2, 2.0],"M":[2.5,2.5]},\
            5.0:{"L":[2, 2],"N":[2.5, 2.2],"M":[3, 3]}}
        drill={3.5:1.2, 5.0:1.4}
        bodyXSize={3.5:7.0, 5.0:7.8}
        bodyHeight={3.5:9.0, 5.0:10.5}
        bodyXOffset={3.5:0, 5.0:0}
        pinDimensions={3.5:[0.75,0.75,3.4], 5.0:[1,1,4.4]}
        shape={"L":padShape.round, "N":padShape.roundRect, "M":padShape.round}
        if not name:
            name = "Screw_Terminal-%1.2fmm-%d_%s" % (pitch, rows, density)
        super().__init__(1, rows, pitch, dim[pitch][density], shape[density], drill[pitch],\
            name=name, alternativeLibName=alternativeLibName, court=court[density],\
            bodySize=[bodyXSize[pitch], pitch*rows], bodyOffset=[bodyXOffset[pitch],0],\
            keySize=-1, bodyHeight=bodyHeight[pitch], pinDimensions=pinDimensions[pitch],\
            pinZOffset=-pinDimensions[pitch][2])
        # drawing
        for i in range(rows):
            y=(rows/2-1/2-i)*pitch
            # front size markers
            self.primitives.append(pcbRectangle(pcbLayer.topSilk, defaults.silkWidth,\
                dimensions=[1, pitch*0.8],\
                position=[-bodyXSize[pitch]/2+bodyXOffset[pitch]+0.5, y]))
            # screw drawing
            self.primitives.append(pcbCircle(pcbLayer.topAssembly, defaults.documentationWidth,\
                [0, y], pitch*0.35))
            k=pitch*0.35*sqrt(2)/2
            self.primitives.append(pcbLine(pcbLayer.topAssembly,defaults.documentationWidth,\
                -k, y-k, k, y+k))

class footprintEDG(footprintConnectorTht):
    """Pluggable terminal block connector footprint generator
    """
    def __init__(self, rows, pitch, density ="N", name="", alternativeLibName="niceTerminalBlocks",\
        originMarkSize=0, textOnSilk=True):
        court={"L":0.7, "N":0.7, "M":1}
        dim={5.08:{"L":[2.1, 2.1],"N":[2.6, 2.3],"M":[3, 3]}}
        drill={5.08:1.5}
        bodyXSize={5.08:12.4}
        bodyXOffset={5.08:-4.9}
        bodyHeight={5.08:8.5}
        plugHeight={5.08:15.5}
        plugXsize={5.08:10.3}
        pinDimensions={5.08:[1,1,4]}
        shape={"L":padShape.round, "N":padShape.roundRect, "M":padShape.round}
        if not name:
            name = "EDG-%1.2fmm-%d_%s" % (pitch, rows, density)
        super().__init__(1, rows, pitch, dim[pitch][density], shape[density], drill[pitch],\
            name=name, alternativeLibName=alternativeLibName, court=court[density],\
            bodySize=[bodyXSize[pitch], pitch*rows], bodyOffset=[bodyXOffset[pitch],0],\
            keySize=-1, bodyHeight=bodyHeight[pitch], pinDimensions=pinDimensions[pitch],\
            pinZOffset=-pinDimensions[pitch][2])
        self.valueObject.position[0]+=0.5
        # drawing
        x=-bodyXSize[pitch]/2+bodyXOffset[pitch]-plugXsize[pitch]/2
        self.addSimple3Dbody([x,0], [plugXsize[pitch], pitch*rows, plugHeight[pitch]])
        for i in range(rows):
            y=(rows/2-1/2-i)*pitch
            # front size markers
            self.primitives.append(pcbRectangle(pcbLayer.topAssembly, defaults.documentationWidth,\
                dimensions=[1, pitch*0.8], position=[x-plugXsize[pitch]/2+0.5, y]))
            # screw drawing
            self.primitives.append(pcbCircle(pcbLayer.topAssembly, defaults.documentationWidth,\
                [x, y], pitch*0.35))
            k=pitch*0.35*sqrt(2)/2
            self.primitives.append(pcbLine(pcbLayer.topAssembly,defaults.documentationWidth,\
                x-k, y-k, x+k, y+k))