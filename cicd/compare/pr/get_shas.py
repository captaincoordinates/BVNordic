from argparse import ArgumentParser
from logging import getLogger
from os import linesep, path
from typing import Final, Tuple  # type: ignore

from cicd.compare.pr.util import get_pr, get_pr_id_from_ref

LOGGER: Final = getLogger(__file__)


def get_shas(repo: str, pr_id: int) -> Tuple[str, str]:
    pr = get_pr(repo, pr_id)
    return (str(pr["base"]["sha"]), str(pr["head"]["sha"]))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("repo", type=str, help="owner/repo")
    parser.add_argument(
        "pr_ref", type=str, help="GitHub Ref of the PR initiating this execution"
    )
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    pr_id = get_pr_id_from_ref(args["pr_ref"])
    shas = get_shas(args["repo"], pr_id)

    with open(path.join(path.dirname(__file__), f"shas-{pr_id}.txt"), "w") as shas_file:
        shas_file.writelines(linesep.join(shas))
