from argparse import ArgumentParser
from json import loads
from logging import getLogger
from typing import Final  # type: ignore

from cicd.compare.pr.templates.templates import get_rendered_html
from cicd.compare.pr.util import get_pr_id_from_ref, update_pr

LOGGER: Final = getLogger(__file__)
FILE_EXT: Final = ".gif"


def show_changes(repo: str, pr_id: int, changes_file: str, uploads_file: str) -> None:
    with open(changes_file, "r") as cfile:
        changes = loads("".join(cfile.readlines()))

    with open(uploads_file, "r") as ufile:
        uploads = loads("".join(ufile.readlines()))

    change_file_ids = {
        layout: uploads[f"{layout}{FILE_EXT}"]
        if f"{layout}{FILE_EXT}" in uploads
        else None
        for layout in [item for sublist in changes.values() for item in sublist]
    }
    template_data = {
        change_type: [
            {"layout": layout, "file_id": change_file_ids[layout]} for layout in layouts
        ]
        for change_type, layouts in changes.items()
    }
    update_pr(repo, pr_id, get_rendered_html("changes", template_data))


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
