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
        pytest.param(200, 400, 0.5, (96, 200), id='50_percent_scale_down'),
        pytest.param(100, 200, 2.0, (200, 400), id='200_percent_scale_up'),
        pytest.param(100, 200, 1.1, (112, 224), id='10_percent_scale_up'),
        pytest.param(100, 200, 0.9, (88, 176), id='10_percent_scale_down'),
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
        # pytest.param(
        #     100, 200, 400, (200, 400),
        #     id='scale_up_to_max_dimension_horizontally',
        # ),
        # pytest.param(
        #     200, 100, 400, (400, 200),
        #     id='scale_up_to_max_dimension_vertically',
        # ),
        # pytest.param(
        #     400, 64, 400, (400, 64),
        #     id='no_scale_up_needed_with_max_dimension_width',
        # ),
        # pytest.param(
        #     64, 400, 400, (64, 400),
        #     id='no_scale_up_needed_with_max_dimension_height',
        # ),
        # pytest.param(
        #     _constants.MIN_DIMENSION,
        #     _constants.MIN_DIMENSION,
        #     _constants.MAX_DIMENSION,
        #     (_constants.MAX_DIMENSION, _constants.MAX_DIMENSION),
        #     id='scale_from_min_to_max',
        # ),
        # pytest.param(
        #     _constants.MAX_DIMENSION,
        #     _constants.MAX_DIMENSION,
        #     _constants.MIN_DIMENSION,
        #     (_constants.MIN_DIMENSION, _constants.MIN_DIMENSION),
        #     id='scale_from_max_to_min',
        # ),
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
        # pytest.param(
        #     _constants.MAX_DIMENSION, 4096, _constants.MAX_DIMENSION,
        #     (1024, _constants.MAX_DIMENSION),
        #     id='scale_above_max_height_dimension_clamps_retains_ar',
        # ),
        # pytest.param(
        #     4096, _constants.MAX_DIMENSION, _constants.MAX_DIMENSION,
        #     (_constants.MAX_DIMENSION, 1024),
        #     id='scale_above_max_width_dimension_clamps_retains_ar',
        # ),
        # pytest.param(
        #     64, 64, _constants.MIN_DIMENSION - 1,
        #     (_constants.MIN_DIMENSION, _constants.MIN_DIMENSION),
        #     id='scale_dimension_below_min_dimension_clamps_retains_ar',
        # ),
        # pytest.param(
        #     64, 64, _constants.MAX_DIMENSION + 1,
        #     (_constants.MAX_DIMENSION, _constants.MAX_DIMENSION),
        #     id='scale_dimension_above_max_dimension_clamps_retains_ar',
        # ),
    ],
)
def test_scale_dimensions_to_max_dim(
        width, height, max_dim, expected,
):
    assert _util.scale_dimensions_to_max_dim(
        width, height, max_dim,
    ) == expected


@pytest.mark.parametrize(
    'width, height, min_dim, expected',
    [
        pytest.param(
            100, 200, 400, (400, 800),
            id='scale_up_to_min_dimension_with_ar_preservation',
        ),
        pytest.param(
            200, 100, 400, (800, 400),
            id='scale_up_to_min_dimension_with_ar_preservation',
        ),
        pytest.param(
            100, 100, 400, (400, 400),
            id='no_scale_up_needed_with_min_dimension',
        ),
        pytest.param(
            _constants.MIN_DIMENSION, _constants.MIN_DIMENSION, _constants.MAX_DIMENSION,
            (_constants.MAX_DIMENSION, _constants.MAX_DIMENSION),
            id='scale_up_to_max_dimension_with_ar_preservation',
        ),
        pytest.param(
            _constants.MAX_DIMENSION, _constants.MAX_DIMENSION, _constants.MIN_DIMENSION,
            (_constants.MIN_DIMENSION, _constants.MIN_DIMENSION),
            id='scale_down_to_min_dimension_with_ar_preservation',
        ),
        pytest.param(
            100, 100, _constants.MAX_DIMENSION,
            (_constants.MAX_DIMENSION, _constants.MAX_DIMENSION),
            id='scale_up_to_max_dimension_with_ar_preservation',
        ),
    ],
)
def test_scale_dimensions_to_min_dim(
        width, height, min_dim, expected,
):
    assert _util.scale_dimensions_to_min_dim(
        width, height, min_dim,
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


@pytest.mark.parametrize(
    'value, expected', [
        (0, 0),
        (7, 8),
        (10, 8),
        (16, 16),
        (23, 24),
        (32, 32),
        (33, 32),
        (100, 96),
        (10.5, 8),
        (15.3, 16),
        (21.8, 24),
        (33.9, 32),
        (98.7, 96),
    ],
)
def test_round_to_multiple_of_8(value, expected):
    assert _util.round_to_multiple_of_8(value) == expected


@pytest.mark.parametrize(
    'width, height, aspect_ratio, expected', [
        (100, 100, 1.0, (96, 96)),
        (3000, 2000, 1.5, (2048, 1368)),
        (500, 8000, 0.5, (1024, 2048)),
        (500, 300, 2.0, (496, 304)),
        (100, 200, 0.5, (96, 200)),
        (500, 500, 1.2, (496, 496)),
        (2048, 2048, 1.0, (2048, 2048)),
        (2049, 2048, 1.0, (2048, 2048)),
        (2048, 2049, 1.0, (2048, 2048)),
        (2049, 2049, 1.0, (2048, 2048)),
        (63, 63, 1.0, (64, 64)),
        (2050, 2050, 1.0, (2048, 2048)),
        (63, 64, 1.0, (64, 64)),
        (64, 63, 1.0, (64, 64)),
        (64, 64, 1.0, (64, 64)),
        (63, 63, 1.0, (64, 64)),
        (2050, 63, 1.0, (2048, 2048)),
        (63, 2050, 1.0, (2048, 2048)),
        (2050, 2050, 0.01, (64, 2048)),
        (100.5, 100.5, 1.0, (104, 104)),
        (200.3, 100.7, 0.5, (200, 104)),
    ],
)
def test_clamp_to_boundaries(width, height, aspect_ratio, expected):
    assert _util.clamp_to_boundaries(width, height, aspect_ratio) == expected
