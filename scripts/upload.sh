#!/bin/bash

pushd $(dirname $0)/..

docker build -t uploader upload
docker run --rm -v $PWD/upload/src:/upload -v $PWD/output/build:/files -e GDRIVE_UPLOAD_SERVICE_ACCT_INFO uploader python -m upload.upload $UPLOAD_FOLDER_NAME /files update_latest='${$1:-""}'
