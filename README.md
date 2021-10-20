# Bulkley Valley Nordic Centre Trails Map

QGIS project file and associated data to generate various georeferenced PDFs used by the Nordic Centre.

[![Generate and Persist Outputs](https://github.com/Bulkley-Valley-Cross-Country-Ski-Club/mapping/actions/workflows/outputs.yml/badge.svg)](https://github.com/Bulkley-Valley-Cross-Country-Ski-Club/mapping/actions/workflows/outputs.yml)

## CI/CD
Pushes to the `master` branch will trigger an export of all QGIS Layouts and upload to a public-readable Google Drive account: https://drive.google.com/drive/folders/1BnA7QL0c6nEB3kifgzp8bWXU3SjuD2rf
Previous exports are named according to commit SHA. The following links will always reference the latest file versions:
- [Print PDF](https://drive.google.com/file/d/1lpf7qo3NgWYj6MZOi5FJ7fjcOuchUvxb/view?usp=sharing)
- [Digital-only PDF](https://drive.google.com/file/d/1MimiPeXI22dCuUXUkiCjco6dH6YYfH8v/view?usp=sharing)

## Development
To begin development execute `scripts/setup.sh`. *Note*: this will install several pip dependencies and should be executed within a virtual environment.
Assumes Python 3.9.7 or higher.
Pre-commit hooks execute `flake8`, `black`, and `mypy` against updated code.

## OSM Conversion
Execute `./osm-conversion/convert.sh` to convert trails data to OSM format. Generates main-data/osm-conversion/out.osm using translation logic in main-data/osm-conversion/translation/nordic_tags.py. Set RETAIN_INTERMEDIARIES=1 to retain temporary GeoJSON file generated during conversion, i.e. `RETAIN_INTERMEDIARIES=1 ./osm-conversion/convert.sh`
