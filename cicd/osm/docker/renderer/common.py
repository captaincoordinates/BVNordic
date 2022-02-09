from typing import Final, List  # type: ignore

from cicd.osm.docker.renderer.render_candidate import RenderCandidate

TILE_PIXELS: Final = 256
MERCATOR_AXIS_MAX: Final = 20037508.3427892
MERCATOR_AXIS_RANGE: Final = MERCATOR_AXIS_MAX * 2
ZOOM_TO_TILE_COUNT_ONE_AXIS: Final = [pow(2, x) for x in range(21)]


def image_dims_for_rect(rect_3857: List[List[float]]) -> List[RenderCandidate]:
    x_range = rect_3857[1][0] - rect_3857[0][0]
    y_range = rect_3857[2][1] - rect_3857[0][1]
    return [
        RenderCandidate(
            zoom_level=i,
            x=round(TILE_PIXELS * x_range / (MERCATOR_AXIS_RANGE / count)),
            y=round(TILE_PIXELS * y_range / (MERCATOR_AXIS_RANGE / count)),
        )
        for i, count in enumerate(ZOOM_TO_TILE_COUNT_ONE_AXIS)
    ]
