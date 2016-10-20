# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 19:12:55 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from symbols.symbolsIC import symbolIC
from libraryManager.defaults import defaults
from libraryManager.symbolPrimitive import *
from libraryManager.footprintPrimitive import *
from libraryManager.part import part
from libraryManager.footprint import footprint
from libraryManager.generateLibraries import generateLibraries

class libraryConnectorsOther(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceConectorsOther")
        self.parts.append(partConnUsb(""))
        for smd in [True,False]:
            self.parts.append(partConnJack(smd=smd))


class partConnUsb(part):
    """
    Straight Nigini NS25 connector
    """
    def __init__(self, connType):
        if connType:
            name = "connUsb-%s" %(connType)
        else:
            name="connUsb"
        super().__init__(name, defaults.conRefDes)
        pins = [
            ['5V', 1, pinType.passive],
            ['D-', 2, pinType.passive],
            ['D+', 3, pinType.passive],
            ['GND', 4, pinType.passive],
            ['GND', 0, pinType.passive]
        ]
        self.symbols.append(symbolIC("connUsb", [], pins, 400, defaults.conRefDes))
        if connType:
            pass

class partConnJack(part):
    """
    Stereo jack connector
    """
    def __init__(self, name="", smd=True):
        if not name:
            name = "jack_narrow_%s" %("smd" if smd else "tht")
        super().__init__(name, defaults.conRefDes)
        self.symbols.append(sybolJack())
        self.footprints.append(footprintJackNarrow(smd=smd))
        
class sybolJack(symbolIC):
    """
    Stereo jack connector
    """
    def __init__(self):
        pins = [
            ['R', 2, pinType.passive],
            ['L', 3, pinType.passive],
            ['GND', 1, pinType.passive],
        ]
        super().__init__("jack", [], pins, 400, defaults.conRefDes,\
        showPinNames=False)
        self.primitives.append(symbolPolyline(defaults.symbolLineWidth,\
            [[200,0],[150,0],[100,50],[50,0]]))
        self.primitives.append(symbolPolyline(defaults.symbolLineWidth,\
            [[200,100],[50,100],[0,50],[-50,100]]))
        self.primitives.append(symbolPolyline(defaults.symbolLineWidth,\
            [[200,-100],[-150,-100],[-150,100],[-100,100],[-100,0],[-150,0]]))

class footprintJackNarrow(footprint):
    """Narrow 3.5 jack THT
    """
    def __init__(self, density ="N", name="", smd=True,\
        alternativeLibName="niceConectorsOther"):
        if not name:
            name = "Jack_Narrow_%s_%s" % ("smd" if smd else "tht", density)
        super().__init__(name, alternativeLibName)
        #body
        self.addSimple3Dbody([0.8,0,0],[11.6,6.3,5.1],silk=True)
        self.addSimple3Dbody([-6.3,0,0],[2.6,5.1,5.1],silk=True)
        # pads
        posx={0:-3.2,1:0,2:3.5}
        for x in range(3):
            for y in [-1,1]:
                if smd:
                    self.primitives.append(pcbSmtPad(pcbLayer.topCopper,\
                    [posx[x],3.325*y],[2,-2.85],str(x+1)))
                    self.addSimple3Dbody([posx[x],3.55*y,0],[1,0.9,0.3],file="cube_metal")
                else:
                    self.primitives.append(pcbThtPad(\
                    [posx[x],2.875*y],[2.7,2.2],1.7,str(x+1)))
                    self.addSimple3Dbody([posx[x],2.875*y,-3],[1,0.8,3],file="cube_metal")
                    
if __name__ == "__main__":
    generateLibraries([libraryConnectorsOther()])