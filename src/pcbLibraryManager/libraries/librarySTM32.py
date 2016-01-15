# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 06:41:54 2016

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from footprints.footprintSmdQuad import footprintQfp
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *

class librarySTM32(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSTM32")
        self.parts.append(partSTM32_LQFP64("STM32F030R8"))
        self.parts.append(partSTM32_LQFP64("STM32F030RC"))
        self.parts.append(partSTM32_LQFP64("STM32F051R4"))
        self.parts.append(partSTM32_LQFP64("STM32F051R6"))
        self.parts.append(partSTM32_LQFP64("STM32F051R8"))
        self.parts.append(partSTM32_LQFP64("STM32F058R8"))
        self.parts.append(partSTM32_LQFP64("STM32F070RB"))
        self.parts.append(partSTM32_LQFP64("STM32F071RB"))
        self.parts.append(partSTM32_LQFP64("STM32F072R8"))
        self.parts.append(partSTM32_LQFP64("STM32F072RB"))
        self.parts.append(partSTM32_LQFP64("STM32F078RB"))
        self.parts.append(partSTM32_LQFP64("STM32F091RB"))
        self.parts.append(partSTM32_LQFP64("STM32F091RC"))
        self.parts.append(partSTM32_LQFP64("STM32F098RC"))
        self.parts.append(partSTM32_LQFP64("STM32F100R4"))
        self.parts.append(partSTM32_LQFP64("STM32F100R6"))
        self.parts.append(partSTM32_LQFP64("STM32F100R8"))
        self.parts.append(partSTM32_LQFP64("STM32F100RB"))
        self.parts.append(partSTM32_LQFP64("STM32F100RC"))
        self.parts.append(partSTM32_LQFP64("STM32F100RD"))
        self.parts.append(partSTM32_LQFP64("STM32F100RE"))
        self.parts.append(partSTM32_LQFP64("STM32F101R4"))
        self.parts.append(partSTM32_LQFP64("STM32F101R6"))
        self.parts.append(partSTM32_LQFP64("STM32F101R8"))
        self.parts.append(partSTM32_LQFP64("STM32F101RB"))
        self.parts.append(partSTM32_LQFP64("STM32F101RC"))
        self.parts.append(partSTM32_LQFP64("STM32F101RD"))
        self.parts.append(partSTM32_LQFP64("STM32F101RE"))
        self.parts.append(partSTM32_LQFP64("STM32F101RF"))
        self.parts.append(partSTM32_LQFP64("STM32F101RG"))
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        self.parts.append(partSTM32_LQFP64())
        
class partSTM32_LQFP64(part):
    """
    STM32 LQFP64 part generator
    """
    def __init__(self, version=""):
        name = "STM32_LQFP64_%s" % version
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolSTM32_LQFP64_A(version))
        self.symbols.append(symbolSTM32_LQFP64_B(version))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintQfp(32, 0.8, density=density))

class symbolSTM32_LQFP64_A(symbolIC):
    """
    STM32 LQFP64 symbol generator - part A
    """
    def __init__(self, version=""):
        name="STM32_LQFP64_%d_A" % STM32_LQFP64_version[version]
#=======================================pins left==============================
        pinsLeft = [
None]
        if STM32_LQFP64_version[version] in [0,9]:
            pinsLeft = pinsLeft + [
    ['PA0/WKUP', 14, pinType.IO]]
        elif STM32_LQFP64_version[version] in [1,2,3,4,5,6,7,8]:
            pinsLeft = pinsLeft + [
    ['PA0', 14, pinType.IO]]
        else:
            raise ValueError("unsupported version")
        pinsLeft = pinsLeft + [
['PA1', 15, pinType.IO],
['PA2', 16, pinType.IO]]
        if version=="":
            pinsLeft = pinsLeft + [
    ['PA3/SAR_VREF+', 17, pinType.passive]]
        elif STM32_LQFP64_version[version] in [1,2,3,4,5,6,7,8,9]:
            pinsLeft = pinsLeft + [
    ['PA3', 17, pinType.IO]]
        else:
            raise ValueError("unsupported version")
        pinsLeft = pinsLeft + [
['PA4', 20, pinType.IO],
['PA5', 21, pinType.IO],
['PA6', 22, pinType.IO],
['PA7', 23, pinType.IO],
['PA8', 41, pinType.IO],
['PA9', 42, pinType.IO],
['PA10', 43, pinType.IO],
['PA11', 44, pinType.IO],
['PA12', 45, pinType.IO],
['PA13', 46, pinType.IO],
['PA14', 49, pinType.IO],
['PA15', 50, pinType.IO],
None,
['PD2', 54, pinType.IO],
        ]
#=======================================pins right=============================
        pinsRight = [
None,
['PB0', 26, pinType.IO]]
        if version=="":
            pinsRight = pinsRight + [
    ['PB1/VREF+', 27, pinType.passive],
    ['PB2/NPOR', 28, pinType.IO]]
        elif STM32_LQFP64_version[version] in [1,2,3,5,7,9]:
            pinsRight = pinsRight + [
    ['PB1', 27, pinType.IO],
    ['PB2', 28, pinType.IO]]
        elif STM32_LQFP64_version[version] in [4,6,8]:
            pinsRight = pinsRight + [
    ['PB1', 27, pinType.IO],
    ['NPOR', 28, pinType.input]]
        else:
            raise ValueError("unsupported version")
        pinsRight = pinsRight + [
['PB3', 55, pinType.IO],
['PB4', 56, pinType.IO],
['PB5', 57, pinType.IO],
['PB6', 58, pinType.IO],
['PB7', 59, pinType.IO],
['PB8', 61, pinType.IO],
['PB9', 62, pinType.IO]]
        if version=="":
            pinsRight = pinsRight + [
    ['PB10/PE8', 29, pinType.IO],
    ['PB11/VCAP1', 30, pinType.passive],
    ['PB12/SD_VREF+', 33, pinType.passive],
    ['PB13/PB14', 34, pinType.IO],
    ['PB14/PB15', 35, pinType.IO],
    ['PB15/PD8', 36, pinType.IO]]
        elif STM32_LQFP64_version[version] in [1,2,3,4,5,6,7,8,9]:
            pinsRight = pinsRight + [
    ['PB10', 29, pinType.IO],
    ['PB11', 30, pinType.IO],
    ['PB12', 33, pinType.IO],
    ['PB13', 34, pinType.IO],
    ['PB14', 35, pinType.IO],
    ['PB15', 36, pinType.IO]]
        else:
            raise ValueError("unsupported version")
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=3000,\
        refDes=defaults.icRefDes,showPinNames=True, showPinNumbers=True)

class symbolSTM32_LQFP64_B(symbolIC):
    """
    STM32 LQFP64 symbol generator - part B
    """
    def __init__(self, version=""):
        name="STM32_LQFP64_%d_B" % STM32_LQFP64_version[version]
#=======================================pins left==============================
        pinsLeft = [
['NRST', 7, pinType.IO]]
        if version=="":
            pinsLeft = pinsLeft + [
    ['BOOT0/PF11', 60, pinType.input],
    None,
    ['VDD/VBAT/VLCD', 1, pinType.pwrIn],
    None,
    ['VDDA/VREF+', 13, pinType.pwrIn]]
        elif STM32_LQFP64_version[version] in [1,2]:
            pinsLeft = pinsLeft + [
    ['BOOT0', 60, pinType.input],
    None,
    ['VDD', 1, pinType.pwrIn],
    None,
    ['VDDA', 13, pinType.pwrIn]]
        elif STM32_LQFP64_version[version] in [3,4,5,6,9]:
            pinsLeft = pinsLeft + [
    ['BOOT0', 60, pinType.input],
    None,
    ['VBAT', 1, pinType.pwrIn],
    None,
    ['VDDA', 13, pinType.pwrIn]]
        elif STM32_LQFP64_version[version] in [7,8]:
            pinsLeft = pinsLeft + [
    ['BOOT0/PF11', 60, pinType.input],
    None,
    ['VBAT', 1, pinType.pwrIn],
    None,
    ['VDDA', 13, pinType.pwrIn]]
        else:
            raise ValueError("unsupported version")
        pinsLeft = pinsLeft + [
None,
['VDD', 32, pinType.pwrIn],
['VDD', 64, pinType.pwrIn]]
        if version=="":
            pinsLeft = pinsLeft + [
    ['VDD/VDDIO2/VUSB/VSA/PF7', 48, pinType.passive],
    ['VDD/PF5', 19, pinType.passive]]
        elif STM32_LQFP64_version[version] in [1,3,4]:
            pinsLeft = pinsLeft + [
    ['PF7', 48, pinType.passive],
    ['PF5', 19, pinType.passive]]
        elif STM32_LQFP64_version[version] in [2,9]:
            pinsLeft = pinsLeft + [
    ['VDD', 48, pinType.passive],
    ['VDD', 19, pinType.passive]]
        elif STM32_LQFP64_version[version] in [5,6,7,8]:
            pinsLeft = pinsLeft + [
    ['VDDIO2', 48, pinType.passive],
    ['VDD', 19, pinType.passive]]
        else:
            raise ValueError("unsupported version")
        pinsLeft = pinsLeft + [
None,
None,
['VSSA', 12, pinType.pwrIn],
None]
        if version=="":
            pinsLeft = pinsLeft + [
    ['VSS/VCAP1', 31, pinType.pwrIn],
    ['VSS', 63, pinType.pwrIn],
    ['VSS/VCAP2/PF6', 47, pinType.passive],
    ['VSS/PF4/PA3', 18, pinType.passive]]
        elif STM32_LQFP64_version[version] in [1,3,4]:
            pinsLeft = pinsLeft + [
    ['VSS', 31, pinType.pwrIn],
    ['VSS', 63, pinType.pwrIn],
    ['PF6', 47, pinType.passive],
    ['PF4', 18, pinType.passive]]
        elif STM32_LQFP64_version[version] in [2,5,6,7,8,9]:
            pinsLeft = pinsLeft + [
    ['VSS', 31, pinType.pwrIn],
    ['VSS', 63, pinType.pwrIn],
    ['VSS', 47, pinType.passive],
    ['VSS', 18, pinType.passive]]
        else:
            raise ValueError("unsupported version")
#=======================================pins right=============================
        pinsRight = [
['PC0', 8 , pinType.IO],
['PC1', 9 , pinType.IO],
['PC2', 10, pinType.IO],
['PC3', 11, pinType.IO],
['PC4', 24, pinType.IO],
['PC5', 25, pinType.IO],
['PC6', 37, pinType.IO],
['PC7', 38, pinType.IO],
['PC8', 39, pinType.IO],
['PC9', 40, pinType.IO],
['PC10', 51, pinType.IO],
['PC11', 52, pinType.IO],
['PC12', 53, pinType.IO]]
        if STM32_LQFP64_version[version] in [0,9]:
            pinsRight = pinsRight + [
            ['PC13/TAMPER-RTC', 2 , pinType.IO]]
        elif STM32_LQFP64_version[version] in [1,2,3,4,5,6,7,8]:
            pinsRight = pinsRight + [
            ['PC13', 2 , pinType.IO]]
        else:
            raise ValueError("unsupported version")
        pinsRight = pinsRight + [
['PC14-OSC32_IN', 3 , pinType.IO],
['PC15-OSC32_OUT', 4 , pinType.IO],
None]
        if version=="":
            pinsRight = pinsRight + [
    ['PF0/PD0/PH0-OSC_IN', 5, pinType.IO],
    ['PF1/PD1/PH1-OSC_OUT', 6, pinType.IO]]
        elif STM32_LQFP64_version[version] in [1,2,3,4,5,6,7,8]:
            pinsRight = pinsRight + [
    ['PF0-OSC_IN', 5, pinType.input],
    ['PF1-OSC_OUT', 6, pinType.output]]
        elif STM32_LQFP64_version[version] in [9]:
            pinsRight = pinsRight + [
    ['OSC_IN', 5, pinType.IO],
    ['OSC_OUT', 6, pinType.IO]]
        else:
            raise ValueError("unsupported version")
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=3000,\
        refDes=defaults.icRefDes,showPinNames=True, showPinNumbers=True)

STM32_LQFP64_version={
    "":0,
    "STM32F030R8":1,
    "STM32F030RC":2,
    "STM32F051R4":3,
    "STM32F051R6":3,
    "STM32F051R8":3,
    "STM32F058R8":4,
    "STM32F070RB":2,
    "STM32F071RB":5,
    "STM32F072R8":5,
    "STM32F072RB":5,
    "STM32F078RB":6,
    "STM32F091RB":7,
    "STM32F091RC":7,
    "STM32F098RC":8,
    "STM32F100R4":9,
    "STM32F100R6":9,
    "STM32F100R8":9,
    "STM32F100RB":9,
    "STM32F100RC":9,
    "STM32F100RD":9,
    "STM32F100RE":9,
    "STM32F101R4":9,
    "STM32F101R6":9,
    "STM32F101R8":9,
    "STM32F101RB":9,
    "STM32F101RC":9,
    "STM32F101RD":9,
    "STM32F101RE":9,
    "STM32F101RF":9,
    "STM32F101RG":9,
}
    
