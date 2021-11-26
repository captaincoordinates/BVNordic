"""
Adapted from https://raw.githubusercontent.com/openstreetmap/mapnik-stylesheets/master/generate_image.py
"""

from os import environ
from typing import Final  # type: ignore

import mapnik

merc: Final = mapnik.Projection(
    "+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over"
)
longlat: Final = mapnik.Projection("+init=epsg:4326")
mapfile: Final = environ["MAPNIK_MAP_FILE"]

map_uri = "image.png"

bounds = (-127.2846, 54.7073, -127.1499, 54.7542)

z = 10
imgx = 500 * z
imgy = 1000 * z

m = mapnik.Map(imgx, imgy)
mapnik.load_map(m, mapfile)

# ensure the target map projection is mercator
m.srs = merc.params()

if hasattr(mapnik, "Box2d"):
    bbox = mapnik.Box2d(*bounds)
else:
    bbox = mapnik.Envelope(*bounds)

transform = mapnik.ProjTransform(longlat, merc)
merc_bbox = transform.forward(bbox)

# Mapnik internally will fix the aspect ratio of the bounding box
# to match the aspect ratio of the target image width and height
# This behavior is controlled by setting the `m.aspect_fix_mode`
# and defaults to GROW_BBOX, but you can also change it to alter
# the target image size by setting aspect_fix_mode to GROW_CANVAS
# m.aspect_fix_mode = mapnik.GROW_CANVAS
# Note: aspect_fix_mode is only available in Mapnik >= 0.6.0
m.zoom_to_box(merc_bbox)

# render the map to an image
im = mapnik.Image(imgx, imgy)
mapnik.render(m, im)
im.save(map_uri, "png")

print(f"output image to {map_uri}")

# Note: instead of creating an image, rendering to it, and then
# saving, we can also do this in one step like:
# mapnik.render_to_file(m, map_uri,'png')
