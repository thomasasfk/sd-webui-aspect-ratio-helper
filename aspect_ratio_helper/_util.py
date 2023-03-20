def _display_multiplication(num):
    return f'x{round(num / 100, 3)}'


def _display_raw_percentage(num):
    return f'{num}%'


def _display_minus_and_plus(num):
    num -= 100
    if num > 0:
        return f'+{num}%'
    return f'{num}%'


_DEFAULT_DISPLAY_KEY = 'Incremental/decremental percentage (-50%, +50%)'
_PREDEFINED_PERCENTAGES_DISPLAY_MAP = {
    _DEFAULT_DISPLAY_KEY: _display_minus_and_plus,
    'Raw percentage (50%, 150%)': _display_raw_percentage,
    'Multiplication (x0.5, x1.5)': _display_multiplication,
}

_MIN_DIMENSION = 64
_MAX_DIMENSION = 2048


def _scale_by_percentage(width, height, pct):
    aspect_ratio = float(width) / float(height)
    step = (pct - 1.0)
    new_width = int(round(width * (1.0 + step)))
    new_height = int(round(new_width / aspect_ratio))
    if new_width > _MAX_DIMENSION:
        new_width = _MAX_DIMENSION
        new_height = int(round(new_width / aspect_ratio))
    if new_height > _MAX_DIMENSION:
        new_height = _MAX_DIMENSION
        new_width = int(round(new_height * aspect_ratio))
    if new_width < _MIN_DIMENSION:
        new_width = _MIN_DIMENSION
        new_height = int(round(new_width / aspect_ratio))
    if new_height < _MIN_DIMENSION:
        new_height = _MIN_DIMENSION
        new_width = int(round(new_height * aspect_ratio))
    return new_width, new_height


def _scale_dimensions_to_max_dimension(width, height, max_dim):
    if max_dim < _MIN_DIMENSION:
        max_dim = _MIN_DIMENSION
    elif max_dim > _MAX_DIMENSION:
        max_dim = _MAX_DIMENSION
    if max_dim == max(width, height):
        return width, height
    aspect_ratio = float(width) / float(height)
    if width > height:
        return max_dim, max(int(round(max_dim / aspect_ratio)), 1)
    return max(int(round(max_dim * aspect_ratio)), 1), max_dim
