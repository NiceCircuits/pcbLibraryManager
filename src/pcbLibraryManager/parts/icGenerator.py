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
from footprints.footprintSmdQuad import *
from libraryManager.footprintPrimitive import *
import pyexcel_ods3
import numpy as np

test_path=r"D:\pcbLibraryManager\src\pcbLibraryManager\libraries\STM32_LQFP48.ods"
    
class icGenerator():
    """
    universal generator for IC symbols from xls files
    """
    def generate_advanced(pinout_file_name, symbol_file_name="", footprint_file_name=""):
        """
        generate one or many parts from pinout file. Read more data from file.
        pinout_file_name: name of file with pinouts
        symbol_file_name: name of file with symbols
        footprint_file_name: name of file with footprints
        """
        ret=[]
        if symbol_file_name=="":
            symbol_file_name = pinout_file_name
        if footprint_file_name=="":
            footprint_file_name = pinout_file_name
        parts=icGenerator.load_parts_advanced(pinout_file_name)
        for part_descr in parts:
            if part_descr:
                if part_descr[0]:
                    new_part=part(part_descr[0], defaults.icRefDes)
                    symbols = icGenerator.load_symbol_advanced(symbol_file_name, part_descr[1])
                    new_part.symbols.extend(symbols)
                    footprints = icGenerator.load_footprints_advanced(footprint_file_name) #, part_descr[2]
                    new_part.footprints.extend(footprints)
                ret.append(new_part)
        return ret

                    # todo: alternate part
                    #new_part=part(part_descr[0]+"_alt", defaults.icRefDes)
    def load_footprints_advanced(fileName):
        ret=[]
        params = icGenerator.load_ods_section(fileName, "Footprint", \
            stopString="Mechanical", vector=True, dictionary=True)
        mechanical = icGenerator.load_ods_section(fileName, "Footprint", \
            startString="Mechanical", stopString="Footprint", vector=False, dictionary=True)
        footprint = icGenerator.load_ods_section(fileName, "Footprint", \
            startString="Footprint", vector=False, dictionary=True)
        for variant in footprint.keys():
            if params["Type"]=="QFP":            
                ret.append(footprintQfpParametrized(params, mechanical, footprint, variant))
            if params["Type"]=="QFN":            
                ret.append(footprintQfnParametrized(params, mechanical, footprint, variant))
            else:
                raise ValueError("Footprint type %s found in %s unsupported" % (params["Type"], fileName))
        return ret
    
    def test_load_footprints_advanced():
        print(icGenerator.load_footprints_advanced(test_path))

    def load_parts_advanced(fileName):
        """
        Load parts description from pinout file.
        """
        ret = icGenerator.load_ods_section(fileName, "Part", vector=False)
        return ret[1:]
    
    def load_ods_sheet(fileName, sheetName):
        try:
            data = pyexcel_ods3.get_data(fileName)[sheetName]
        except KeyError:
            raise ValueError("No \"%s\" tab found in %s" %(sheetName, fileName))
        except:
            raise ValueError("Error opening file " + fileName)
        return data

    def load_ods_section(fileName, sheetName, startString="", stopString="", \
        vector=False, dictionary=False):
        """
        data:
        a,1
        b,2
        read as vector and dictionary:
        {"a":1' "b":2}
        read vector and not dictionary:
        [["a",1], ["b",2]]
        
        data:
        ,v1,v2
        a,1,2
        b,3,4,5,6
        read as not vector and not dictionary:
        [[,"v1","v2"],
        ["a",1,2],
        ["b",3,4]]
        read as not vector and dictionary:
        {"v1":{"a":1,"b":3},
        "v2":{"a":2,"b":4}}
        """
        if dictionary:
            output={}
        elif vector:
            output=[]
        else:
            output=[[]]
        data=icGenerator.load_ods_sheet(fileName, sheetName)
        header = True
        variants=[]
        if startString:
            save_data=False
        else:
            save_data=True
        for line in data:
            if line and save_data:
                if stopString and line[0]==stopString:
                    break
                if vector and line[0] and len(line)>=2:
                    if dictionary:
                        output[str(line[0]).strip()]=line[1]
                    else:
                        output.append([str(line[0]).strip(), line[1]])
                elif not vector:
                    if header:
                        header=False
                        start=1 if dictionary else 0
                        for name in line[start:]:
                            name=str(name).strip()
                            if dictionary:
                                output[name]={}
                            else:
                                output[0].append(name)
                            variants.append(name)
                    elif dictionary:
                        for i in range(len(variants)):
                            if i<(len(line)-1):
                                output[variants[i]][line[0]]=line[i+1]
                            else:
                                output[variants[i]][line[0]]=None
                    else:
                        temp=[]
                        for i in range(len(variants)):
                            if i<len(line):
                                temp.append(line[i])
                            else:
                                temp.append(None)
                        output.append(temp)
                else:
                    pass
            else:
                if line:
                    if str(line[0]).strip() == startString:
                        save_data = True
        return output
                
    def test_load_ods_section():
        print(icGenerator.load_ods_section(test_path, "Footprint", stopString="Mechanical",\
            vector=True, dictionary=True))
        print(icGenerator.load_ods_section(test_path, "Footprint", stopString="Mechanical",\
            vector=True, dictionary=False))
        print(icGenerator.load_ods_section(test_path, "Footprint", startString="Footprint",\
            vector=False, dictionary=True))
        print(icGenerator.load_ods_section(test_path, "Footprint", startString="Mechanical",\
            stopString="Footprint",vector=False, dictionary=False))
    
    def test_load_parts_advanced():
        print(icGenerator.load_parts_advanced(test_path))
        
    def load_symbol_advanced(fileName, symbolName):
        try:
            data = pyexcel_ods3.get_data(fileName)["Symbol"]
        except KeyError:
            raise ValueError("No \"Symbol\" tab found in " + fileName)
        except:
            raise ValueError("Error opening file " + fileName)
        pinout_start=0
        params={}
        pinout=[]
        symbols=[]
        col=0
        for line in data:
            if line:
                if line[0]:
                    if pinout_start==1:
                        for i in range(4,len(line),2):
                            if str(line[i]).strip()==str(symbolName).strip():
                                col=i
                                break
                        pinout_start=2
                    elif pinout_start==2:
                        if col:
                            pin = line[0]
                            unit = line[1]
                            side = 0 if line[2]=="L" else 1
                            position = line[3]
                            pin_name = line[i]
                            direction = line[i+1]
                            while len(pinout)<=unit:
                                pinout.append([[],[]])
                            while len(pinout[unit][side])<=position:
                                pinout[unit][side].append(None)
                            pinout[unit][side][position]=[pin_name, pin, direction]
                        else:
                            raise ValueError("Symbol %s not found in file %s" % (symbolName, fileName))
                    else:
                        if str(line[0]).lower()=="pinout":
                            pinout_start = 1
                        else:
                            if len(line)>=2:
                                params[str(line[0]).strip()]=line[1]
                else:
                    pass
            else:
                pass
        i=0
        for sym in pinout:
            if len(pinout)>1:
                postfix = "_%d"%i
                width = params["Width%d"%i]
            else:
                postfix = ""
                width = params["Width"]
            symbols.append(symbolIC(symbolName + postfix,\
                pinsLeft=sym[0], pinsRight=sym[1], width=width, refDes=defaults.icRefDes,showPinNames=True, showPinNumbers=True))
            i=i+1
        return symbols
        
    def test_load_symbol_advanced():
        print(icGenerator.load_symbol_advanced(test_path))
        
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
    icGenerator.test_load_footprints_advanced()
    
    