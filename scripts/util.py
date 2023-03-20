_MIN_DIMENSION = 64
_MAX_DIMENSION = 2048


def _scale_by_percentage(width, height, pct):
    aspect_ratio = float(width) / float(height)
    step = (pct - 1.0)
    new_width = max(int(round(width * (1.0 + step))), 1)
    new_height = max(int(round(new_width / aspect_ratio)), 1)
    if new_width > _MAX_DIMENSION:
        new_width = _MAX_DIMENSION
        new_height = max(int(round(new_width / aspect_ratio)), 1)
    if new_height > _MAX_DIMENSION:
        new_height = _MAX_DIMENSION
        new_width = max(int(round(new_height * aspect_ratio)), 1)
    if new_width < _MIN_DIMENSION:
        new_width = _MIN_DIMENSION
        new_height = max(int(round(new_width / aspect_ratio)), 1)
    if new_height < _MIN_DIMENSION:
        new_height = _MIN_DIMENSION
        new_width = max(int(round(new_height * aspect_ratio)), 1)
    return new_width, new_height


def _scale_dimensions_to_max_dimension(width, height, max_dim):
    if not _MIN_DIMENSION < max_dim < _MAX_DIMENSION:
        raise ValueError('Invalid dimension provided.')
    if max_dim == max(width, height):
        return width, height
    aspect_ratio = float(width) / float(height)
    if width > height:
        return max_dim, max(int(round(max_dim / aspect_ratio)), 1)
    return max(int(round(max_dim * aspect_ratio)), 1), max_dim
