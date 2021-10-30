from argparse import ArgumentParser
from logging import getLogger
from os import path
from pathlib import Path
from re import search
from typing import Final  # type: ignore

from PIL import Image
from qgis.core import QgsApplication, QgsLayoutExporter, QgsProject
from yaml import safe_load

LOGGER: Final = getLogger(__file__)


def execute(  # noqa: C901
    project_name: str, output_base: str, png: bool, pdf: bool
) -> None:

    if not (png or pdf):
        return

    with open(path.join(path.dirname(__file__), "outputs.yml"), "r") as config_file:
        try:
            config = safe_load(config_file)[project_name]
        except KeyError:
            raise Exception(f"Project {project_name} does not exist in config")

    QgsApplication.setPrefixPath("/usr/bin/qgis", True)
    qgs = QgsApplication([], False)
    qgs.initQgis()
    project = QgsProject.instance()
    project.read(f"{project_name}.qgs")
    output_dir = path.join(output_base, project_name)
    Path(output_dir).mkdir(exist_ok=True)
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

        if png:
            export.exportToImage(
                path.join(output_dir, f"{layout_name}.png"),
                QgsLayoutExporter.ImageExportSettings(),
            )
            if layout_name in thumbnails_by_layout:
                size = thumbnails_by_layout[layout_name]["size"]
                thumbnail = Image.open(path.join(output_dir, f"{layout_name}.png"))
                thumbnail.thumbnail((size, size))
                thumbnail.save(path.join(output_dir, f"{layout_name}-thumbnail.png"))

        if pdf:
            export.exportToPdf(
                path.join(output_dir, f"{layout_name}.pdf"),
                QgsLayoutExporter.PdfExportSettings(),
            )

    qgs.exitQgis()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "project_name", type=str, help="Name of the QGIS project to export"
    )
    parser.add_argument(
        "output_base", type=str, help="Directory in which to generate output"
    )
    parser.add_argument(
        "--png",
        dest="png",
        action="store_true",
        help="Generate PNG output",
    )
    parser.add_argument(
        "--pdf",
        dest="pdf",
        action="store_true",
        help="Generate PDF output",
    )
    parser.set_defaults(png=False)
    parser.set_defaults(pdf=False)
    args = vars(parser.parse_args())
    LOGGER.info(f"{__file__} called with {args}")
    execute(args["project_name"], args["output_base"], args["png"], args["pdf"])
