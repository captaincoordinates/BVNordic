from os import _exit, environ
from os.path import expanduser, join
from uuid import uuid4

def writelog(line):
    with open("/tmp/exlog", "a") as f:
        f.write(line)
        f.flush()

writelog("0")

layout_name = environ.get("PDF_LAYOUT_NAME", "Print")
filename = environ.get("PDF_OUTPUT_PATH", join(expanduser("~"), f"{uuid4()}.pdf"))
writelog("1")
projectInstance = QgsProject.instance()
writelog("2")
layoutmanager = projectInstance.layoutManager()
writelog("3")
layout_item = layoutmanager.layoutByName(layout_name)
writelog("4")
export = QgsLayoutExporter(layout_item)
writelog("5")
export.exportToPdf(filename, QgsLayoutExporter.PdfExportSettings())
writelog("6")

_exit(0)