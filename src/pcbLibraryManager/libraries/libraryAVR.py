# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 18:04:03 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from libraryManager.part import part
from libraryManager.footprint import footprint
from libraryManager.footprintPrimitive import *
from libraryManager.defaults import *
from symbols.symbolsIC import symbolIC
from libraryManager.symbolPrimitive import *

class libraryAVR(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceAVR")
        self.parts.append(partAtmega48("ATmega48", "AU"))
        self.parts.append(partAtmega48("ATmega328", "AU"))
        
class partAtmega48(part):
    """
    Atmega48/88/168/328/P/A part
    """
    def __init__(self, name="ATmega48", version="AU"):
        name = name + "-" + version
        super().__init__(name, "U")
        self.symbols.append(symbolAtmega48(name, version))
        for size in ["0402", "0603", "0805", "1206", "1210", "2010", "2512"]:
            for density in ["L", "N", "M"]:
                pass
                #self.footprints.append(footprintSmdChip(size + "_" + density, \
                 #   size = size, density = density, alternativeLibName = "niceRLC"))

class symbolAtmega48(symbolIC):
    """
    Atmega48/88/168/328/P/A symbol
    """
    def __init__(self, name, version, refDes="U", showPinNames=True, showPinNumbers=True):
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
