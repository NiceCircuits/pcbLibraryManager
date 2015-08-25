# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 22:48:34 2015

@author: piotr at nicecircuits.com
"""

class defaults:
    # footprint defaults
    silkWidth = 0.1524
    silkExtend = 0.18 # extension of silkscreen from component pads
    silkTextHeight = 1.0
    firstPinMarkerR = 0.5
    documentationWidth = 0.05
    documentationTextHeight = 0.5
    originMarkSize = 1.0
    court={'L':0.15, 'N':0.26, 'M':0.5}
    courtSmall={'L':0.1, 'N':0.15, 'M':0.26}
    courtConn={'L':0.5, 'N':0.5, 'M':1.0}
    # symbol defaults
    symbolTextHeight = 60
    symbolSmallTextHeight = 40
    symbolPinTextHeight = 60
    symbolLineWidth = 10
    symbolThickLineWidth = 20
    #symbolPinLineWidth = 6
    # reference designators
    icRefDes = "U"
    transistorRefDes = "T"
    diodeRefDes = "D"
    switchRefDes = "SW"
    conRefDes = "CON"
    resonatorRefDes="Q"