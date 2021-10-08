# Bulkley Valley Nordic Centre Trails Map

QGIS project file and associated data to generate various georeferenced PDFs used by the Nordic Centre.

## OSM Conversion
Execute `./osm-conversion/convert.sh` to convert trails data to OSM format. Generates main-data/osm-conversion/out.osm using translation logic in main-data/osm-conversion/translation/nordic_tags.py. Set RETAIN_INTERMEDIARIES=1 to retain temporary GeoJSON file generated during conversion, i.e. `RETAIN_INTERMEDIARIES=1 ./osm-conversion/convert.sh`
