# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 18:04:03 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from footprints.footprintSmdQuad import footprintQfp
from footprints.footprintSmdDualRow import footprintSot23
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *
from libraries.libraryPinheaders import footprintPinheader
from libraryManager.generateLibraries import generateLibraries
from parts.icGenerator import icGenerator
import os

class libraryAVR(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceAVR")
        self.parts.append(partAtmega48("ATmega48", "AU"))
        self.parts.append(partAtmega48("ATmega328", "AU"))
        self.parts.append(partAttiny10("ATtiny10-TSHR"))
        self.parts.append(partAvrProg())
# ============== Atmega48/88/168/328 in MLF32/VFQFN32 package ============== 
        path=os.path.join(os.path.dirname(__file__),"ATmega48_88_168_328_MLF32.ods")
        self.parts.extend(icGenerator.generate_advanced(path))
        
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

class partAttiny10(part):
    """
    Attiny4/5/9/10 part
    """
    def __init__(self, name="ATtiny10"):
        super().__init__(name, defaults.icRefDes)
        self.symbols.append(symbolAttiny10(name))
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintSot23(6, density=density))

class partAvrProg(part):
    """AVR programming connector part
    """
    def __init__(self, name="AVR_Prog"):
        super().__init__(name, defaults.conRefDes)
        self.symbols.append(symbolAvrProg())
        for density in ["N", "L", "M"]:
            self.footprints.append(footprintPinheader(2, 3, density))


class symbolAtmega48(symbolIC):
    """
    Atmega48/88/168/328/P/A symbol
    """
    def __init__(self, name, refDes="U", showPinNames=True, showPinNumbers=True):
        pinsRight = [
['(PCINT0/CLKO/ICP1) PB0', 12, pinType.IO],
['(PCINT1/OC1A) PB1', 13, pinType.IO],
['(PCINT2/SS/OC1B) PB2', 14, pinType.IO],
['(PCINT3/OC2A/MOSI) PB3', 15, pinType.IO],
['(PCINT4/MISO) PB4', 16, pinType.IO],
['(SCK/PCINT5) PB5', 17, pinType.IO],
['(ADC0/PCINT8) PC0', 23, pinType.IO],
['(ADC1/PCINT9) PC1', 24, pinType.IO],
['(ADC2/PCINT10) PC2', 25, pinType.IO],
['(ADC3/PCINT11) PC3', 26, pinType.IO],
['(ADC4/SDA/PCINT12) PC4', 27, pinType.IO],
['(ADC5/SCL/PCINT13) PC5', 28, pinType.IO],
['(RXD/PCINT16) PD0', 30, pinType.IO],
['(TXD/PCINT17) PD1', 31, pinType.IO],
['(INT0/PCINT18) PD2', 32, pinType.IO],
['(PCINT19/OC2B/INT1) PD3', 1, pinType.IO],
['(PCINT20/XCK/T0) PD4', 2, pinType.IO],
['(PCINT21/OC0B/T1) PD5', 9, pinType.IO],
['(PCINT22/OC0A/AIN0) PD6', 10, pinType.IO],
['(PCINT23/AIN1) PD7', 11, pinType.IO]
        ]
        pinsLeft = [
['PC6 (RESET/PCINT14)', 29, pinType.IO],
None,
['PB6 (PCINT6/XTAL1/TOSC1)', 7, pinType.IO],
['PB7 (PCINT7/XTAL2/TOSC2)', 8, pinType.IO],
None,
None,
None,
None,
['VCC', 4, pinType.pwrIn],
['VCC', 6, pinType.pwrIn],
['AVCC', 18, pinType.pwrIn],
['AREF', 20, pinType.input],
None,
['GND', 3, pinType.pwrIn],
['GND', 5, pinType.pwrIn],
['GND', 21, pinType.pwrIn],
None,
None,
['ADC6', 19, pinType.input],
['ADC7', 22, pinType.input]
        ]
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=3000)

class symbolAttiny10(symbolIC):
    """
    Attiny4/5/9/10 symbol
    """
    def __init__(self, name, refDes="U", showPinNames=True, showPinNumbers=True):
        pinsRight = [
['TPIDATA/PB0', 1, pinType.IO],
['TPICLK/PB1', 3, pinType.IO],
['PB2', 4, pinType.IO],
['RESET/PB3', 6, pinType.IO]
        ]
        pinsLeft = [
['VCC', 5, pinType.pwrIn],
None,
None,
['GND', 2, pinType.pwrIn],
        ]
        super().__init__(name, pinsLeft=pinsLeft, pinsRight=pinsRight, width=1200)

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

if __name__ == "__main__":
    generateLibraries([libraryAVR()])