# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 22:52:36 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.library import libraryClass
from symbols.symbolConnectors import symbolConnector

class libraryConectorsWireToBoard(libraryClass):
    """
    """
    def __init__(self):
        super().__init__("niceConectorsWireToBoard")
        for rightAngle in [True, False]:
            for n in [2,3,4,5,6,7,8,10,20]:
                self.parts.append(partNS25(n, rightAngle))


class partNS25_Straight():
    """
    Straight Nigini NS25 connector
    """
    def __init__(self, circuits, rightAngle):
        name = "NS25-W%d%s" %(circuits, "K" if rightAngle else "P")
        super().__init__(name, defaults.conRefDes)
        self.symbol = symbolConnector("CON%d" % circuits, circuits)
        self.footprints.append(footprintNS25Straight(name, circuits,\
            alternativeLibName = "niceConectorsWireToBoard"))

class footprintNS25Straight():
    """
    """
    pass