import random
from argparse import ArgumentParser
from http import HTTPStatus
from json import loads
from logging import getLogger
from os import path
from typing import Final, List  # type: ignore

import requests
from bs4 import BeautifulSoup

from cicd.compare.pr.settings import GITHUB_WEB_BASE
from cicd.compare.pr.templates.templates import get_rendered_html
from cicd.compare.pr.util import get_pr_id_from_ref, update_pr

LOGGER: Final = getLogger(__file__)
MAX_IMG_DOWNLOAD_ATTEMPTS: Final = 5


def show_changes(repo: str, pr_id: int, changes_file: str, uploads_file: str) -> None:
    with open(changes_file, "r") as cfile:
        changes = loads("".join(cfile.readlines()))

    with open(uploads_file, "r") as ufile:
        uploads = {
            path.splitext(local_path)[0]: file_id
            for local_path, file_id in loads("".join(ufile.readlines())).items()
        }

    change_file_ids = {
        layout: uploads[layout] if layout in uploads else None
        for layout in [item for sublist in changes.values() for item in sublist]
    }
    template_data = {
        change_type: [
            {"layout": layout, "file_id": change_file_ids[layout]} for layout in layouts
        ]
        for change_type, layouts in changes.items()
    }
    update_pr(repo, pr_id, get_rendered_html("changes", template_data))
    cache_images(repo, pr_id)


def cache_images(repo: str, pr_id: int) -> None:
    response = requests.get(f"{GITHUB_WEB_BASE}/{repo}/pull/{pr_id}")
    if response.status_code == HTTPStatus.OK:
        response_content = str(response.content)
        soup = BeautifulSoup(response_content, "html.parser")
        img_links = [
            element["src"]
            for element in soup.find_all(
                lambda element: element.name == "img"
                and "data-canonical-src" in element.attrs
            )
        ]
        get_images(img_links)
    else:
        LOGGER.error(
            f"unable to retrieve HTML for {repo} PR {pr_id}. {response.status_code}: {response.text}"
        )


def get_images(urls: List[str], attempt: int = 1):
    retry = []
    LOGGER.info(
        f"image attempt {attempt} of {MAX_IMG_DOWNLOAD_ATTEMPTS} with {len(urls)} URL/s"
    )
    if attempt <= MAX_IMG_DOWNLOAD_ATTEMPTS:
        for url in urls:
            response = requests.get(url, headers={"User-Agent": get_random_user_agent()})
            if response.status_code != HTTPStatus.OK:
                LOGGER.info(
                    f"unable to retrieve image on attempt {attempt} {url} ({response.status_code})"
                )
                retry.append(url)
        if len(retry) > 0:
            get_images(retry, attempt + 1)
        else:
            LOGGER.info("successfully retrieved all images")
    else:
        if len(urls) > 0:
            LOGGER.warning(
                f"unable to get {len(retry)} image/s after {MAX_IMG_DOWNLOAD_ATTEMPTS} attempt/s"
            )


def get_random_user_agent() -> str:
    userAgentList = (
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        # Firefox
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
    )
    return random.choice(userAgentList)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("repo", type=str, help="owner/repo")
    parser.add_argument(
        "pr_ref", type=str, help="GitHub Ref of the PR initiating this execution"
    )
    parser.add_argument(
        "changes_file", type=str, help="Path to changes.json from prior change detection"
    )
    parser.add_argument(
        "uploads_file", type=str, help="Path to uploads.json with upload report"
    )
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    pr_id = get_pr_id_from_ref(args["pr_ref"])
    show_changes(args["repo"], pr_id, args["changes_file"], args["uploads_file"])
