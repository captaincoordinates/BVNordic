from argparse import ArgumentParser
from logging import getLogger
from typing import Final  # type: ignore

from cicd.upload.service import create_service
from cicd.upload.settings import MIME_FOLDER, ROOT_FOLDER_NAME

LOGGER: Final = getLogger(__file__)


def clean_all(service, include_root: bool, test_only: bool):
    if test_only:
        search = service.files().list(
            q=f"name contains 'test-*' and mimeType='{MIME_FOLDER}'", fields="*"
        )
    else:
        search = service.files().list(fields="*")
    for item in search.execute().get("files", []):
        id, name = item["id"], item["name"]
        if include_root or name != ROOT_FOLDER_NAME:
            LOGGER.info(f"deleting {name} ({id})")
            try:
                service.files().delete(fields="*", fileId=id).execute()
            except Exception as e:
                LOGGER.warning(f"unable to delete: {e}")
        else:
            LOGGER.info(f"skipping {name} ({id})")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--include_root",
        dest="include_root",
        action="store_true",
        help="Delete root directory",
    )
    parser.add_argument(
        "--test_only",
        dest="test_only",
        action="store_true",
        help="Only delete test- prefix directories",
    )
    parser.set_defaults(include_root=False)
    parser.set_defaults(test_only=False)
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    clean_all(create_service(), args["include_root"], args["test_only"])
