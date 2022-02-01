from dataclasses import dataclass


@dataclass
class RenderCandidate:
    zoom_level: int
    x: int
    y: int
