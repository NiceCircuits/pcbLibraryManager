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
from libraryManager.symbolPrimitive import *
import logging
import re

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
    
    scale=1
            
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
            # part header
            print(r"DEF %s %s 0 50 %s %s %d F N" %(part.name, part.refDes,\
                boolToYN(sym.showPinNumbers), boolToYN(sym.showPinNames),\
                len(part.symbols)), file=f)
            self.generateSymbolTextSpecial(sym.nameObject,f,"F0")
            sym.valueObject.text=part.name # to ensure compatibility with KiCad
            self.generateSymbolTextSpecial(sym.valueObject,f,"F1")
            footprint = symbolText(part.footprints[0].name if part.footprints else "",\
                translatePoints([sym.valueObject.position],[0, -1.5*sym.valueObject.height])[0],\
                defaults.symbolSmallTextHeight, visible=False, align = sym.valueObject.align)
            self.generateSymbolTextSpecial(footprint,f,"F2")
            #self.generateSymbolTextSpecial(datasheet,f,"F3")
            print("DRAW",file=f)
            # symbols
            for i in range(len(part.symbols)):
                s=part.symbols[i]
                for p in s.primitives:
                    self.generateSymbolPrimitive(p, f, gateNumber=i+1)
                for p in s.pins:
                    self.generateSymbolPin(p, f, gateNumber=i+1)
            # part footer
            print("ENDDRAW\nENDDEF",file=f)
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
        print(r'%s "%s" %d %d %d %s %s %sNN' % (textType, p.text, round(p.position[0]*self.scale),\
            round(p.position[1]*self.scale), round(p.height*self.scale), rot, "V" if p.visible else "I",\
            self.textAlignsSch[p.align]), file=file)
        # width, text, position, height, rotation = 0.0, align=textAlign.center, mirror=False):

    def generateSymbolPrimitive(self, primitive, file, gateNumber=1):
        """
        """
        p = primitive
        n = p.__class__.__name__
        if n == "symbolLine":
            primitive.__class__= symbolPolyline
            self.generateSymbolPrimitive(primitive, file, gateNumber)
        elif n == "symbolPolyline":
            pointsStr=""
            for p in primitive.points:
                pointsStr += "%d %d " %(round(p[0]*self.scale), round(p[1]*self.scale))
            print(r"P %d %d 1 %d %s%s" %(len(primitive.points), gateNumber, round(primitive.width),\
                pointsStr, self.symbolFillType[primitive.filled]), file=file)
        elif n == "symbolRectangle":
            c = rotatePoints(rectangleCorners(p.position, p.dimensions),p.rotation)
            print(r"S %d %d %d %d %d 1 %d %s"%(round(c[0][0]*self.scale), round(c[0][1]*self.scale),\
                round(c[1][0]*self.scale), round(c[1][1]*self.scale), gateNumber, round(p.width*self.scale),\
                self.symbolFillType[p.filled]), file=file)
        elif n == "symbolArc":
            pass
        elif n == "symbolCircle":
            print(r"C %d %d %d %d 1 %d %s" %(round(p.position[0]*self.scale),\
                round(p.position[1]*self.scale), round(p.radius*self.scale),\
                gateNumber, round(p.width*self.scale), self.symbolFillType[p.filled]),\
                file=file)
        elif n == "symbolText":
            pass
        else:
            text = "generateSymbolPrimitive: Invalid primitive class name: %s" % n
            self.log.error(text)
            raise TypeError(text)
    
    def generateSymbolPin(self, pin, file, gateNumber=1):
        """
        """
        name = re.sub(r"\s", r"_", str(pin.name))
        print(r"X %s %s %d %d %d %s %d %d %d 1 %s"%(name, pin.number, round(pin.position[0]*self.scale),\
            round(pin.position[1]*self.scale), round(pin.length*self.scale), self.symbolPinAngle[pin.rotation],\
            round(pin.heightNumber*self.scale), round(pin.heightName*self.scale), gateNumber, self.symbolPinType[pin.type]), file=file)

        
                
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
        elif n == "pcbText":
            return self.generatePcbText(primitive, file)
        elif n == "pcbArc":
            # calculate KiCad coordinates of arc: start point, end point and angle
            # ensure angles are in 0..360* range
            angles = [x % 360 for x in primitive.angles]
            end =[cos(angles[1])*primitive.radius + primitive.position[0],\
                sin(angles[1])*primitive.radius + primitive.position[1]]
            angle = (angles[1]-angles[0])%360
            print(r"  (fp_arc (start %1.3f %1.3f) (end %1.3f %1.3f) (angle %1.1f) (layer %s) (width %1.3f))"%\
                (primitive.position[0], -primitive.position[1], end[0], -end[1], angle,\
                self.layerNames[primitive.layer], primitive.width), file=file)
        elif n == "pcbCircle":
            print(r"  (fp_circle (center %1.3f %1.3f) (end %1.3f %1.3f) (layer %s) (width %1.3f))"%\
                (primitive.position[0], -primitive.position[1],\
                primitive.position[0]+primitive.radius, -primitive.position[1],\
                self.layerNames[primitive.layer], primitive.width), file=file)
        elif n == "pcbThtPad":
            layerText = r"*.Cu *.Mask"
            print(r"  (pad %s thru_hole %s (at %1.3f %1.3f %1.1f) (size %1.3f %1.3f) (drill %1.3f) (layers %s))" %\
                (primitive.name, self.padShape[primitive.shape], primitive.position[0],\
                -primitive.position[1], primitive.rotation, primitive.dimensions[0],\
                primitive.dimensions[1], primitive.drill, layerText), file=file)
        elif n == "pcbSmtPad":
            if primitive.layer==pcbLayer.topCopper:
                #TODO: paste on/off
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
        elif n == "pcb3DBody":
            p=primitive
            print(r"""  (model %s.wrl
    (at (xyz %1.3f %1.3f %1.3f))
    (scale (xyz %1.3f %1.3f %1.3f))
    (rotate (xyz %1.3f %1.3f %1.3f))
  )""" %(p.name, mm2inch(p.position[0]), mm2inch(p.position[1]), mm2inch(p.position[2]),\
      p.dimensions[0], p.dimensions[1], p.dimensions[2],\
      p.rotations[0], p.rotations[1], -p.rotations[2]), file=file)
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
        print(r"""  (fp_text %s %s (at %1.3f %1.3f  %1.1f) (layer %s)%s
    (effects (font (size %1.3f %1.3f) (thickness %1.3f))%s)
  )""" % (textType, primitive.text, primitive.position[0], -primitive.position[1],\
            primitive.rotation, self.layerNames[primitive.layer],\
            "" if primitive.visible else " hide", primitive.height,\
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
        pcbLayer.topDocumentation:"F.Fab", pcbLayer.bottomDocumentation:"B.Fab",\
        pcbLayer.topCourtyard:"F.CrtYd", pcbLayer.bottomCourtyard:"B.CrtYd"}
    
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
        
    symbolPinAngle={0:"R", 90:"U", 180:"L", 270:"D"}
    
    symbolPinType={pinType.input:"I", pinType.output:"O", pinType.IO:"B", pinType.tristate:"T",\
        pinType.passive:"P", pinType.OC:"C", pinType.NC:"N", pinType.pwrIn:"W", pinType.pwrOut:"w"}
    
    symbolFillType={fillType.none:"N", fillType.background:"f", fillType.foreground:"F"}
    
    padShape={padShape.rect:"rect", padShape.round:"circle", padShape.roundRect:"oval"}