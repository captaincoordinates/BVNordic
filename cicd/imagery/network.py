from os import environ, path
from typing import Final  # type: ignore

from osgeo import ogr

from cicd.imagery.bounds import Bounds
from cicd.imagery.settings import EPSG_3857
from cicd.imagery.tiles_to_tiff import execute as tiles_to_tiff

TILE_SRC: Final = environ.get(
    "NETWORK_TILE_SRC",
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
)
ZOOM: Final = environ.get("NETWORK_TILE_ZOOM", 14)


def execute() -> None:
    gpkg_driver = ogr.GetDriverByName("GPKG")
    data_source = gpkg_driver.Open(
        path.abspath(path.join(path.dirname(__file__), "..", "..", "main-data.gpkg"))
    )
    bounds_layer = data_source.ExecuteSQL(
        "SELECT ST_Envelope(ST_Transform(ST_Buffer(ST_Envelope(ST_Union(geom)), 100), 4326)) FROM Trails"
    )
    lonmin, lonmax, latmin, latmax = bounds_layer.GetExtent()
    tiles_to_tiff(
        TILE_SRC,
        ZOOM,
        Bounds(
            latmin=latmin,
            latmax=latmax,
            lonmin=lonmin,
            lonmax=lonmax,
        ),
        "network",
        EPSG_3857,
    )


if __name__ == "__main__":
    execute()
