#!/bin/bash

pip install -r requirements-dev.txt
pip install -r cicd/compare/requirements-pr.txt
pip install -r cicd/compare/requirements-detect.txt
pip install -r cicd/compare/requirements-changes.txt
pre-commit install