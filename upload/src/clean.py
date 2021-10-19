from argparse import ArgumentParser
from logging import getLogger
from typing import Final  # type: ignore

from .service import create_service
from .settings import ROOT_FOLDER_NAME
from .util import configure_logging

LOGGER: Final = getLogger(__file__)


def clean_all(service, include_root: bool = True):
    for item in service.files().list(fields="*").execute().get("files", []):
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
    configure_logging()
    parser = ArgumentParser()
    parser.add_argument(
        "--include_root",
        dest="include_root",
        action="store_true",
        help="Delete root directory",
    )
    parser.set_defaults(include_root=False)
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    clean_all(create_service(), args["include_root"])
