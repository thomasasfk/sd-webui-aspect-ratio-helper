from __future__ import annotations

import contextlib

import aspect_ratio_helper._constants as _const


def safe_opt_util(shared_opts, key, default_key_map: dict[str, object]):
    # attempt to retrieve key from shared options
    with contextlib.suppress(AttributeError):
        value = shared_opts.__getattr__(key)
        if value is not None:
            return value

    # attempt to retrieve default, and last resort the constant default
    return shared_opts.get_default(key) or default_key_map.get(key)


def display_multiplication(num) -> str:
    return f'x{round(num / 100, 3)}'


def display_raw_percentage(num) -> str:
    return f'{num}%'


def display_minus_and_plus(num) -> str:
    num -= 100
    if num > 0:
        return f'+{num}%'
    return f'{num}%'


def scale_by_percentage(width, height, pct) -> tuple[int, int]:
    aspect_ratio = float(width) / float(height)
    step = (pct - 1.0)
    new_width = int(round(width * (1.0 + step)))
    new_height = int(round(new_width / aspect_ratio))
    return clamp_to_boundaries(new_width, new_height, aspect_ratio)


def scale_dimensions_to_ui_width_or_height(
        width, height, arw, arh,
) -> tuple[int, int]:
    return scale_dimensions_to_max_dim(arw, arh, max(width, height))


def scale_dimensions_to_max_dim_func(
        width, height, max_dim: callable,
) -> tuple[int, int]:
    return scale_dimensions_to_max_dim(width, height, max_dim())


def scale_dimensions_to_max_dim(
        width, height, max_dim,
) -> tuple[int, int]:
    aspect_ratio = float(width) / float(height)
    return scale_dimensions_to_ar(width, height, max_dim, aspect_ratio)


def scale_dimensions_to_min_dim(
        width, height, min_dim,
) -> tuple[int, int]:
    aspect_ratio = float(width) / float(height)
    if width >= height:
        max_dim = min_dim * aspect_ratio
    else:
        max_dim = min_dim / aspect_ratio
    return scale_dimensions_to_ar(width, height, max_dim, aspect_ratio)


def scale_dimensions_to_ar(
        width, height, max_dim, aspect_ratio,
) -> tuple[int, int]:
    if width > height:
        new_width = max_dim
        new_height = int(round(max_dim / aspect_ratio))
    else:
        new_height = max_dim
        new_width = int(round(max_dim * aspect_ratio))
    return clamp_to_boundaries(new_width, new_height, aspect_ratio)


def round_to_multiple_of_8(value):
    return int(round(value / 8.0)) * 8


def clamp_to_boundaries(owidth, oheight, aspect_ratio) -> tuple[int, int]:
    width, height = owidth, oheight
    if width > _const.MAX_DIMENSION:
        width = _const.MAX_DIMENSION
        height = int(round(width / aspect_ratio))
    if height > _const.MAX_DIMENSION:
        height = _const.MAX_DIMENSION
        width = int(round(height * aspect_ratio))
    if width < _const.MIN_DIMENSION:
        width = _const.MIN_DIMENSION
        height = int(round(width / aspect_ratio))
    if height < _const.MIN_DIMENSION:
        height = _const.MIN_DIMENSION
        width = int(round(height * aspect_ratio))

    width = round_to_multiple_of_8(width)
    height = round_to_multiple_of_8(height)
    # for insane aspect ratios we don't support... i.e 1:100
    # 64:6400 when run through this function, so we clamp to 64:2048 (‾◡◝)
    # also.  when the user does this it breaks the "scale to max" function
    # on the ui until they change to another reasonable aspect ratio.
    # todo: figure out why ^ and handle it better.
    if width < _const.MIN_DIMENSION:
        width = _const.MIN_DIMENSION
    elif width > _const.MAX_DIMENSION:
        width = _const.MAX_DIMENSION
    if height < _const.MIN_DIMENSION:
        height = _const.MIN_DIMENSION
    elif height > _const.MAX_DIMENSION:
        height = _const.MAX_DIMENSION

    return width, height
