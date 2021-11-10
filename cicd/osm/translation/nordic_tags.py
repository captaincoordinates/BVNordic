"""
Translations for Nordic Centre trails.
Dog-friendly trails are treated as one-way. These trails are only one-way for dogs but the OSM tags do not appear to support this nuance.
"""
from os import environ


def filterTags(attrs):
    if not attrs:
        return
    piste_prefix = "piste:"
    bvnordic_prefix = "bvnordic:"
    return {
        "name": attrs.get("name", ""),
        f"{piste_prefix}type": "nordic",
        f"{piste_prefix}difficulty": [
            value
            for key, value in {
                (0, 1): "easy",
                (2,): "intermediate",
                (3,): "advanced",
            }.items()
            if int(attrs.get("difficulty", 0)) in key
        ][0],
        f"{piste_prefix}oneway": {0: "no", 1: "yes"}[int(attrs.get("dog_friend", 0))],
        "dog": {0: "no", 1: "yes"}[int(attrs.get("dog_friend", 0))],
        "lit": {0: "no", 1: "yes"}[int(attrs.get("lights", 0))],
        f"{piste_prefix}grooming": "classic;skating",
        f"{bvnordic_prefix}network": "Bulkley Valley Nordic Centre",
        f"{bvnordic_prefix}readme": "Created by Bulkley Valley Nordic Centre GIS. Please contact osm@bvnordic.ca before making any changes.",
        f"{bvnordic_prefix}commit-sha": f"{environ['GITHUB_SHA']}",
    }
