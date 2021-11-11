from argparse import ArgumentParser
from collections import defaultdict
from logging import getLogger
from typing import Dict, Final, List  # type: ignore

from bs4 import BeautifulSoup

LOGGER: Final = getLogger(__file__)

INITIAL_RELATION_ID: Final = -1
RELATION_ID_INCREMENT: Final = -1


def execute(in_path: str, out_path: str) -> None:
    with open(in_path, "r") as osm_file:
        content = "".join(osm_file.readlines())

    bs = BeautifulSoup(content, "xml")
    root_node = bs.find("osm")
    way_members: Dict[str, List[int]] = defaultdict(list)
    way_properties: Dict[str, Dict] = defaultdict(dict)
    for way in root_node.find_all("way"):
        way_id = way.find("tag", {"k": "name"})["v"]
        way_members[way_id].append(way["id"])
        for tag in way.find_all("tag"):
            way_properties[way_id][tag["k"]] = tag["v"]

    current_relation_id = INITIAL_RELATION_ID
    for route_name, ways in way_members.items():
        relation = bs.new_tag("relation", id=current_relation_id)
        for way in ways:
            relation.append(bs.new_tag("member", type="way", ref=way))
        for key, value in way_properties[route_name].items():
            relation.append(bs.new_tag("tag", k=key, v=value))
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
