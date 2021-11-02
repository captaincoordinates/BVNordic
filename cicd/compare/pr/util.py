import re
from http import HTTPStatus
from os import environ
from typing import Any, Dict

import requests

from cicd.compare.pr.settings import AUTO_CONTENT_REGEX, GITHUB_API_BASE


def get_pr_id_from_ref(pr_ref: str) -> int:
    return int(re.sub(r"[^\d]", "", pr_ref))


def get_pr(repo: str, pr_id: int) -> Dict[str, Any]:
    response = requests.get(f"{GITHUB_API_BASE}/repos/{repo}/pulls/{pr_id}")
    if response.status_code == HTTPStatus.OK:
        return response.json()
    else:
        raise Exception(
            f"PR {pr_id} is not known (HTTP {response.status_code}: {response.text})"
        )


def update_pr(repo: str, pr_id: int, new_content: str) -> None:
    pr = get_pr(repo, pr_id)
    pr_new = pr["body"] or ""
    if re.search(AUTO_CONTENT_REGEX, pr_new):
        pr_new = re.sub(AUTO_CONTENT_REGEX, "", pr_new)
    rendered = "".join([line.strip() for line in new_content.splitlines()])
    response = requests.patch(
        f"{GITHUB_API_BASE}/repos/{repo}/pulls/{pr_id}",
        json={"body": f"{pr_new}{rendered}"},
        headers={"Authorization": f"Bearer {environ['PAT_GITHUB_API']}"},
    )
    if response.status_code != HTTPStatus.OK:
        raise Exception(
            f"Received unexpected response when updating PR: {response.status_code}, {response.text}"
        )
