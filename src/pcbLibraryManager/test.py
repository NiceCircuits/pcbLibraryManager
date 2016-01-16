# -*- coding: utf-8 -*-
import pyexcel_ods3
import numpy as np

class pinoutLoader:
    def load(fileName):
        try:
            sheet = np.array(pyexcel_ods3.get_data(fileName)["pinout"])
            test=sheet[:,0] #check proper conversion to numpy.array
        except Exception as ex:
            print("Error! Maybe sheet contains empty cells (especially at ends of rows)?")
            raise ex
        rowV = sheet[0]
        nVersions = int((len(rowV)-1)/2)
        print(rowV)
        ret=[0]*nVersions #initialize return structure
        nPins=len(sheet)-2
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
                ret[nV]["pinTypes"][ret[nV]["pins"][i]]=pinTypes[i]
                ret[nV]["pinNames"][ret[nV]["pins"][i]]=pinNames[i]
        return ret

if 1:
    print(__file__)
else:
    print (pyexcel_ods3.get_data("test.ods"))
    