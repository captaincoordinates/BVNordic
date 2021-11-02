import re
from argparse import ArgumentParser
from collections import defaultdict
from json import dumps
from logging import getLogger
from multiprocessing import Pool
from os import path, remove, walk
from pathlib import Path
from shutil import copyfile
from typing import Dict, Final, List, Tuple  # type: ignore

import cv2
import imageio
from skimage.metrics import structural_similarity

from cicd.compare.change_type import ChangeType
from cicd.compare.image_type import ImageType
from cicd.util import get_process_pool_count

LOGGER: Final = getLogger(__file__)
IMAGE_EXT: Final = ".png"


def add_dir_to_pairs(
    pairs: Dict[str, List[ImageType]], dir_path: str, image_type: ImageType
) -> None:
    for root, _, files in walk(dir_path):
        for file in files:
            if file.endswith(IMAGE_EXT):
                local_path = path.join(
                    root.replace(dir_path, ""), file.replace(IMAGE_EXT, "")
                )
                pairs[re.sub("^/", "", local_path)].append(image_type)


def execute(before_dir: str, after_dir: str, compare_base: str) -> None:
    result_dir = path.join(compare_base, "result")
    Path(result_dir).mkdir(parents=True, exist_ok=True)
    before_path = path.join(compare_base, before_dir)
    after_path = path.join(compare_base, after_dir)
    image_pairs: Dict[str, List[ImageType]] = defaultdict(list)
    add_dir_to_pairs(image_pairs, before_path, ImageType.BEFORE)
    add_dir_to_pairs(image_pairs, after_path, ImageType.AFTER)

    remained = [
        file_path
        for file_path, types in image_pairs.items()
        if ImageType.BEFORE in types and ImageType.AFTER in types
    ]
    added = [path for path, types in image_pairs.items() if ImageType.BEFORE not in types]
    removed = [
        path for path, types in image_pairs.items() if ImageType.AFTER not in types
    ]

    changes: Dict[ChangeType, List[str]] = {
        change_type: list() for change_type in ChangeType
    }

    for addition in added:
        changes[ChangeType.ADDED].append(addition)
        copy_to_result(after_path, addition, result_dir)

    for removal in removed:
        changes[ChangeType.REMOVED].append(removal)
        copy_to_result(before_path, removal, result_dir)

    for file_path, change_type in _change_detection_executor(
        result_dir,
        before_path,
        after_path,
        remained,
    ).parallel(get_process_pool_count()):
        changes[change_type].append(file_path)

    with open(path.join(result_dir, "changes.json"), "w") as change_json:
        change_json.write(
            dumps(
                {
                    change_type.name: file_paths
                    for change_type, file_paths in changes.items()
                }
            )
        )


def copy_to_result(source_dir: str, local_path: str, result_dir) -> None:
    local_path_parts = path.split(local_path)
    local_result_dir = path.join(result_dir, path.join(local_path_parts[0]))
    Path(local_result_dir).mkdir(parents=True, exist_ok=True)
    copyfile(
        path.join(source_dir, f"{local_path}{IMAGE_EXT}"),
        path.join(local_result_dir, f"{local_path_parts[1]}{IMAGE_EXT}"),
    )


class _change_detection_executor:
    def __init__(
        self,
        result_dir: str,
        before_dir: str,
        after_dir: str,
        local_paths: List[str],
    ):
        self.result_dir = result_dir
        self.before_dir = before_dir
        self.after_dir = after_dir
        self.local_paths = local_paths

    def __call__(self, local_path: str):
        # adapted from https://stackoverflow.com/a/56193442/519575
        before_file = path.join(self.before_dir, local_path)
        after_file = path.join(self.after_dir, local_path)
        before = cv2.imread(f"{before_file}{IMAGE_EXT}")
        after = cv2.imread(f"{after_file}{IMAGE_EXT}")
        before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)
        (score, diff) = structural_similarity(before_gray, after_gray, full=True)
        LOGGER.info(f"structural similarity for {local_path}: {score}")
        if score == 1:
            return (local_path, ChangeType.UNCHANGED)

        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = contours[0] if len(contours) == 2 else contours[1]
        for c in contours:
            area = cv2.contourArea(c)
            if area > 40:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(before, (x, y), (x + w, y + h), (0, 0, 255), 2)

        local_path_parts = path.split(local_path)
        local_result_dir = path.join(self.result_dir, path.join(local_path_parts[0]))
        Path(local_result_dir).mkdir(parents=True, exist_ok=True)
        before_result = path.join(
            local_result_dir, f"before-{local_path_parts[1]}{IMAGE_EXT}"
        )
        after_result = path.join(
            local_result_dir, f"after-{local_path_parts[1]}{IMAGE_EXT}"
        )
        gif_result = path.join(local_result_dir, f"{local_path_parts[1]}.gif")

        cv2.imwrite(before_result, before)
        cv2.imwrite(after_result, after)

        imageio.mimsave(
            gif_result,
            [imageio.imread(filename) for filename in [before_result, after_result]],
            duration=1.5,
        )

        remove(before_result)
        remove(after_result)

        return (local_path, ChangeType.CHANGED)

    def parallel(self, pool_size: int) -> List[Tuple[str, ChangeType]]:
        pool = Pool(processes=pool_size)
        outcomes = pool.map(self, self.local_paths)
        pool.close()
        return outcomes


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "before_dir", type=str, help="Name of the directory containing 'before' images"
    )
    parser.add_argument(
        "after_dir", type=str, help="Name of the directory containing 'after' images"
    )
    parser.add_argument("compare_base", type=str, help="Path to the comparison directory")
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    execute(args["before_dir"], args["after_dir"], args["compare_base"])
