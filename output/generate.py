from os import environ
from os.path import join
from pathlib import Path
from re import search

from PIL import Image
from qgis.core import QgsApplication, QgsLayoutExporter, QgsProject
from yaml import safe_load

PROJECT_KEY = "PROJECT"
OUTPUT_BASE_KEY = "OUTPUT_BASE"

if PROJECT_KEY not in environ:
    raise Exception(f"{PROJECT_KEY} must be provided")

if OUTPUT_BASE_KEY not in environ:
    raise Exception(f"{OUTPUT_BASE_KEY} must be provided")

project_name = environ[PROJECT_KEY]
with open("/export/output/outputs.yml", "r") as config_file:
    try:
        config = safe_load(config_file)[project_name]
    except KeyError:
        raise Exception(f"Project {environ[PROJECT_KEY]} does not exist in config")


QgsApplication.setPrefixPath("/usr/bin/qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()
project = QgsProject.instance()
project.read(f"{environ.get(PROJECT_KEY)}.qgs")
output_base = join(environ.get(OUTPUT_BASE_KEY), project_name)
Path(output_base).mkdir(exist_ok=True)
layout_manager = project.layoutManager()

common_layers = config["common_layers"]
thumbnails_by_layout = (
    {thumbnail["layout"]: thumbnail for thumbnail in config["thumbnails"]}
    if "thumbnails" in config
    else dict()
)

for layout in layout_manager.layouts():
    layout_name = layout.name()
    visible_layers = common_layers.copy()

    for special_config in config["special_configs"]:
        for special_layout in special_config["layouts"]:
            if search(special_layout, layout_name):
                visible_layers.extend(special_config["layers"])

    for layer_id, layer in project.mapLayers().items():
        show = False
        if layer.name() in visible_layers:
            show = True
        project.layerTreeRoot().findLayer(layer_id).setItemVisibilityChecked(show)

    item = layout_manager.layoutByName(layout_name)
    export = QgsLayoutExporter(item)
    export.exportToImage(
        join(output_base, f"{layout_name}.png"), QgsLayoutExporter.ImageExportSettings()
    )
    export.exportToPdf(
        join(output_base, f"{layout_name}.pdf"), QgsLayoutExporter.PdfExportSettings()
    )

    if layout_name in thumbnails_by_layout:
        thumbnail = Image.open(join(output_base, f"{layout_name}.png"))
        thumbnail.thumbnail(
            (
                thumbnails_by_layout[layout_name]["size"],
                thumbnails_by_layout[layout_name]["size"],
            )
        )
        thumbnail.save(join(output_base, f"{layout_name}-thumbnail.png"))

qgs.exitQgis()
