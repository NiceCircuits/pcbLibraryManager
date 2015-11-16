# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 19:12:55 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from symbols.symbolsIC import symbolIC
from libraryManager.defaults import defaults
from libraryManager.symbolPrimitive import *
from libraryManager.part import part

class libraryConnectorsOther(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceConectorsOther")
        self.parts.append(partConnUsb(""))


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
        self.symbols.append(symbolIC("connUsb", [], pins, 400, defaults.conRefDes,))
        if connType:
            pass
