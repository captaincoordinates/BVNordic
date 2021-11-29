from dataclasses import dataclass


@dataclass
class Bounds:
    lonmin: float
    lonmax: float
    latmin: float
    latmax: float
