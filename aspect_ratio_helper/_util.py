import contextlib

from aspect_ratio_helper._constants import _MAX_DIMENSION
from aspect_ratio_helper._constants import _MIN_DIMENSION
from aspect_ratio_helper._constants import _OPT_KEY_TO_DEFAULT_MAP


def _safe_opt_util(shared_opts, key):
    # attempt to retrieve key from shared options
    with contextlib.suppress(AttributeError):
        value = shared_opts.__getattr__(key)
        if value is not None:
            return value

    # attempt to retrieve default, and last resort the constant default
    return shared_opts.get_default(key) or _OPT_KEY_TO_DEFAULT_MAP.get(key)


def _display_multiplication(num):
    return f'x{round(num / 100, 3)}'


def _display_raw_percentage(num):
    return f'{num}%'


def _display_minus_and_plus(num):
    num -= 100
    if num > 0:
        return f'+{num}%'
    return f'{num}%'


def _scale_by_percentage(width, height, pct):
    aspect_ratio = float(width) / float(height)
    step = (pct - 1.0)
    new_width = int(round(width * (1.0 + step)))
    new_height = int(round(new_width / aspect_ratio))
    return _clamp_to_boundaries(new_width, new_height, aspect_ratio)


def _scale_dimensions_to_max_dimension(width, height, max_dim):
    aspect_ratio = float(width) / float(height)
    if width > height:
        new_width = max_dim
        new_height = max(int(round(max_dim / aspect_ratio)), 1)
    else:
        new_height = max_dim
        new_width = max(int(round(max_dim * aspect_ratio)), 1)
    return _clamp_to_boundaries(new_width, new_height, aspect_ratio)


def _clamp_to_boundaries(width, height, aspect_ratio):
    if width > _MAX_DIMENSION:
        width = _MAX_DIMENSION
        height = int(round(width / aspect_ratio))
    if height > _MAX_DIMENSION:
        height = _MAX_DIMENSION
        width = int(round(height * aspect_ratio))
    if width < _MIN_DIMENSION:
        width = _MIN_DIMENSION
        height = int(round(width / aspect_ratio))
    if height < _MIN_DIMENSION:
        height = _MIN_DIMENSION
        width = int(round(height * aspect_ratio))
    return width, height
