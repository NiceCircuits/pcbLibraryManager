# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 06:41:54 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from footprints.footprintSmdQuad import footprintQfp
from footprints.footprintSmdDualRow import footprintTssop
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *
from parts.icGenerator import icGenerator
import os.path
from libraryManager.generateLibraries import generateLibraries

class librarySTM32(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSTM32")
# ============== STM32 LQFP64 ============== 
        pinNames=[
[None,"14","15","16","17","20","21","22","23","41","42","43","44","45","46","49","50",None,"54"],
[None,"26","27","28","55","56","57","58","59","61","62","29","30","33","34","35","36"],
["7","60",None,"1",None,"13",None,"32","64","48","19",None,None,"12",None,"31","63","47","18",],
["8","9","10","11","24","25","37","38","39","40","51","52","53","2","3","4",None,"5","6"]
        ]
        footprints = [footprintQfp(64, 0.5, density=density) for density in ["N", "L", "M"]]
        path=os.path.join(os.path.dirname(__file__),"STM32_LQFP64.ods")
        #generate symbols configured by pinNames
        self.parts.extend(icGenerator.generate(path,pinNames,footprints,size=3000))
        #generate quad pin-by-pin symbols
        self.parts.extend(icGenerator.generate(path,pinNames=None,\
            footprints=footprints,symbolType="quad",namePosfix="_q",size=3100))

# ============== STM32 TSSOP20 ============== 
        pinNames=[
["4","1",None,"5","16",None,None,None,None,"2","3",None,"15"],
["6","7","8","9","10","11","12","13","17","18","19","20","14"]
        ]
        footprints = [footprintTssop(20, density=density) for density in ["N", "L", "M"]]
        path=os.path.join(os.path.dirname(__file__),"STM32_TSSOP20.ods")
        #generate symbols configured by pinNames
        self.parts.extend(icGenerator.generate(path,pinNames,footprints,size=2000))

if __name__ == "__main__":
    generateLibraries([librarySTM32()])