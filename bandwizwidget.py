from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
import os



from qgis.core import (
    # QgisInterface,
    QgsMapLayer,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsRasterRenderer,
    QgsMultiBandColorRenderer,
    QgsSingleBandGrayRenderer,
    QgsContrastEnhancement
)


class BandWizWidget(QtWidgets.QWidget):
    def __init__(self, iface):
        super(BandWizWidget, self).__init__(None)
        # print("init")
        hlayout = QtWidgets.QHBoxLayout()

        basepath = os.path.dirname(os.path.realpath(__file__))
        rgbipath = os.path.join(basepath,"res","rgbi.png")
        bgripath = os.path.join(basepath,"res","bgri.png")

        self.infoLbl = QtWidgets.QLabel("")
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.RGBIbut = QtWidgets.QPushButton(QtGui.QIcon(rgbipath), "RGBI")
        self.BGRIbut = QtWidgets.QPushButton(QtGui.QIcon(bgripath), "BGRI")
        
        # self.BGRIbut = QtWidgets.QPushButton("BGRI")
        self.onlRbut = QtWidgets.QPushButton("band 1")
        self.onlGbut = QtWidgets.QPushButton("band 2")
        self.onlBbut = QtWidgets.QPushButton("band 3")
        self.onlIbut = QtWidgets.QPushButton("band 4")
        self.RGBIbut.setCheckable(True)
        self.BGRIbut.setCheckable(True)
        self.onlRbut.setCheckable(True)
        self.onlGbut.setCheckable(True)
        self.onlBbut.setCheckable(True)
        self.onlIbut.setCheckable(True)
        self.buttonGroup.addButton(self.RGBIbut)
        self.buttonGroup.addButton(self.BGRIbut)
        self.buttonGroup.addButton(self.onlRbut)
        self.buttonGroup.addButton(self.onlGbut)
        self.buttonGroup.addButton(self.onlBbut)
        self.buttonGroup.addButton(self.onlIbut)
        self.buttonGroup.setExclusive(True)
        self.RGBIbut.setChecked(True)
        # self.colrbut = QtWidgets.QPushButton("Invert")
        self.morebut = QtWidgets.QPushButton("Adv Settings")
        hlayout.addWidget(self.infoLbl)
        # hlayout.addWidget(buttonGroup)
        hlayout.addWidget(self.RGBIbut)
        hlayout.addWidget(self.BGRIbut)
        hlayout.addWidget(self.onlRbut)
        hlayout.addWidget(self.onlGbut)
        hlayout.addWidget(self.onlBbut)
        hlayout.addWidget(self.onlIbut)
        
        # hlayout.addWidget(self.colrbut)
        hlayout.addStretch()
        hlayout.addWidget(self.morebut)
        self.setLayout(hlayout)
        self.iface = iface
        self.setLayer(self.iface.activeLayer())
        # self.setBackgroundRole(QtGui.QPalette.Light)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(10,160,18))
        p.setColor(self.foregroundRole(), QtGui.QColor(125,64,22))
        self.setPalette(p)
        
        #signal slot connections
        self.iface.currentLayerChanged.connect(self.setLayer)
        self.RGBIbut.clicked.connect(self.orderAsRGBI)
        self.BGRIbut.clicked.connect(self.orderAsBGRI)
        self.onlRbut.clicked.connect(self.rBandGrayscale)
        self.onlGbut.clicked.connect(self.gBandGrayscale)
        self.onlBbut.clicked.connect(self.bBandGrayscale)
        self.onlIbut.clicked.connect(self.irBandGrayscale)
        self.morebut.clicked.connect(self.showLayerProperties)

    def setLayer(self, layer):
        #if layer is not raster, return
        #check if single band or multiband
        #enable options accordingly
        self.curLayer = None
        if layer is None:
            self.infoLbl.setText("-----")
            self.setEnabled(False)
            return #no layer selected

        if layer.type() != QgsMapLayer.RasterLayer:
            self.infoLbl.setText("Not Raster")
            self.setEnabled(False)
            return
        self.setEnabled(True)
        self.numBands = layer.bandCount()
        # if self.numBands <= 1:
        #     self.layout().setEnabled(False)

        if self.numBands < 1:
            self.infoLbl.setText(f"Raster (empty)")
        elif self.numBands == 1:
            self.infoLbl.setText(f"Raster ({self.numBands} band)")
        elif self.numBands > 1:
            self.infoLbl.setText(f"Raster ({self.numBands} bands)")
        # self.layout().setEnabled(True)
        
        for b in range(2,6):
            if b < self.numBands+2 :
                self.buttonGroup.buttons()[b].setEnabled(True)
            else:
                self.buttonGroup.buttons()[b].setEnabled(False)

        if self.numBands < 3:
            self.RGBIbut.setEnabled(False)
            self.BGRIbut.setEnabled(False)
        else:
            self.RGBIbut.setEnabled(True)
            self.BGRIbut.setEnabled(True)

        self.curLayer = layer

        #get the renderer state for the current layer
        renderer = self.curLayer.renderer().clone()
        if isinstance(renderer, QgsMultiBandColorRenderer):
            if renderer.redBand() == 1:
                self.RGBIbut.setChecked(True)
            elif renderer.redBand() == 3:
                self.BGRIbut.setChecked(True)
        elif isinstance(renderer, QgsSingleBandGrayRenderer):
            if renderer.grayBand() == 1:
                self.onlRbut.setChecked(True)
            elif renderer.grayBand() == 2:
                self.onlGbut.setChecked(True)
            elif renderer.grayBand() == 3:
                self.onlBbut.setChecked(True)
            if renderer.grayBand() == 4:
                self.onlIbut.setChecked(True)
        else:
            print("Unhandled rendering.")
            self.layout().setEnabled(False)

       

    def orderAsRGBI(self):
        if self.curLayer is None:
            return
        # renderer = self.curLayer.renderer().clone()
        # renderer.setRedBand(1)
        # renderer.setGreenBand(2)
        # renderer.setBlueBand(3)
        renderer = QgsMultiBandColorRenderer(self.curLayer.dataProvider(), 1,2,3)
        self.curLayer.setRenderer(renderer)
        self.curLayer.setDefaultContrastEnhancement()
        self.curLayer.triggerRepaint()
        # print("orderAsRGBI")

    def orderAsBGRI(self):
        if self.curLayer is None:
            return
        # renderer = self.curLayer.renderer().clone()
        # renderer.setRedBand(3)
        # renderer.setGreenBand(2)
        # renderer.setBlueBand(1)
        renderer = QgsMultiBandColorRenderer(self.curLayer.dataProvider(), 3,2,1)
        self.curLayer.setRenderer(renderer)
        self.curLayer.setDefaultContrastEnhancement()
        self.curLayer.triggerRepaint()
        # print("orderAsBGRI")
    
    def rBandGrayscale(self):
        if self.curLayer is None:
            return
        # renderer = self.curLayer.renderer().clone()
        # if isinstance(renderer, QgsMultiBandColorRenderer):
        #     print("Multiband renderer")
        #     renderer.setRedBand(1)
        #     renderer.setGreenBand(1)
        #     renderer.setBlueBand(1)
        # elif isinstance(renderer, QgsSingleBandGrayRenderer):
        #     print("Single band renderer")
        #     renderer.setGrayBand(1)
        renderer = QgsSingleBandGrayRenderer(self.curLayer.dataProvider(), 1)
        self.curLayer.setRenderer(renderer)
        self.curLayer.setDefaultContrastEnhancement()
        self.curLayer.triggerRepaint()
        # print("rBandGrayscale")

    def gBandGrayscale(self):
        if self.curLayer is None:
            return
        renderer = QgsSingleBandGrayRenderer(self.curLayer.dataProvider(), 2)
        self.curLayer.setRenderer(renderer)
        self.curLayer.setDefaultContrastEnhancement()
        self.curLayer.triggerRepaint()
        # print("gBandGrayscale")

    def bBandGrayscale(self):
        if self.curLayer is None:
            return
        renderer = QgsSingleBandGrayRenderer(self.curLayer.dataProvider(), 3)
        self.curLayer.setRenderer(renderer)
        self.curLayer.setDefaultContrastEnhancement()
        self.curLayer.triggerRepaint()
        # print("bBandGrayscale")

    def irBandGrayscale(self):
        if self.curLayer is None:
            return
        renderer = QgsSingleBandGrayRenderer(self.curLayer.dataProvider(), 4)
        self.curLayer.setRenderer(renderer)
        self.curLayer.setDefaultContrastEnhancement()
        self.curLayer.triggerRepaint()
        # print("irBandGrayscale")

    def showLayerProperties(self):
        print("showLayerProperties")
        if self.curLayer is None:
            return
        self.iface.showLayerProperties(self.curLayer,'mOptsPage_Style')
