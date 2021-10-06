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

QgsApplication.setPrefixPath("/usr/bin/qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()
project = QgsProject.instance()
project.read("./main.qgs")

layoutmanager = project.layoutManager()
layout_item = layoutmanager.layoutByName(layout_name)
export = QgsLayoutExporter(layout_item)
settings = QgsLayoutExporter.PdfExportSettings()
settings.dpi = 96
export.exportToPdf(filename, settings)

qgs.exitQgis()