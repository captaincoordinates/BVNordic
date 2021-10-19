from .util import configure_logging
from .service import create_service
from typing import Final
from .settings import ROOT_FOLDER_NAME

from logging import getLogger

LOGGER: Final = getLogger(__file__)

def clean_all(service, exclude_root: bool = True):
    for item in service.files().list(fields="*").execute().get("files", []):
        id, name = item["id"], item["name"]
        if not exclude_root or name != ROOT_FOLDER_NAME:
            LOGGER.info(f"deleting {name} ({id})")
            try:
                service.files().delete(fields="*", fileId=id).execute()
            except Exception as e:
                LOGGER.warning(f"unable to delete: {e}")
        else:
            LOGGER.info(f"skipping {name} ({id})")

if __name__ == "__main__":
    configure_logging()
    service: Final = create_service()
    clean_all(service)