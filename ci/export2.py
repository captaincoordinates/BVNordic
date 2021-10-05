from qgis.core import QgsApplication
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
from qgis.core import *
from qgis.utils import iface
from os import _exit, environ
from os.path import expanduser, join
from uuid import uuid4

layout_name = environ.get("PDF_LAYOUT_NAME", "Print")
filename = environ.get("PDF_OUTPUT_PATH", join(expanduser("~"), f"{uuid4()}.pdf"))

print("1")

QgsApplication.setPrefixPath("/usr/bin/qgis", True)
print("2")
qgs = QgsApplication([], False)
print("3")
 
# Load providers
qgs.initQgis()
print("4")

project = QgsProject.instance()
print("5")
project.read("./main.qgs")

print("6")

layoutmanager = project.layoutManager()
layout_item = layoutmanager.layoutByName(layout_name)
export = QgsLayoutExporter(layout_item)
export.exportToPdf(filename, QgsLayoutExporter.PdfExportSettings())
 
# Finally, exitQgis() is called to remove the
# provider and layer registries from memory
qgs.exitQgis()