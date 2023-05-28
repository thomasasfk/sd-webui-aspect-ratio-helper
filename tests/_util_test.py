from __future__ import annotations

import pytest

import aspect_ratio_helper._constants as _constants
import aspect_ratio_helper._util as _util


@pytest.mark.parametrize(
    'num, expected',
    [
        (50, 'x0.5'),
        (150, 'x1.5'),
        (175, 'x1.75'),
        (250, 'x2.5'),
    ],
)
def test_display_multiplication(num, expected):
    assert _util.display_multiplication(num) == expected


@pytest.mark.parametrize(
    'num, expected',
    [
        (50, '50%'),
        (75, '75%'),
        (100, '100%'),
        (150, '150%'),
        (250, '250%'),
    ],
)
def test_display_raw_percentage(num, expected):
    assert _util.display_raw_percentage(num) == expected


@pytest.mark.parametrize(
    'num, expected_output', [
        (150, '+50%'),
        (100, '0%'),
        (50, '-50%'),
        (0, '-100%'),
        (200, '+100%'),
        (75, '-25%'),
    ],
)
def test_display_minus_and_plus(num, expected_output):
    assert _util.display_minus_and_plus(num) == expected_output


@pytest.mark.parametrize(
    'width, height, pct, expected',
    [
        pytest.param(200, 400, 0.5, (100, 200), id='50_percent_scale_down'),
        pytest.param(100, 200, 2.0, (200, 400), id='200_percent_scale_up'),
        pytest.param(100, 200, 1.1, (110, 220), id='10_percent_scale_up'),
        pytest.param(100, 200, 0.9, (90, 180), id='10_percent_scale_down'),
        pytest.param(100, 200, 0.0, (64, 128), id='scale_full_down'),
        pytest.param(
            _constants.MIN_DIMENSION - 1,
            _constants.MIN_DIMENSION - 1,
            0.5,
            (_constants.MIN_DIMENSION, _constants.MIN_DIMENSION),
            id='scale_belowMIN_DIMENSION',
        ),
        pytest.param(
            _constants.MAX_DIMENSION + 1,
            _constants.MAX_DIMENSION + 1,
            2.0,
            (_constants.MAX_DIMENSION, _constants.MAX_DIMENSION),
            id='scale_aboveMAX_DIMENSION',
        ),
    ],
)
def test_scale_by_percentage(
        width, height, pct, expected,
):
    assert _util.scale_by_percentage(
        width, height, pct,
    ) == expected


@pytest.mark.parametrize(
    'width, height, max_dim, expected',
    [
        pytest.param(
            100, 200, 400, (200, 400),
            id='scale_up_toMAX_DIMENSION_horizontally',
        ),
        pytest.param(
            200, 100, 400, (400, 200),
            id='scale_up_toMAX_DIMENSION_vertically',
        ),
        pytest.param(
            400, 64, 400, (400, 64),
            id='no_scale_up_needed_withMAX_DIMENSION_width',
        ),
        pytest.param(
            64, 400, 400, (64, 400),
            id='no_scale_up_needed_withMAX_DIMENSION_height',
        ),
        pytest.param(
            _constants.MIN_DIMENSION,
            _constants.MIN_DIMENSION,
            _constants.MAX_DIMENSION,
            (_constants.MAX_DIMENSION, _constants.MAX_DIMENSION),
            id='scale_from_min_to_max',
        ),
        pytest.param(
            _constants.MAX_DIMENSION,
            _constants.MAX_DIMENSION,
            _constants.MIN_DIMENSION,
            (_constants.MIN_DIMENSION, _constants.MIN_DIMENSION),
            id='scale_from_max_to_min',
        ),
        pytest.param(
            _constants.MIN_DIMENSION, 32, _constants.MIN_DIMENSION,
            (128, _constants.MIN_DIMENSION),
            id='scale_below_min_height_dimension_clamps_retains_ar',
        ),
        pytest.param(
            32, _constants.MIN_DIMENSION, _constants.MIN_DIMENSION,
            (_constants.MIN_DIMENSION, 128),
            id='scale_below_min_width_dimension_clamps_retains_ar',
        ),
        pytest.param(
            _constants.MAX_DIMENSION, 4096, _constants.MAX_DIMENSION,
            (1024, _constants.MAX_DIMENSION),
            id='scale_above_max_height_dimension_clamps_retains_ar',
        ),
        pytest.param(
            4096, _constants.MAX_DIMENSION, _constants.MAX_DIMENSION,
            (_constants.MAX_DIMENSION, 1024),
            id='scale_above_max_width_dimension_clamps_retains_ar',
        ),
        pytest.param(
            64, 64, _constants.MIN_DIMENSION - 1,
            (_constants.MIN_DIMENSION, _constants.MIN_DIMENSION),
            id='scale_dimension_belowMIN_DIMENSION_clamps_retains_ar',
        ),
        pytest.param(
            64, 64, _constants.MAX_DIMENSION + 1,
            (_constants.MAX_DIMENSION, _constants.MAX_DIMENSION),
            id='scale_dimension_aboveMAX_DIMENSION_clamps_retains_ar',
        ),
    ],
)
def test_scale_dimensions_to_max_dim(
        width, height, max_dim, expected,
):
    assert _util.scale_dimensions_to_max_dim(
        width, height, max_dim,
    ) == expected


class SharedOpts:
    def __init__(self, options=None, defaults=None):
        self.options = options or {}
        self.defaults = defaults or {}

    def __getattr__(self, key):
        try:
            return self.options[key]
        except KeyError:
            raise AttributeError()

    def get_default(self, key):
        return self.defaults.get(key, None)


def test_safe_opt_util():
    shared_opts = SharedOpts(options={'key': 'value'})
    assert _util.safe_opt_util(shared_opts, 'key', {}) == 'value'


def test_safe_opt_util_none():
    shared_opts = SharedOpts(options={'key': None}, defaults={'key': 'value'})
    assert _util.safe_opt_util(shared_opts, 'key', {}) == 'value'


def testsafe_opt_util_default_a():
    shared_opts = SharedOpts(
        defaults={'key': 'default_a'},
    )
    assert _util.safe_opt_util(
        shared_opts, 'key', {'key': 'default_b'},
    ) == 'default_a'


def test_safe_opt_util_default_b():
    shared_opts = SharedOpts(defaults={'key': None})
    assert _util.safe_opt_util(
        shared_opts, 'key', {'key': 'default_b'},
    ) == 'default_b'


@pytest.mark.parametrize(
    'options', ({'key': None}, {}),
)
def test_safe_opt_safe_return_no_defaults_b(options):
    shared_opts = SharedOpts(options=options)
    assert _util.safe_opt_util(shared_opts, 'unknown_key', {}) is None
