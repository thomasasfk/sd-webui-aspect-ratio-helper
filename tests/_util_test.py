import pytest

from aspect_ratio_helper._util import _display_minus_and_plus
from aspect_ratio_helper._util import _display_multiplication
from aspect_ratio_helper._util import _display_raw_percentage
from aspect_ratio_helper._util import _MAX_DIMENSION
from aspect_ratio_helper._util import _MIN_DIMENSION
from aspect_ratio_helper._util import _safe_opt_util
from aspect_ratio_helper._util import _scale_by_percentage
from aspect_ratio_helper._util import _scale_dimensions_to_max_dimension


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
    assert _display_multiplication(num) == expected


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
    assert _display_raw_percentage(num) == expected


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
    assert _display_minus_and_plus(num) == expected_output


@pytest.mark.parametrize(
    'width, height, pct, expected',
    [
        pytest.param(200, 400, 0.5, (100, 200), id='50_percent_scale_down'),
        pytest.param(100, 200, 2.0, (200, 400), id='200_percent_scale_up'),
        pytest.param(100, 200, 1.1, (110, 220), id='10_percent_scale_up'),
        pytest.param(100, 200, 0.9, (90, 180), id='10_percent_scale_down'),
        pytest.param(100, 200, 0.0, (64, 128), id='scale_full_down'),
        pytest.param(
            _MIN_DIMENSION - 1,
            _MIN_DIMENSION - 1,
            0.5,
            (_MIN_DIMENSION, _MIN_DIMENSION),
            id='scale_below_min_dimension',
        ),
        pytest.param(
            _MAX_DIMENSION + 1,
            _MAX_DIMENSION + 1,
            2.0,
            (_MAX_DIMENSION, _MAX_DIMENSION),
            id='scale_above_max_dimension',
        ),
    ],
)
def test_scale_by_percentage(
        width, height, pct, expected,
):
    assert _scale_by_percentage(
        width, height, pct,
    ) == expected


@pytest.mark.parametrize(
    'width, height, max_dim, expected',
    [
        pytest.param(
            100, 200, 400, (200, 400),
            id='scale_up_to_max_dimension_horizontally',
        ),
        pytest.param(
            200, 100, 400, (400, 200),
            id='scale_up_to_max_dimension_vertically',
        ),
        pytest.param(
            400, 64, 400, (400, 64),
            id='no_scale_up_needed_with_max_dimension_width',
        ),
        pytest.param(
            64, 400, 400, (64, 400),
            id='no_scale_up_needed_with_max_dimension_height',
        ),
        pytest.param(
            _MIN_DIMENSION, _MIN_DIMENSION, _MAX_DIMENSION,
            (_MAX_DIMENSION, _MAX_DIMENSION),
            id='scale_from_min_to_max',
        ),
        pytest.param(
            _MAX_DIMENSION, _MAX_DIMENSION, _MIN_DIMENSION,
            (_MIN_DIMENSION, _MIN_DIMENSION),
            id='scale_from_max_to_min',
        ),
        pytest.param(
            _MIN_DIMENSION, 32, _MIN_DIMENSION,
            (128, _MIN_DIMENSION),
            id='scale_below_min_height_dimension_clamps_retains_ar',
        ),
        pytest.param(
            32, _MIN_DIMENSION, _MIN_DIMENSION,
            (_MIN_DIMENSION, 128),
            id='scale_below_min_width_dimension_clamps_retains_ar',
        ),
        pytest.param(
            _MAX_DIMENSION, 4096, _MAX_DIMENSION,
            (1024, _MAX_DIMENSION),
            id='scale_above_max_height_dimension_clamps_retains_ar',
        ),
        pytest.param(
            4096, _MAX_DIMENSION, _MAX_DIMENSION,
            (_MAX_DIMENSION, 1024),
            id='scale_above_max_width_dimension_clamps_retains_ar',
        ),
        pytest.param(
            64, 64, _MIN_DIMENSION - 1,
            (_MIN_DIMENSION, _MIN_DIMENSION),
            id='scale_dimension_below_min_dimension_clamps_retains_ar',
        ),
        pytest.param(
            64, 64, _MAX_DIMENSION + 1,
            (_MAX_DIMENSION, _MAX_DIMENSION),
            id='scale_dimension_above_max_dimension_clamps_retains_ar',
        ),
    ],
)
def test_scale_dimensions_to_max_dimension(
        width, height, max_dim, expected,
):
    assert _scale_dimensions_to_max_dimension(
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
    assert _safe_opt_util(shared_opts, 'key') == 'value'


def test_safe_opt_util_none():
    shared_opts = SharedOpts(options={'key': None}, defaults={'key': 'value'})
    assert _safe_opt_util(shared_opts, 'key') == 'value'


def test_safe_opt_util_default_a(monkeypatch):
    monkeypatch.setattr(
        'aspect_ratio_helper._util._OPT_KEY_TO_DEFAULT_MAP',
        {'key': 'default_b'},
    )
    shared_opts = SharedOpts(
        defaults={'key': 'default_a'},
    )
    assert _safe_opt_util(shared_opts, 'key') == 'default_a'


def test_safe_opt_util_default_b(monkeypatch):
    monkeypatch.setattr(
        'aspect_ratio_helper._util._OPT_KEY_TO_DEFAULT_MAP',
        {'key': 'default_b'},
    )
    shared_opts = SharedOpts(defaults={'key': None})
    assert _safe_opt_util(shared_opts, 'key') == 'default_b'


@pytest.mark.parametrize(
    'options', ({'key': None}, {}),
)
def test_safe_opt_safe_return_no_defaults_b(monkeypatch, options):
    monkeypatch.setattr(
        'aspect_ratio_helper._util._OPT_KEY_TO_DEFAULT_MAP',
        {},
    )
    shared_opts = SharedOpts(options=options)
    assert _safe_opt_util(shared_opts, 'unknown_key') is None
