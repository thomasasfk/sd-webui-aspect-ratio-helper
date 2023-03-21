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


def scale_dimensions_to(
        width, height, max_dim,
) -> tuple[int, int]:
    aspect_ratio = float(width) / float(height)
    if width > height:
        new_width = max_dim
        new_height = int(round(max_dim / aspect_ratio))
    else:
        new_height = max_dim
        new_width = int(round(max_dim * aspect_ratio))
    return clamp_to_boundaries(new_width, new_height, aspect_ratio)


def clamp_to_boundaries(width, height, aspect_ratio) -> tuple[int, int]:
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
    return width, height
