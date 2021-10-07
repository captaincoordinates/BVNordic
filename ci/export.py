"""
Call with `docker build -t exporter ci && docker run --rm -v $PWD:/export -v ~/Desktop/pdf:/output -e PDF_OUTPUT_PATH=/output/map.pdf exporter`
Generated output at ~/Desktop/pdf/map.pdf
"""

from os import environ
from os.path import expanduser, join
from qgis.core import QgsApplication, QgsLayoutExporter, QgsProject
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