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

def boolToYN(x):
    if x:
        return "Y"
    else:
        return "N"

class KiCad(cadPackage):
    """
    KiCad CAD package handling class
    """
    def __init__(self):
        """
        """
        super().__init__()
    
    scale=0.5
            
    def generateLibrary(self, library, path):
        """
        """
        super().generateLibrary(library, path)
        ################# Symbol library #################
        f = self.openFile(os.path.join(path, library.name + ".lib"))
        # library header
        print(r"""EESchema-LIBRARY Version 2.3
#encoding utf-8""", file=f)
        for part in library.parts:
            self.log.debug("Creating part %s in library %s.", part.name, library.name)
            print(r"""#
# %s
#""" % part.name, file=f)
            sym=part.symbols[0]
            print(r"DEF %s %s 0 50 %s %s %d F N" %(part.name, part.refDes,\
                boolToYN(sym.showPinNumbers), boolToYN(sym.showPinNames),\
                len(part.symbols)), file=f)
            self.generateSymbolTextSpecial(sym.nameObject,f,"F0")
            self.generateSymbolTextSpecial(sym.valueObject,f,"F1")
            #self.generateSymbolTextSpecial(footprintName,f,"F2")
            #self.generateSymbolTextSpecial(datasheet,f,"F3")
        # library footer
        print(r"""#
#End Library
""",file=f)
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

############## Symbol primitives ##############
    def generateSymbolTextSpecial(self, primitive, file, textType):
        """
        """
        p=primitive
        if p.rotation>360-45:
            rot="H"
        elif p.rotation>180+45:
            rot="V"
        elif p.rotation>180-45:
            rot="H"
        elif p.rotation>45:
            rot="V"
        else:
            rot="H"
        print(r'%s "%s" %d %d %d %s %s %sNN' % (textType, p.text, p.position[0]*self.scale,\
            p.position[1]*self.scale, p.height*self.scale, rot, "V" if p.visible else "I",\
            self.textAlignsSch[p.align]), file=file)
        # width, text, position, height, rotation = 0.0, align=textAlign.center, mirror=False):
                
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
        # calculate KiCad coordinates of arc: start point, end point and angle
        # ensure angles are in 0..360* range
        angles = [x % 360 for x in primitive.angles]
        end =[cos(angles[1])*primitive.radius + primitive.position[0],\
            sin(angles[1])*primitive.radius + primitive.position[1]]
        angle = (angles[1]-angles[0])%360
        print(r"  (fp_arc (start %1.3f %1.3f) (end %1.3f %1.3f) (angle %1.1f) (layer %s) (width %1.3f))"%\
            (primitive.position[0], -primitive.position[1], end[0], -end[1], angle,\
            self.layerNames[primitive.layer], primitive.width), file=file)
        pass

    def generatePcbCircle(self, primitive, file):
        """
        """
        print(r"  (fp_circle (center %1.3f %1.3f) (end %1.3f %1.3f) (layer %s) (width %1.3f))"%\
            (primitive.position[0], -primitive.position[1],\
            primitive.position[0]+primitive.radius, -primitive.position[1],\
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
        alignText = self.textAlignsPcb[primitive.align]
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
        pcbLayer.topNames:"F.Fab", pcbLayer.bottomNames:"B.Fab", \
        pcbLayer.topValues:"F.Fab", pcbLayer.bottomValues:"B.Fab",\
        pcbLayer.topPaste:"F.Paste", pcbLayer.bottomPaste:"B.Paste",\
        pcbLayer.topGlue:"F.Adhes", pcbLayer.bottomGlue:"B.Adhes",\
        pcbLayer.topKeepout:None, pcbLayer.bottomKeepout:None,\
        pcbLayer.topRestrict:None, pcbLayer.bottomRestrict:None,\
        pcbLayer.thtRestrict:None, pcbLayer.thtHoles:None,\
        pcbLayer.topAssembly:"F.Fab", pcbLayer.bottomAssembly:"B.Fab",\
        pcbLayer.topDocumentation:"F.Fab", pcbLayer.bottomDocumentation:"B.Fab"}
    
    textAlignsPcb = {textAlign.center:"", textAlign.centerLeft:" left",\
        textAlign.centerRight:" right", textAlign.topCenter:" top",\
        textAlign.topLeft:" left top", textAlign.topRight:" right top",\
        textAlign.bottomCenter:" bottom", textAlign.bottomLeft:" left bottom",\
        textAlign.bottomRight:" right bottom"}
        
    textAlignsSch = {textAlign.center:"C C", textAlign.centerLeft:"L C",\
        textAlign.centerRight:"R C", textAlign.topCenter:"C T",\
        textAlign.topLeft:"L T", textAlign.topRight:"R T",\
        textAlign.bottomCenter:"C B", textAlign.bottomLeft:"L B",\
        textAlign.bottomRight:"R B"}