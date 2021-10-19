from os import environ
from typing import Final
from googleapiclient.discovery import build
from json import loads
from logging import getLogger

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


LOGGER: Final = getLogger(__file__)

def create_service():
    LOGGER.info("loading credentials")
    credentials: Final = Credentials.from_service_account_info(
        loads(
            environ["GDRIVE_UPLOAD_SERVICE_ACCT_INFO"]
        ),
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    LOGGER.info("creating service with credentials")
    return build("drive", "v3", credentials=credentials)
