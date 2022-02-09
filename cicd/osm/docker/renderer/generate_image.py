"""
Adapted from https://raw.githubusercontent.com/openstreetmap/mapnik-stylesheets/master/generate_image.py
"""

from hashlib import md5
from json import dumps, loads
from logging import getLogger
from os import environ, linesep, path
from tempfile import mkstemp
from typing import Final  # type: ignore

import mapnik
from osgeo.gdal import Translate, Warp

from cicd.imagery.bounds import Bounds as DownloadBounds
from cicd.imagery.tiles_to_tiff import EPSG_3857, execute as download_bg_img
from cicd.osm.docker.renderer.common import image_dims_for_rect

LOGGER: Final = getLogger(__file__)
TILE_URL: Final = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"


def generate() -> None:
    pixel_max = int(environ.get("PIXEL_MAX", 1200))
    with open(environ["BOUNDS_3857_FILE"], "r") as f:
        bounds_rect = loads(f.read())["features"][0]["geometry"]["coordinates"][0]
    rect_id = md5(dumps(bounds_rect).encode()).hexdigest()
    preferred_candidate = None
    # assumes candidates list is ordered zoom_level ascending
    for candidate in image_dims_for_rect(bounds_rect):
        if candidate.x <= pixel_max and candidate.y <= pixel_max:
            preferred_candidate = candidate
    bg_img_path = download_bg_img(
        TILE_URL,
        preferred_candidate.zoom_level,
        DownloadBounds(
            xmin=bounds_rect[0][0],
            xmax=bounds_rect[1][0],
            ymin=bounds_rect[0][1],
            ymax=bounds_rect[2][1],
        ),
        f"{rect_id}-{md5(TILE_URL.encode()).hexdigest()}",
        EPSG_3857,
        EPSG_3857,
    )
    if preferred_candidate is None:
        LOGGER.error(
            f"Unable to determine preferred export candidate from list: {linesep}{image_dims_for_rect(bounds_rect)}"
        )
    map = mapnik.Map(preferred_candidate.x, preferred_candidate.y)
    mapnik.load_map(map, environ["MAPNIK_MAP_FILE"])
    map.aspect_fix_mode = mapnik.aspect_fix_mode.RESPECT
    map.zoom_to_box(
        mapnik.Box2d(
            bounds_rect[0][0],
            bounds_rect[0][1],
            bounds_rect[1][0],
            bounds_rect[2][1],
        )
    )
    _, png_path = mkstemp()
    _, change_tif_path = mkstemp()
    _, merge_tif_path = mkstemp()
    output_png_path = path.join(
        environ["OUTPUT_DIR"],
        f"{environ.get('OUTPUT_PREFIX', 'osm-')}{rect_id}.png",
    )
    mapnik.render_to_file(map, png_path, "png")
    Translate(
        change_tif_path,
        png_path,
        format="GTIFF",
        outputBounds=[
            bounds_rect[0][0],
            bounds_rect[3][1],
            bounds_rect[1][0],
            bounds_rect[0][1],
        ],
    )
    Warp(merge_tif_path, [bg_img_path, change_tif_path])
    Translate(output_png_path, merge_tif_path, format="PNG", options="zlevel=9")
    LOGGER.info(f"rendered to {output_png_path}")


if __name__ == "__main__":
    generate()
