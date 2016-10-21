# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 21:13:05 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.footprint import footprint
from libraryManager.defaults import defaults
from libraryManager.footprintPrimitive import *
from math import floor, sqrt

class footprintSmdPower(footprint):
    """SMD high power footprint generator (D-Pak, D2Pak, SOT223 etc.)
    """
    def __init__(self, name, bodySize, pitch, padSize, padOffset, leadSize,\
    tabSize, tabPadSize, tabPadOffset, pads=2, court=0.5, stubSize=None,\
    tabShape="cube", leadShape="gullwing", alternativeLibName="niceSemiconductors"):
        super().__init__(name, alternativeLibName)
        # body
        self.addSimple3Dbody([0,0], bodySize)
        # tab
        tabNumber=floor(pads/2+1)
        self.primitives.append(pcbSmtPad(pcbLayer.topCopper,[0, tabPadOffset],\
            tabPadSize, tabNumber))
        self.addLead([0, bodySize[1]/2+tabSize[0]/2], tabSize, lead=tabShape, rotation=90)
        # pads
        iX = [-a for a in range(tabNumber-1,0,-1)] + [a for a in range(tabNumber)]
        stub = (pads%2)==0
        for i in iX:
            if i==0 and stub:
                # stub
                self.addSimple3Dbody([0,-(bodySize[1]+stubSize[1])/2,\
                    leadSize[2]-stubSize[2]], stubSize, file="cube_metal")
            else:
                # pin
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper,[pitch*i, padOffset],\
                    padSize,i+tabNumber))
                self.addLead([pitch*i,-(bodySize[1]+leadSize[0])/2], leadSize, rotation=270)
        # courtyard and silk
        dim=[max(bodySize[0], tabPadSize[0]),\
            (tabPadSize[1]+padSize[1])/2-padOffset+tabPadOffset]
        offsetY=((tabPadSize[1]-padSize[1])/2+padOffset+tabPadOffset)/2
        self.addCourtyardAndSilk(dim, court, offset=[0,offsetY])
        # name, value


class footprintDPak(footprintSmdPower):
    """D-Pak (TO 252)
    """
    def __init__(self, pins=3, name="", density="N", alternativeLibName="niceSemiconductors"):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            if pins==3:
                name = "D-PAK_%s" % density
            else:
                name = "D-PAK-%d_%s" % (pins,density)
        
        padSize = {3:{"L":[1.2,2], "N":[1.5,2.5], "M":[2,3]},
                      5:{"L":[0.8,2.2], "N":[0.8,2.5], "M":[0.95,3]}}
        padOffset ={"L":-5.3,"N":-5.1,"M":-5.2}
        tabPadSize = {"L":[7.0,6.5], "N":[7.0,7.0], "M":[7.0,7.0]}
        tabPadOffset ={"L":1.55,"N":1.8,"M":1.8}
        pitch={3:2.27,5:1.135}
        super().__init__( name,\
            bodySize=[6.8, 6.3, 2.4],\
            pitch=pitch[pins],\
            padSize = padSize[pins][density],\
            padOffset = padOffset[density],\
            leadSize = [2.95, 0.95, 1.8],\
            tabSize = [1.2, 5.65, 0.6],\
            tabPadSize = tabPadSize[density],\
            tabPadOffset = tabPadOffset[density],\
            pads=pins-1,\
            court=defaults.court[density],\
            stubSize=[0.95, 1.2, 0.6],\
            tabShape="cube_metal",\
            leadShape="gullwing",
            alternativeLibName=alternativeLibName)

class footprintSot223(footprintSmdPower):
    """SOT223
    """
    def __init__(self, name="", density="N", alternativeLibName="niceSemiconductors"):
        """
        density: "L" - least, "N" - nominal, "M" - most
        """
        if not name:
            name = "SOT223_%s" % density
        
        padSize = {"L":[1.1,1.6], "N":[1.4,2.2], "M":[1.6,2.4]}
        padOffset = {"L":-3.1,"N":-3.1,"M":-3.2}
        tabPadSize = {"L":[3.4,1.6], "N":[3.7,2.2], "M":[4,2.4]}
        super().__init__( name,\
            bodySize=[6.7, 3.7, 1.8],\
            pitch=2.3,\
            padSize = padSize[density],\
            padOffset = padOffset[density],\
            leadSize = [1.8, 0.85, 0.7],\
            tabSize = [1.8, 3.1, 0.7],\
            tabPadSize = tabPadSize[density],\
            tabPadOffset = -padOffset[density],\
            pads=3,\
            court=defaults.court[density],\
            stubSize=[0.95, 1.2, 0.6],\
            tabShape="gullwing",\
            leadShape="gullwing",
            alternativeLibName=alternativeLibName)

class footprintSot89(footprint):
    """SOT89
    """
    def __init__(self, name="", density="N", alternativeLibName="niceSemiconductors"):
        if not name:
            name = "SOT89_%s" % density
        super().__init__(name, alternativeLibName)
        # body
        self.addSimple3Dbody([0,0], [4.8,2.8,1.75])
        # tab
        tabPadOffset={"L":0.8,"N":0.8,"M":1.05}
        tabPadSize={"L":[1.9,2.5],"N":[2,2.5],"M":[2,3]}
        self.addSimple3Dbody([0,1.675], [1.8,0.55,0.5], file="cube_metal")
        self.primitives.append(pcbSmtPad(pcbLayer.topCopper,[0, tabPadOffset[density]],\
            tabPadSize[density], 2))
        self.primitives.append(pcbSmtPad(pcbLayer.topCopper,[0, -0.45],\
            [tabPadSize[density][0]/sqrt(2),tabPadSize[density][0]/sqrt(2)], 2,\
            rotation=45.0))
        # pads
        padOffset={"L":-1.65,"N":-1.7,"M":-1.75}
        padSize={"L":[0.55,1.4],"N":[0.6,1.5],"M":[0.7,1.6]}
        for i in [-1,0,1]:
                # pin
                self.primitives.append(pcbSmtPad(pcbLayer.topCopper,[1.5*i, padOffset[density]],\
                    padSize[density],i+2))
                self.addSimple3Dbody([1.5*i,-1.85], [0.5,0.9,0.5], file="cube_metal")
        # courtyard and silk
        #dim=[max(bodySize[0], tabPadSize[0]),\
        #    (tabPadSize[1]+padSize[1])/2-padOffset+tabPadOffset]
        #offsetY=((tabPadSize[1]-padSize[1])/2+padOffset+tabPadOffset)/2
        #self.addCourtyardAndSilk(dim, court, offset=[0,offsetY])
