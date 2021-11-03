from argparse import ArgumentParser
from logging import getLogger
from typing import Final  # type: ignore

from cicd.compare.pr.util import get_pr, get_pr_id_from_ref

LOGGER: Final = getLogger(__file__)


def check(repo: str, pr_id: int) -> None:
    pr = get_pr(repo, pr_id)
    head_repo = pr["head"]["repo"]["full_name"]
    base_repo = pr["base"]["repo"]["full_name"]

    if head_repo == base_repo:
        exit(0)
    else:
        LOGGER.warning(
            f"PR across forks not compatible with visual diff, exiting early. Workflow cannot access GitHub Secrets due to security constraints. For a visual diff merge the remote branch to a local branch, and then create a PR from the local branch. Head repo: {head_repo}, base repo: {base_repo}"
        )
        exit(1)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("repo", type=str, help="owner/repo")
    parser.add_argument(
        "pr_ref", type=str, help="GitHub Ref of the PR initiating this execution"
    )
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    pr_id = get_pr_id_from_ref(args["pr_ref"])
    check(args["repo"], pr_id)
