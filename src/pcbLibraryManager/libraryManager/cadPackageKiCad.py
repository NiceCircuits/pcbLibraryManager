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
import logging

class KiCad(cadPackage):
    """
    KiCad CAD package handling class
    """
    def __init__(self):
        """
        """
        super().__init__()
        
    def generateLibrary(self, library, path):
        """
        """
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
                self.generatePcbText(footprint.nameObject, file=f, textType="reference")
                self.generatePcbText(footprint.valueObject, file=f, textType="value")
                for primitive in footprint.primitives:
                    self.generatePcbPrimitive(primitive, f)
                print(")", file = f)
                
############## Footprint primitives ##############
    def generatePcbPrimitive(self, primitive, file):
        """
        """
        n = primitive.__class__.__name__
        if n == "pcbLine":
            return self.generatePcbLine(primitive, file)
        elif n == "pcbPolyline":
            return self.generatePcbPolyLine(primitive, file)
        elif n == "pcbRectangle":
            return self.generatePcbRectangle(primitive, file)
        elif n == "pcbArc":
            return self.generatePcbArc(primitive, file)
        elif n == "pcbCircle":
            return self.generatePcbCircle(primitive, file)
        elif n == "pcbSmtPad":
            return self.generatePcbSmtPad(primitive, file)
        elif n == "pcbText":
            return self.generatePcbText(primitive, file)
        else:
            text = "generatePcbPrimitive: Invalid primitive class name: %s" % n
            self.log.error(text)
            raise TypeError(text)

    def generatePcbLine(self, primitive, file):
        """
        """
        print(r"  (fp_line (start %1.3f %1.3f) (end %1.3f %1.3f) (layer %s) (width %1.3f))" %\
            (primitive.points[0][0], -primitive.points[0][1], primitive.points[1][0],\
            -primitive.points[1][1], self.layerNames[primitive.layer], primitive.width),\
            file=file)
    
    def generatePcbPolyLine(self, primitive, file):
        """
        """
        for p in polylinePointsToLines(primitive.points):
            self.log.log(logging.DEBUG-3,p)
            self.generatePcbLine(pcbLine(primitive.layer, primitive.width,\
                points=p),file)

    def generatePcbRectangle(self, primitive, file):
        """
        """
        # width, position, dimensions, rotation
        points = rectangleToPolyLinePoints(primitive.position,\
            primitive.dimensions, primitive.rotation)
        poly = pcbPolyline(primitive.layer, primitive.width, points)
        self.generatePcbPolyLine(poly, file)

    def generatePcbArc(self, primitive, file):
        """
        """
        pass

    def generatePcbCircle(self, primitive, file):
        """
        """
        print(r"  (fp_circle (center %1.3f %1.3f) (end %1.3f %1.3f) (layer %s) (width %1.3f))"%\
            (primitive.dimensions[0], primitive.dimensions[1],\
            primitive.dimensions[0]+primitive.radius, primitive.dimensions[1],\
            self.layerNames[primitive.layer], primitive.width), file=file)

    def generatePcbSmtPad(self, primitive, file):
        """
        """
        if primitive.layer==pcbLayer.topCopper:
            layerText=r"F.Cu F.Paste F.Mask"
        else:
            layerText=r"B.Cu B.Paste B.Mask"
        if 0:
            shape = "oval"
        else:
            shape = "rect" #TODO: roundness, circle
        print(r"  (pad %s smd %s (at %1.3f %1.3f %1.1f) (size %1.3f %1.3f) (layers %s))" %\
            (primitive.name, shape, primitive.position[0], -primitive.position[1],\
            primitive.rotation, primitive.dimensions[0], primitive.dimensions[1],\
            layerText), file=file)

    def generatePcbText(self, primitive, file, textType="user"):
        """
        Generate PCB text
        """
        alignText = self.textAligns[primitive.align]
        mirrorText = " mirror" if primitive.mirror else ""
        if alignText or mirrorText:
            justifyText = r" (justify" + alignText + mirrorText + ")"
        else:
            justifyText = ""
        print(r"""  (fp_text %s %s (at %1.3f %1.3f  %1.1f) (layer %s)
    (effects (font (size %1.3f %1.3f) (thickness %1.3f))%s)
  )""" % (textType, primitive.text, primitive.position[0], -primitive.position[1],\
            primitive.rotation, self.layerNames[primitive.layer], primitive.height,\
            primitive.height, primitive.width, justifyText), file = file)

    layerNames = {pcbLayer.topCopper:"F.Cu" ,pcbLayer.bottomCopper:"B.Cu", \
        pcbLayer.topSilk:"F.SilkS", pcbLayer.bottomSilk:"B.SilkS", \
        pcbLayer.topMask:"F.Mask", pcbLayer.bottomMask:"B.Mask",\
        pcbLayer.thtPads:None, pcbLayer.thtVias:None, pcbLayer.edges:None,\
        pcbLayer.topNames:"F.SilkS", pcbLayer.bottomNames:"B.SilkS", \
        pcbLayer.topValues:"F.Fab", pcbLayer.bottomValues:"B.Fab",\
        pcbLayer.topPaste:"F.Paste", pcbLayer.bottomPaste:"B.Paste",\
        pcbLayer.topGlue:"F.Adhes", pcbLayer.bottomGlue:"B.Adhes",\
        pcbLayer.topKeepout:None, pcbLayer.bottomKeepout:None,\
        pcbLayer.topRestrict:None, pcbLayer.bottomRestrict:None,\
        pcbLayer.thtRestrict:None, pcbLayer.thtHoles:None,\
        pcbLayer.topAssembly:"F.Fab", pcbLayer.bottomAssembly:"B.Fab",\
        pcbLayer.topDocumentation:"F.Fab", pcbLayer.bottomDocumentation:"B.Fab"}
    
    textAligns = {textAlign.center:"", textAlign.centerLeft:" left",\
        textAlign.centerRight:" right", textAlign.topCenter:" top",\
        textAlign.topLeft:" left top", textAlign.topRight:" right top",\
        textAlign.bottomCenter:" bottom", textAlign.bottomLeft:" left bottom",\
        textAlign.bottomRight:" right bottom"}