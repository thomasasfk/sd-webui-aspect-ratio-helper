import pytest

from scripts.util import _MIN_DIMENSION
from scripts.util import _MAX_DIMENSION
from scripts.util import _scale_by_percentage
from scripts.util import _scale_dimensions_to_max_dimension


@pytest.mark.parametrize(
    "width, height, pct, expected",
    [
        pytest.param(200, 400, 0.5, (100, 200), id="50_percent_scale_down"),
        pytest.param(100, 200, 2.0, (200, 400), id="200_percent_scale_up"),
        pytest.param(100, 200, 1.1, (110, 220), id="10_percent_scale_up"),
        pytest.param(100, 200, 0.9, (90, 180), id="10_percent_scale_down"),
        pytest.param(100, 200, 0.0, (64, 128), id="scale_full_down"),
        pytest.param(
            _MIN_DIMENSION - 1,
            _MIN_DIMENSION - 1,
            0.5,
            (_MIN_DIMENSION, _MIN_DIMENSION),
            id="scale_below_min_dimension",
        ),
        pytest.param(
            _MAX_DIMENSION + 1,
            _MAX_DIMENSION + 1,
            2.0,
            (_MAX_DIMENSION, _MAX_DIMENSION),
            id="scale_above_max_dimension",
        ),
    ],
)
def test_scale_by_percentage(
        width, height, pct, expected
):
    assert _scale_by_percentage(
        width, height, pct
    ) == expected


@pytest.mark.parametrize(
    "width, height, max_dim, expected",
    [
        pytest.param(
            100, 200, 400, (200, 400), id="scale_up_to_max_dimension_horizontally"
        ),
        pytest.param(
            200, 100, 400, (400, 200), id="scale_up_to_max_dimension_vertically"
        ),
        pytest.param(
            400, 64, 400, (400, 64), id="no_scale_up_needed_with_max_dimension_width"
        ),
        pytest.param(
            64, 400, 400, (64, 400), id="no_scale_up_needed_with_max_dimension_height"
        ),
    ],
)
def test_scale_dimensions_to_max_dimension(
        width, height, max_dim, expected
):
    assert _scale_dimensions_to_max_dimension(
        width, height, max_dim
    ) == expected


@pytest.mark.parametrize(
    "width, height, max_dim",
    [
        pytest.param(
            64,
            64,
            _MIN_DIMENSION - 1,
            id="scale_below_min_dimension",
        ),
        pytest.param(
            64,
            64,
            _MAX_DIMENSION + 1,
            id="scale_above_max_dimension",
        ),

    ],
)
def test_error_thrown_given_dim_outside_boundaries(width, height, max_dim):
    with pytest.raises(ValueError):
        _scale_dimensions_to_max_dimension(width, height, max_dim)
