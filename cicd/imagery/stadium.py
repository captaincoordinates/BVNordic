from os import environ, path
from typing import Final  # type: ignore

from osgeo import ogr
from pyproj import Transformer

from cicd.imagery.bounds import Bounds
from cicd.imagery.settings import EPSG_3857, EPSG_4326
from cicd.imagery.tiles_to_tiff import execute as tiles_to_tiff

TILE_SRC: Final = environ.get(
    "STADIUM_TILE_SRC",
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
)
ZOOM: Final = environ.get("STADIUM_TILE_ZOOM", 17)


def execute() -> None:
    gpkg_driver = ogr.GetDriverByName("GPKG")
    data_source = gpkg_driver.Open(
        path.abspath(path.join(path.dirname(__file__), "..", "..", "stadium-data.gpkg"))
    )
    opacity_layer = data_source.GetLayerByName("opacity_cover")
    opacity_extent = opacity_layer.GetExtent()
    transformer = Transformer.from_crs(EPSG_3857, EPSG_4326)
    latmin, lonmin = transformer.transform(opacity_extent[0], opacity_extent[2])
    latmax, lonmax = transformer.transform(opacity_extent[1], opacity_extent[3])
    tiles_to_tiff(
        TILE_SRC,
        ZOOM,
        Bounds(
            latmin=latmin,
            latmax=latmax,
            lonmin=lonmin,
            lonmax=lonmax,
        ),
    )


if __name__ == "__main__":
    execute()
