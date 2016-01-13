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
from libraries.libraryPinheaders import footprintPinheader

class librarySTM32(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceSTM32")
        self.parts.append(partAtmega48("ATmega48", "AU"))
        self.parts.append(partAtmega48("ATmega328", "AU"))
        self.parts.append(partAvrProg())
        
class partAtmega48(part):
    """
    Atmega48/88/168/328/P/A part
    """
    def __init__(self, name="ATmega48", version="AU"):
        name = name + "-" + version
        super().__init__(name, "U")
        self.symbols.append(symbolAtmega48(name, version))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintQfp(32, 0.8, density=density))

class partAvrProg(part):
    """AVR programming connector part
    """
    def __init__(self, name="AVR_Prog"):
        super().__init__(name, defaults.conRefDes)
        self.symbols.append(symbolAvrProg())
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintPinheader(2, 3, density))


class symbolSTM32_LQFP64_main(symbolIC):
    """
    STM32 LQFP64 main symbol generator
    """
    def __init__(self, version=""):
        name="STM32_LQFP64_%s_main" % version
        pinsLeft = [
['PA0', 14, pinType.IO],
['PA1', 15, pinType.IO],
['PA2', 16, pinType.IO]]
        if version=="":
            pinsLeft = pinsLeft + [
['PA3/SAR_VREF+', 17, pinType.IO]]
        elif STM32_LQFP64_version[version] in [1,2]:
            pinsLeft = pinsLeft + [
['PA3/SAR_VREF+', 17, pinType.IO]]
        else:
            warnings.warn("unsupported version")
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
none,
['PC0', 8 , pinType.IO],
['PC1', 9 , pinType.IO],
['PC2', 10, pinType.IO],
['PC3', 11, pinType.IO],
['PC4', 24, pinType.IO],
['PC5', 25, pinType.IO],
['PC6', 37, pinType.IO],
['PC7', 38, pinType.IO]
        ]
        pinsRight = [
['PB0', 26, pinType.IO]]
        if version=="":
            pinsRight = pinsRight + [
['PB1/VREF+', 27, pinType.IO]]
        else:
            warnings.warn("unsupported version")
        pinsRight = pinsRight + [
['PB2', 28, pinType.IO],
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
['PB11/VCAP1', 30, pinType.IO],
['PB12/SD_VREF+', 33, pinType.IO],
['PB13/PB14', 34, pinType.IO],
['PB14/PB15', 35, pinType.IO],
['PB15/PD8', 36, pinType.IO]]
        else:
            warnings.warn("unsupported version")
        pinsRight = pinsRight + [
none,
['PC8', 39, pinType.IO],
['PC9', 40, pinType.IO],
['PC10', 51, pinType.IO],
['PC11', 52, pinType.IO],
['PC12', 53, pinType.IO],
['PC13', 2 , pinType.IO],
['PC14 - OSC32_IN', 3 , pinType.IO],
['PC15 - OSC32_OUT', 4 , pinType.IO]
        ]
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=3000,\
        refDes=defaults.icRefDes,showPinNames=True, showPinNumbers=True)

class symbolSTM32_LQFP64_power(symbolIC):
    """
    STM32 LQFP64 power part symbol generator
    """
    def __init__(self, name, version, refDes="U", showPinNames=True, showPinNumbers=True):
        pinsRight = [
['(PCINT0/CLKO/ICP1) PB0', 12, pinType.IO],
        ]
        pinsLeft = [
['PC6 (RESET/PCINT14)', 29, pinType.IO],
        ]
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=3000)

class symbolAvrProg(symbolIC):
    """AVR programming connector symbol symbol
    """
    def __init__(self, name="AVR_Prog", refDes=defaults.conRefDes, showPinNames=True, showPinNumbers=True):
        pinsRight = [
['VCC', 2, pinType.passive],
['MOSI', 4, pinType.passive],
['GND', 6, pinType.passive]
        ]
        pinsLeft = [
['MISO', 1, pinType.passive],
['SCK', 3, pinType.passive],
['RST', 5, pinType.passive]
        ]
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=800, refDes=refDes)

STM32_LQFP64_version={
    "":0,
    "STM32F030R8":1,
    "STM32F030RC":2
}
    
