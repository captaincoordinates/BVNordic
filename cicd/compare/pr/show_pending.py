import re
from argparse import ArgumentParser
from logging import getLogger
from typing import Final  # type: ignore

from cicd.compare.pr.settings import AUTO_CONTENT_REGEX
from cicd.compare.pr.templates.templates import get_rendered_html
from cicd.compare.pr.util import get_pr, get_pr_id_from_ref, update_pr

LOGGER: Final = getLogger(__file__)


def show_pending(repo: str, pr_id: int) -> None:
    pr = get_pr(repo, pr_id)
    pr_new = pr["body"] or ""
    if re.search(AUTO_CONTENT_REGEX, pr_new):
        pr_new = re.sub(AUTO_CONTENT_REGEX, "", pr_new)
    rendered = "".join(
        [line.strip() for line in get_rendered_html("pending").splitlines()]
    )
    update_pr(repo, pr_id, f"{pr_new}{rendered}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("repo", type=str, help="owner/repo")
    parser.add_argument(
        "pr_ref", type=str, help="GitHub Ref of the PR initiating this execution"
    )
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    pr_id = get_pr_id_from_ref(args["pr_ref"])
    show_pending(args["repo"], pr_id)
