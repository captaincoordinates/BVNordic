from qgis.core import *
from qgis.gui import *
from qgis.utils import iface

@qgsfunction(args='auto', group='Custom')
def applyMmOffsetX(feature, parent):
    scale = iface.mapCanvas().scale()
    attribute = feature.attribute("DISP_OFF")
    if attribute != NULL:
        strDispOff = str(attribute)
        dispOffParts = strDispOff.split(",")
        dispOffX = float(dispOffParts[0])
        locationPoint = feature.geometry().asPoint()
        locationPointX = locationPoint.x()
        labelPoint = locationPoint.project(dispOffX / 1000 * scale, 90)
        return labelPoint.x()
        
@qgsfunction(args='auto', group='Custom')
def applyMmOffsetY(feature, parent):
    scale = iface.mapCanvas().scale()
    attribute = feature.attribute("DISP_OFF")
    if attribute != NULL:
        strDispOff = str(attribute)
        dispOffParts = strDispOff.split(",")
        dispOffY = float(dispOffParts[1])
        locationPoint = feature.geometry().asPoint()
        locationPointX = locationPoint.y()
        labelPoint = locationPoint.project(dispOffY / 1000 * scale, 180)
        return labelPoint.y()
