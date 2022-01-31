from http import HTTPStatus
from logging import getLogger
from math import atan, cos, degrees, floor, log, pi, radians, sinh, tan
from os import path
from random import choice
from typing import Final, List, Tuple  # type: ignore

from osgeo.gdal import BuildVRT, Translate
from PIL import Image
from requests import get

from cicd.imagery.bounds import Bounds
from cicd.imagery.settings import EPSG_3857, EPSG_4326

LOGGER: Final = getLogger(__file__)
OUTPUT_DIR: Final = path.join(path.dirname(__file__), "output")
MERCATOR_AXIS_MAX: Final = 20037508.3427892


def execute(
    tile_src: str, zoom: int, bounds: Bounds, image_name: str, target_epsg_code: str
) -> None:
    x_min, x_max, y_min, y_max = bbox_to_xyz(
        bounds.lonmin, bounds.lonmax, bounds.latmin, bounds.latmax, zoom
    )
    LOGGER.info(f"Fetching up to {(x_max - x_min + 1) * (y_max - y_min + 1)} tiles")
    tmpdirpath = path.join(path.dirname(__file__), "tmp")
    tif_paths = []
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            img_base = path.join(tmpdirpath, f"{x}_{y}_{zoom}_{image_name}.")
            png_path = f"{img_base}png"
            png_rgb_path = f"{img_base}rgb.png"
            tif_path = f"{img_base}tif"
            if path.exists(tif_path):
                LOGGER.debug(f"file exists {tif_path}")
            else:
                try:
                    if not path.exists(png_path):
                        url = tile_src.format(x=x, y=y, z=zoom)
                        LOGGER.debug(f"retrieving {url}")
                        with get(
                            url, headers={"User-Agent": get_random_user_agent()}
                        ) as response:
                            if response.status_code == HTTPStatus.OK:
                                with open(png_path, "wb") as file:
                                    file.write(response.content)
                            else:
                                LOGGER.warning(
                                    f"failed to retrieve {url}: {response.status_code}, {response.text}"
                                )
                    png_use_path = png_path
                    if Image.open(png_path).mode == "P":
                        Translate(png_rgb_path, png_path, rgbExpand="rgb")
                        png_use_path = png_rgb_path
                    georeference_tile(
                        target_epsg_code, x, y, zoom, png_use_path, tif_path
                    )
                except Exception as e:
                    LOGGER.error(e)
                    raise e
            tif_paths.append(tif_path)

    LOGGER.info("generating merged tif")
    vrt = BuildVRT("", tif_paths, addAlpha=True)
    Translate(
        path.join(OUTPUT_DIR, f"{image_name}.tif"),
        vrt,
        format="GTiff",
        projWin=[
            bounds.lonmin,
            bounds.latmax,
            bounds.lonmax,
            bounds.latmin,
        ],
        projWinSRS=EPSG_4326,
    )


def bbox_to_xyz(
    lon_min: float, lon_max: float, lat_min: float, lat_max: float, z: int
) -> Tuple[int, int, int, int]:
    def sec(x):
        return 1 / cos(x)

    def latlon_to_xyz(lat, lon, z):
        tile_count = pow(2, z)
        x = (lon + 180) / 360
        y = (1 - log(tan(radians(lat)) + sec(radians(lat))) / pi) / 2
        return (tile_count * x, tile_count * y)

    x_min, y_max = latlon_to_xyz(lat_min, lon_min, z)
    x_max, y_min = latlon_to_xyz(lat_max, lon_max, z)

    return (floor(x_min), floor(x_max), floor(y_min), floor(y_max))


def georeference_tile(
    epsg_code: str, x: int, y: int, z: int, tile_path: str, output_path: str
) -> None:
    bounds_providers = {
        EPSG_4326: tile_bounds_4326,
        EPSG_3857: tile_bounds_3857,
    }
    if epsg_code not in bounds_providers.keys():
        raise Exception(
            f"cannot georeference tile in {epsg_code}. Options: {bounds_providers.keys()}"
        )
    bounds = bounds_providers[epsg_code](x, y, z)
    filename, _ = path.splitext(tile_path)
    Translate(output_path, tile_path, outputSRS=epsg_code, outputBounds=bounds)


def tile_bounds_3857(x: int, y: int, z: int) -> List[float]:
    tile_count = pow(2, z)
    tile_length = (MERCATOR_AXIS_MAX * 2) / tile_count
    return [
        -MERCATOR_AXIS_MAX + tile_length * x,
        MERCATOR_AXIS_MAX - tile_length * y,
        -MERCATOR_AXIS_MAX + tile_length * (x + 1),
        MERCATOR_AXIS_MAX - tile_length * (y + 1),
    ]


def tile_bounds_4326(x: int, y: int, z: int) -> List[float]:
    def mercatorToLat(mercatorY: int) -> float:
        return degrees(atan(sinh(mercatorY)))

    def y_to_lat_edges(y: int, z: int) -> Tuple[float, float]:
        tile_count = pow(2, z)
        unit = 1 / tile_count
        relative_y1 = y * unit
        relative_y2 = relative_y1 + unit
        lat1 = mercatorToLat(pi * (1 - 2 * relative_y1))
        lat2 = mercatorToLat(pi * (1 - 2 * relative_y2))
        return (lat1, lat2)

    def x_to_lon_edges(x: int, z: int) -> Tuple[float, float]:
        tile_count = pow(2, z)
        unit = 360 / tile_count
        lon1 = -180 + x * unit
        lon2 = lon1 + unit
        return (lon1, lon2)

    def tile_edges(x: int, y: int, z: int) -> List[float]:
        lat1, lat2 = y_to_lat_edges(y, z)
        lon1, lon2 = x_to_lon_edges(x, z)
        return [lon1, lat1, lon2, lat2]

    return tile_edges(x, y, z)


# https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
def get_random_user_agent() -> str:
    user_agent_list = (
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        # Firefox
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
    )
    return choice(user_agent_list)
