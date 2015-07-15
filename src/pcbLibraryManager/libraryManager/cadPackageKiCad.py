# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:10:58 2015

@author: piotr at nicecircuits.com
"""

from libraryManager.cadPackage import cadPackage
from libraryManager.library import  libraryClass
import os.path
from libraryManager.common import *
from libraryManager.footprintPrimitive import *

class KiCad(cadPackage):
    """
    KiCad CAD package handling class
    """
    def __init__(self):
        super().__init__()
        
    def generateLibrary(self, library, path):
        super().generateLibrary(library, path)
        ################# Symbol library #################
        f = self.openFile(os.path.join(path, library.name + ".lib"))
        # TODO: symbol library
        f.close()
        ################# footprint library #################
        for part in library.parts:
            for footprint in part.footprints:
                self.log.debug("Generating footprint %s in library %s.",\
                    footprint.name, footprint.alternativeLibName)
                libDir = os.path.join(path, footprint.alternativeLibName + ".pretty")
                self.createFolder(libDir)
                f = self.openFile(os.path.join(libDir, footprint.name + ".kicad_mod"))
                print(r"(module %s (layer F.Cu)" % footprint.name, file=f)
                print(r"""  (fp_text reference REF** (at 0 0) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )""", file=f)  # TODO:
                print(r"""  (fp_text value SW_1290F1123 (at 0 -5) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )""", file=f)  # TODO:
                for primitive in footprint.primitives:
                    self.generatePcbPrimitive(primitive, f)
                print(")", file = f)
                
############## Footprint primitives ##############
    def generatePcbPrimitive(self, primitive):
        n = primitive.__class__.__name__
        if n == "pcbLine":
            return self.generatePcbLine(primitive)
        elif n == "pcbPolyline":
            return self.generatePcbPolyLine(primitive)
        elif n == "pcbRectangle":
            return self.generatePcbRectangle(primitive)
        elif n == "pcbArc":
            return self.generatePcbArc(primitive)
        elif n == "pcbCircle":
            return self.generatePcbCircle(primitive)
        elif n == "pcbPad":
            return self.generatePcbPad(primitive)
        elif n == "pcbText":
            return self.generatePcbText(primitive)
        else:
            text = "generatePcbPrimitive: Invalid primitive class name: %s" % n
            self.log.error(text)
            raise TypeError(text)

    def generatePcbLine(self, primitive, file):
        print(r"  (fp_line (start %1.3f %1.3f) (end %1.3f %1.3f) (layer %s) (width %1.3f))" %\
            (primitive.points[0][0], primitive.points[0][1], primitive.points[1][0],\
            primitive.points[1][1], self.layerNames[primitive.layer], primitive.width),\
            file=file)
    
    def generatePcbPolyLine(self, primitive, file):
        pass

    def generatePcbRectangle(self, primitive, file):
        # width, position, dimensions, rotation
        
        poly = pcbPolyline(primitive.layer, primitive.width, points)
        self.generatePcbPolyLine(poly, file)

    def generatePcbArc(self, primitive, file):
        pass

    def generatePcbCircle(self, primitive, file):
        pass

    def generatePcbPad(self, primitive, file):
        pass

    def generatePcbText(self, primitive, file):
        pass

    layerNames = {pcbLayer.topCopper:"F.Cu" ,pcbLayer.bottomCopper:"B.Cu", \
        pcbLayer.topSilk:"F.SilkS", pcbLayer.bottomSilk:"B.SilkS", \
        pcbLayer.topMask:"F.Mask", pcbLayer.bottomMask:"B.Mask",\
        pcbLayer.thtPads:None, pcbLayer.thtVias:None, pcbLayer.edges:None,\
        pcbLayer.topNames:"F.SilkS", pcbLayer.bottomNames:"B.SilkS", \
        pcbLayer.topValues:"F.SilkS", pcbLayer.bottomValues:"B.SilkS",\
        pcbLayer.topPaste:"F.Paste", pcbLayer.bottomPaste:"B.Paste",\
        pcbLayer.topGlue:"F.Adhes", pcbLayer.bottomGlue:"B.Adhes",\
        pcbLayer.topKeepout:None, pcbLayer.bottomKeepout:None,\
        pcbLayer.topRestrict:None, pcbLayer.bottomRestrict:None,\
        pcbLayer.thtRestrict:None, pcbLayer.thtHoles:None,\
        pcbLayer.topAssembly:"F.Fab", pcbLayer.bottomAssembly:"B.Fab",\
        pcbLayer.topDocumentation:"F.Fab", pcbLayer.bottomDocumentation:"B.Fab"}