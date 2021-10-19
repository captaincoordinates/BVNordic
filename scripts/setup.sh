#!/bin/bash

pip install -r requirements-dev.txt
pip install -r upload/requirements.txt
pre-commit install