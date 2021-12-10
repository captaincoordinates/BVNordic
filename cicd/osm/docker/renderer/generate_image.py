"""
Adapted from https://raw.githubusercontent.com/openstreetmap/mapnik-stylesheets/master/generate_image.py
"""

from logging import getLogger
from os import environ
from typing import Final  # type: ignore

import mapnik

LOGGER: Final = getLogger(__file__)

MERC: Final = mapnik.Projection(
    "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over"
)
LONLAT: Final = mapnik.Projection("+init=epsg:4326")


def generate() -> None:
    bounds = [float(bound) for bound in environ["EXTENT"].split(" ")]
    zoom = int(environ.get("MAPNIK_ZOOM", 5))
    imgx = 1000 * zoom
    imgy = 500 * zoom
    LOGGER.info(f"generating for {bounds} as {imgx}x{imgy}")

    map = mapnik.Map(imgx, imgy)
    mapnik.load_map(map, environ["MAPNIK_MAP_FILE"])
    map.srs = MERC.params()

    transform = mapnik.ProjTransform(LONLAT, MERC)
    bbox = transform.forward(mapnik.Box2d(*bounds))
    map.zoom_to_box(bbox)

    output_path = environ["OUTPUT_PNG_PATH"]
    mapnik.render_to_file(map, output_path, "png")
    LOGGER.info(f"rendered to {output_path}")


if __name__ == "__main__":
    generate()
