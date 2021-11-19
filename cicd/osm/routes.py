from argparse import ArgumentParser
from collections import defaultdict
from logging import getLogger
from typing import Any, Dict, Final, List  # type: ignore

from bs4 import BeautifulSoup

LOGGER: Final = getLogger(__file__)

INITIAL_RELATION_ID: Final = -1
RELATION_ID_INCREMENT: Final = -1
BVNORDIC_PREFIX: Final = "bvnordic:"


def get_trail_name_from_way(way: Any) -> str:
    return way.find("tag", {"k": f"{BVNORDIC_PREFIX}trail_name"})["v"]


def execute(in_path: str, out_path: str) -> None:  # noqa: C901
    with open(in_path, "r") as osm_file:
        content = "".join(osm_file.readlines())

    bs = BeautifulSoup(content, "xml")
    root_node = bs.find("osm")
    trail_members: Dict[str, List[int]] = defaultdict(list)
    trail_properties: Dict[str, Dict] = defaultdict(dict)
    bad_ways = []
    for way in root_node.find_all("way"):
        trail_name = get_trail_name_from_way(way)
        if len(way.findAll("nd")) < 2:
            bad_ways.append(way)
            continue
        if len(trail_name) > 0:
            if way.find("tag", {"k": f"{BVNORDIC_PREFIX}closed", "v": "yes"}) is None:
                trail_members[trail_name].append(way["id"])
                for tag in [tag for tag in way.find_all("tag") if tag["k"] != "name"]:
                    trail_properties[trail_name][tag["k"]] = tag["v"]

    LOGGER.info(f"found {len(bad_ways)} way(s) with < 2 nodes")
    for bad_way in bad_ways:
        LOGGER.info(f"deleting member of {get_trail_name_from_way(way)}")
        bad_way.decompose()

    current_relation_id = INITIAL_RELATION_ID
    for trail_name, ways in trail_members.items():
        relation = bs.new_tag("relation", id=current_relation_id, visible="true")
        for way in ways:
            relation.append(bs.new_tag("member", type="way", ref=way))
        for key, value in trail_properties[trail_name].items():
            if key == f"{BVNORDIC_PREFIX}trail_name":
                relation.append(bs.new_tag("tag", k="name", v=value))
            else:
                relation.append(bs.new_tag("tag", k=key, v=value))
        relation.append(bs.new_tag("tag", k="route", v="piste"))
        relation.append(bs.new_tag("tag", k="type", v="route"))
        root_node.append(relation)
        current_relation_id = current_relation_id + RELATION_ID_INCREMENT

    with open(out_path, "w") as osm_file:
        osm_file.write(bs.prettify())


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "in_path", type=str, help="Path to the input OSM file with only nodes and ways"
    )
    parser.add_argument(
        "out_path",
        type=str,
        help="Path to the output OSM file with added relations",
    )
    args = vars(parser.parse_args())
    LOGGER.info(f"{__name__} called with {args}")
    execute(args["in_path"], args["out_path"])
