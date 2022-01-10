"""
Adapted from https://raw.githubusercontent.com/openstreetmap/mapnik-stylesheets/master/generate_image.py
"""

from logging import getLogger
from os import environ
from typing import Final  # type: ignore

import mapnik

LOGGER: Final = getLogger(__file__)


def generate() -> None:
    bounds_4326 = [float(bound) for bound in environ["EXTENT_4326"].split(" ")]
    x_range = bounds_4326[2] - bounds_4326[0]
    x_tiles = x_range / 0.003
    x_pixel = x_tiles * 256
    bounds_3857 = [float(bound) for bound in environ["EXTENT_3857"].split(" ")]
    ratio_3857 = (bounds_3857[3] - bounds_3857[1]) / (bounds_3857[2] - bounds_3857[0])
    y_pixel = x_pixel * ratio_3857
    imgx, imgy = round(x_pixel), round(y_pixel)

    LOGGER.info(f"generating for {bounds_4326} as {imgx}x{imgy}")

    map = mapnik.Map(imgx, imgy)
    mapnik.load_map(map, environ["MAPNIK_MAP_FILE"])
    map.aspect_fix_mode = mapnik.aspect_fix_mode.RESPECT
    map.zoom_to_box(mapnik.Box2d(*bounds_3857))

    output_path = environ["OUTPUT_PNG_PATH"]
    mapnik.render_to_file(map, output_path, "png")
    LOGGER.info(f"rendered to {output_path}")


if __name__ == "__main__":
    generate()
