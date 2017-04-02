# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 06:41:54 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from footprints.footprintSmdQuad import *
from footprints.footprintSmdDualRow import *
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *
from parts.icGenerator import icGenerator
from libraryManager.footprint import footprint
import os.path
from libraryManager.generateLibraries import generateLibraries
from libraries.libraryOpamps import symbolOpamp

class libraryTest(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("Test")
# ============== R7F7010343AFP ============== 
        footprints = [footprintSmdQuad("R7F7010343AFP","niceSemiconductors",\
        176,0.5,[25.4,25.4],[1.3,0.3],[24.1,24.1,1.7],defaults.court["N"],\
        [1.0,0.25,1.7/2])]
        path=os.path.join(os.path.dirname(__file__),"R7F7010343AFP.ods")
        #generate quad pin-by-pin symbols
        self.parts.extend(icGenerator.generate(path,pinNames=None,\
            footprints=footprints,symbolType="quad",namePosfix="",size=5600))
# ============== AXK5S60047YG ============== 
        # added as footprints only 
        self.parts[0].footprints.append(footprintAXK5S60047YG())
        self.parts[0].footprints.append(footprintAXK6S60447YG())
# ============== Dummy semiconductor for package generation ============== 
        self.parts.append(partDummySemiconductor())

class partDummySemiconductor(part):
    """
    Dummy part
    """
    def __init__(self, name="Dummy", refDes=defaults.icRefDes):
        super().__init__(name, refDes)
        self.symbols.append(symbolOpamp())
        for density in ["N", "L", "M"]:
            for pinCount in [8, 14, 16]:
                self.footprints.append(footprintSoic(pinCount=pinCount,density=density))
            for pinCount in [3,5,6,8]:
                self.footprints.append(footprintSot23(pinCount=pinCount,density=density))
                self.footprints.append(footprintSc70(pinCount=pinCount,density=density))


class footprintAXK5S60047YG(footprintSmdDualRow):
    """
    Panasonic Narrow Pitch Connector P5KS Socket 60 pin 
    For mated height 4.0 mm, 5.0 mm and 6.0 mm
    Without positioning boss/with direction for protection from reverse mating
    """
    def __init__(self, name="AXK5S60047YG", alternativeLibName="niceConectorsOther", density="N", wide=False):
        super().__init__(name, alternativeLibName,\
            pinCount=60, pitch=0.5,\
            padSpan=4.6,padDimensions=[0.25,2.2],\
            bodyDimensions=[18.40,4.8,3.05],\
            leadDimensions=[0.4,0.2,0.18],\
            court = defaults.court[density],\
            leadStyle="cube_metal")
        pads=["%d"%(2*i+1) for i in range(30)]+["%d"%(60-2*i) for i in range(30)]
        self.renamePads(pads)

class footprintAXK6S60447YG(footprintSmdDualRow):
    """
    Panasonic Narrow Pitch Connector P5KS Header 60 pin 
    For mated height 4.0 mm, 4.5 mm and 7.0 mm
    Without positioning boss/with direction for protection from reverse mating
    """
    def __init__(self, name="AXK6S60447YG", alternativeLibName="niceConectorsOther", density="N", wide=False):
        super().__init__(name, alternativeLibName,\
            pinCount=60, pitch=0.5,\
            padSpan=4.2,padDimensions=[0.25,2.2],\
            bodyDimensions=[18.40,4.4,0.95],\
            leadDimensions=[0.4,0.2,0.23],\
            court = defaults.court[density],\
            leadStyle="cube_metal")
        pads=["%d"%(2*i+1) for i in range(30)]+["%d"%(60-2*i) for i in range(30)]
        self.renamePads(pads)
        self.addSimple3Dbody([0,0],[16.5,1.72,3.3])

class pogoPin(footprint):
    """
    
    """
    def __init__(self, name="AXK5S60047YG", alternativeLibName="niceConectorsOther", density="N", wide=False):
        super().__init__(name, alternativeLibName,\
            pinCount=60, pitch=0.5,\
            padSpan=4.6,padDimensions=[0.25,2.2],\
            bodyDimensions=[18.40,4.8,3.05],\
            leadDimensions=[0.4,0.2,0.18],\
            court = defaults.court[density],\
            leadStyle="cube_metal")
        pads=["%d"%(2*i+1) for i in range(30)]+["%d"%(60-2*i) for i in range(30)]
        self.renamePads(pads)


if __name__ == "__main__":
    generateLibraries([libraryTest()])
