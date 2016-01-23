# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 14:27:28 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.symbol import symbol
from libraryManager.symbolPrimitive import *
from libraryManager.defaults import defaults
from libraryManager.part import part
from symbols.symbolsIC import *
from footprints.footprintSmdQuad import footprintQfp
from libraryManager.footprintPrimitive import *
import pyexcel_ods3
import numpy as np

class icGenerator():
    """
    universal generator for IC symbols from xls files
    """
    def generate(fileName, pinNames=[], footprints=[], namePosfix="", symbolType="dual",size=0):
        """
        generate one or many parts from pinout file
        fileName: name of file with pinouts
        pinNames: pin configuration: [[pins left], [pins right],...[pins left], [pins right]]
            like: [["1","2","3"],["6","5","4"]] or [["1","2"],["6","5"],["4","7"],["8","9"]]
        footprints: list of footprint objects
        namePostfix: postfix to IC name read from pinout
        """
        pinout=icGenerator.loadPinout(fileName)
        ret=[]
        if not pinNames:
            #auto generate
            if symbolType=="quad":
                nPins=len(pinout[0]["pins"])
                nSide=int((nPins)/4)
                #if additional pin above N*4 (thermal pad)
                plus=((nPins%4)>0)*1
                pinNames=np.array([[None]*(nSide+plus)]*4)
                for side in range(4):
                    for i in range(nSide):
                        pinNames[side,i]=pinout[0]["pins"][i+side*nSide]
                if plus:
                    pinNames[3,nSide]=pinout[0]["pins"][nPins-1]
            else:
                raise ValueError("Auto pinout for %s symbol type not implemented yet!" % symbolType)
        #for each pinout variant
        for v in pinout:
            # generate symbol(s)
            symbols=[]
            pins=[]
            for pinNameCol in pinNames:
                pinCol = []
                for p in pinNameCol:
                    if p:
                        p=str(p)
                        pinCol.append([v["pinNames"][p], p, v["pinTypes"][p]])
                    else:
                        pinCol.append(None)
                pins.append(pinCol)
            if symbolType=="dual":
                #for 1..2 pin columns - one symbol, for 2..3 - 2 etc.
                nSymbols = int((len(pinNames)+1)/2)
                for i in range(nSymbols):
                    if nSymbols>1:
                        symPostfix = "_%d" % i
                    else:
                        symPostfix = ""
                    symbols.append(symbolIC(v["name"]+symPostfix+namePosfix, pinsLeft=pins[i*2], pinsRight=pins[i*2+1],\
                        width=size, refDes=defaults.icRefDes,showPinNames=True, showPinNumbers=True))
            elif symbolType=="quad":
                symbols.append(symbolICquad(v["name"]+namePosfix,\
                    pins=pins,size=size))
            else:
                raise ValueError("invalid symbolType: %s!" % symbolType)
            for p in v["partNames"]:
                _part = part(p+namePosfix, defaults.icRefDes)
                _part.symbols.extend(symbols)
                _part.footprints.extend(footprints)
                ret.append(_part)
        return ret
        
    def loadPinout(fileName):
        """
        Load pinout from ods file.
        """
        try:
            sheet = np.array(pyexcel_ods3.get_data(fileName)["pinout"])
            test=sheet[:,0] #check proper conversion to numpy.array
        except Exception as ex:
            print("Error! Maybe sheet contains empty cells (especially at ends of rows)?")
            raise ex
        rowV = sheet[0]
        nVersions = int((len(rowV)-1)/2)
        ret=[0]*nVersions #initialize return structure
        for nV in range(nVersions):
            ret[nV]={}
            ret[nV]["name"]=rowV[nV*2+2]
            partNames=sheet[1,nV*2+2]
            partNames=partNames.split("\n")
            ret[nV]["partNames"]=partNames
            ret[nV]["pins"]=sheet[2:,0]
            pinTypes=sheet[2:,nV*2+1]
            pinNames=sheet[2:,nV*2+2]
            ret[nV]["pinTypes"]={}
            ret[nV]["pinNames"]={}
            for i in range(len(ret[nV]["pins"])):
                ret[nV]["pinTypes"][ret[nV]["pins"][i]]=pinType.fromStr[pinTypes[i]]
                ret[nV]["pinNames"][ret[nV]["pins"][i]]=pinNames[i]
        return ret
    
    def _testLoadPinout():
        """
        test for loadPinout function
        """
        print(icGenerator.loadPinout("pinoutTest.ods"))

    def _testGenerate():
        """
        test for generate function
        """
        fp=[footprintQfp(32, 0.8, density=density) for density in ["N", "L", "M"]]
        pins=[["1","2",None,"3","4"],["5","6","7","8"]]
        print(icGenerator.generate("pinoutTest.ods",pins,fp,""))

    def _testGenerate2():
        """
        test for generate function
        """
        print(icGenerator.generate("pinoutTest.ods",symbolType="quad"))

if __name__ == "__main__":
    icGenerator._testGenerate2()
    
    