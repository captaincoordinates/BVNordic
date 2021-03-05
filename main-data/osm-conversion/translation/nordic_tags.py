"""
Translations for Nordic Centre trails.
Dog-friendly trails are treated as one-way. These trails are only one-way for dogs but the OSM tags do not appear to support this nuance.
"""


def filterTags(attrs):
    if not attrs:
        return
    piste_prefix = "piste:"
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
        f"dog": {0: "no", 1: "yes"}[int(attrs.get("dog_friend", 0))],
        f"lit": {0: "no", 1: "yes"}[int(attrs.get("lights", 0))],
        f"{piste_prefix}grooming": "classic;skating",
    }
