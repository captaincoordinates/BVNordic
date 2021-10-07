"""
Call with `qgis --nologo --project main.qgs --code ci/export.py`
Script is only run via QGIS, will not run standalone
"""

from os import _exit, environ
from os.path import expanduser, join
from uuid import uuid4


layout_name = environ.get("PDF_LAYOUT_NAME", "Print")
filename = environ.get("PDF_OUTPUT_PATH", join(expanduser("~"), f"{uuid4()}.pdf"))
projectInstance = QgsProject.instance()
layoutmanager = projectInstance.layoutManager()
layout_item = layoutmanager.layoutByName(layout_name)
export = QgsLayoutExporter(layout_item)
export.exportToPdf(filename, QgsLayoutExporter.PdfExportSettings())

_exit(0)