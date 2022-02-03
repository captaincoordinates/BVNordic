from argparse import ArgumentParser
from logging import getLogger
from os import path, remove
from pathlib import Path
from re import search
from typing import Final  # type: ignore

from PIL import Image
from qgis.core import (
    QgsApplication,
    QgsLabelLineSettings,
    QgsLayoutExporter,
    QgsProject,
    QgsVectorLayer,
)
from yaml import safe_load

LOGGER: Final = getLogger(__file__)
MAX_IMAGE_DIMENSION: Final = 1600


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

    # working label position locking
    # need to drive from outputs.yml and argument whether or not to enable label locking
    # enable from compare calls, disable from export calls
    candidates = [
        layer for layer in project.mapLayers().values() if layer.name() == "Trails"
    ]
    if len(candidates) == 1 and isinstance(candidates[0], QgsVectorLayer):
        layer = candidates[0]
        for rule in layer.labeling().rootRule().children():
            settings = rule.settings()
            line_settings = settings.lineSettings()
            line_settings.setAnchorType(QgsLabelLineSettings.AnchorType.Strict)
            settings.setLineSettings(line_settings)
            rule.setSettings(settings)

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

        png_path = path.join(output_dir, f"{layout_name}.png")
        pdf_path = path.join(output_dir, f"{layout_name}.pdf")

        if png:
            LOGGER.info(f"Exporting {layout_name} PNG")
            export_png(png_path, export)

        if pdf:
            LOGGER.info(f"Exporting {layout_name} PDF")
            export_pdf(pdf_path, export)

        if layout_name in thumbnails_by_layout:
            LOGGER.info(f"Exporting {layout_name} PNG thumbnail")
            size = thumbnails_by_layout[layout_name]["size"]
            clean = False
            if not path.exists(png_path):
                export_png(png_path, export)
                clean = True
            thumbnail = Image.open(png_path)
            thumbnail.thumbnail((size, size))
            thumbnail.save(path.join(output_dir, f"{layout_name}-thumbnail.png"))
            if clean:
                remove(png_path)

    qgs.exitQgis()


def export_png(path: str, exporter: QgsLayoutExporter) -> None:
    exporter.exportToImage(
        path,
        QgsLayoutExporter.ImageExportSettings(),
    )
    large_image = Image.open(path)
    large_image.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION))
    large_image.save(path)


def export_pdf(path: str, exporter: QgsLayoutExporter) -> None:
    exporter.exportToPdf(
        path,
        QgsLayoutExporter.PdfExportSettings(),
    )


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
