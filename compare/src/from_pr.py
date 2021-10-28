import re
from argparse import ArgumentParser
from http import HTTPStatus
from logging import getLogger
from os import linesep, path
from typing import Final, Tuple  # type: ignore

import requests

from .util import configure_logging

LOGGER: Final = getLogger(__file__)


def get_shas(repo: str, pr_ref: str) -> Tuple[str, str]:
    pr_id = int(re.sub(r"[^\d]", "", pr_ref))
    LOGGER.info(f"PR ID: {pr_id}")
    response = requests.get(f"https://api.github.com/repos/{repo}/pulls/{pr_id}")
    if response.status_code == HTTPStatus.OK:
        data = response.json()
        return (str(data["base"]["sha"]), str(data["head"]["sha"]))
    else:
        raise Exception(
            f"PR {pr_id} is not known (HTTP {response.status_code}: {response.text})"
        )


if __name__ == "__main__":
    configure_logging()
    parser = ArgumentParser()
    parser.add_argument("repo", type=str, help="owner/repo")
    parser.add_argument(
        "pr_ref", type=str, help="GitHub Ref of the PR initiating this execution"
    )
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    shas = get_shas(args["repo"], args["pr_ref"])
    LOGGER.info(f"shas: {shas}")

    with open(path.join(path.dirname(__file__), "..", "pr_shas.txt"), "w") as shas_file:
        shas_file.writelines(linesep.join(shas))
