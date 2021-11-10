# Bulkley Valley Nordic Centre Trails Map

QGIS project file and associated data to generate various georeferenced PDFs used by the Nordic Centre.

[![Generate and Persist Outputs](https://github.com/Bulkley-Valley-Cross-Country-Ski-Club/mapping/actions/workflows/outputs.yml/badge.svg?branch=master)](https://github.com/Bulkley-Valley-Cross-Country-Ski-Club/mapping/actions/workflows/outputs.yml)

## CI/CD
Pushes to the `master` branch will trigger an export of all QGIS Layouts and upload to a public-readable Google Drive account.

https://drive.google.com/drive/folders/1BnA7QL0c6nEB3kifgzp8bWXU3SjuD2rf

Previous exports are named according to commit SHA. The following links will always reference the latest file versions:
- [Print PDF](https://drive.google.com/file/d/1lpf7qo3NgWYj6MZOi5FJ7fjcOuchUvxb/view?usp=sharing)
- [Print Thumbnail](https://drive.google.com/file/d/17QCZHo1_aAu5rAIrHlpFTzOyBx82mWuq/view?usp=sharing)
- [Digital-only PDF](https://drive.google.com/file/d/1MimiPeXI22dCuUXUkiCjco6dH6YYfH8v/view?usp=sharing)

## Map Data Edits
Map data edits should be managed via [issues](https://github.com/Bulkley-Valley-Cross-Country-Ski-Club/mapping/issues) and merged to the `master` branch via Pull Request.

## Development
To begin development execute `scripts/setup.sh`. *Note*: this will install several pip dependencies and should be executed within a virtual environment. Assumes Python 3.9.7 or higher.

Pre-commit hooks execute `flake8`, `black`, and `mypy` against updated code.

## Generate Outputs
### Deployment Outputs
Execute `cicd/export/scripts/test.sh` to generate all outputs locally in `output/`. Append `upload=1` to upload the local directory to Google Drive. `GDRIVE_CI_UPLOAD_SERVICE_ACCT_INFO` env var must be set to a valid JSON key for a Google Service Account.

### Visual Diff Outputs
Execute `cicd/compare/scripts/test.sh before=[[ base commit SHA (full) ]] after=[[ head commit SHA (full) ]]`. Append `upload=1` to upload the local directory to Google Drive. `GDRIVE_PR_UPLOAD_SERVICE_ACCT_INFO` env var must be set to a valid JSON key for a Google Service Account.
