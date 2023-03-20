import contextlib

import gradio as gr
from modules import shared

from aspect_ratio_helper._constants import _ARH_EXPAND_BY_DEFAULT_KEY
from aspect_ratio_helper._constants import _ARH_MAX_WIDTH_OR_HEIGHT_KEY
from aspect_ratio_helper._constants import \
    _ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY
from aspect_ratio_helper._constants import _ARH_PREDEFINED_PERCENTAGES_KEY
from aspect_ratio_helper._constants import _ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY
from aspect_ratio_helper._constants import _ARH_SHOW_PREDEFINED_PERCENTAGES_KEY
from aspect_ratio_helper._constants import _DEFAULT_PERCENTAGES_DISPLAY_KEY
from aspect_ratio_helper._constants import _EXTENSION_NAME
from aspect_ratio_helper._constants import _MAX_DIMENSION
from aspect_ratio_helper._constants import _MIN_DIMENSION
from aspect_ratio_helper._constants import _OPT_KEY_TO_DEFAULT_MAP
from aspect_ratio_helper._util import _display_minus_and_plus
from aspect_ratio_helper._util import _display_multiplication
from aspect_ratio_helper._util import _display_raw_percentage

_PREDEFINED_PERCENTAGES_DISPLAY_MAP = {
    _DEFAULT_PERCENTAGES_DISPLAY_KEY: _display_minus_and_plus,
    'Raw percentage (50%, 150%)': _display_raw_percentage,
    'Multiplication (x0.5, x1.5)': _display_multiplication,
}


# todo: add test coverage to this?..
def _safe_opt(key):
    # attempt to retrieve key from shared options
    with contextlib.suppress(AttributeError):
        return shared.opts.__getattr__(key)

    # attempt to retrieve default, and last resort the constant default
    return shared.opts.get_default(key) or _OPT_KEY_TO_DEFAULT_MAP.get(key)


def on_ui_settings():
    section = 'aspect_ratio_helper', _EXTENSION_NAME
    shared.opts.add_option(
        key=_ARH_EXPAND_BY_DEFAULT_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP[_ARH_EXPAND_BY_DEFAULT_KEY],
            label='Expand by default',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP[_ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY],
            label='Show maximum width or height button',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_MAX_WIDTH_OR_HEIGHT_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP[_ARH_MAX_WIDTH_OR_HEIGHT_KEY],
            label='Maximum width or height default',
            component=gr.Slider,
            component_args={
                'minimum': _MIN_DIMENSION,
                'maximum': _MAX_DIMENSION,
                'step': 1,
            },
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_SHOW_PREDEFINED_PERCENTAGES_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP[
                _ARH_SHOW_PREDEFINED_PERCENTAGES_KEY
            ],
            label='Show predefined percentage buttons',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_PREDEFINED_PERCENTAGES_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP[_ARH_PREDEFINED_PERCENTAGES_KEY],
            label='Predefined percentage buttons, applied to dimensions (75, '
                  '125, 150)',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP[
                _ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY
            ],
            label='Predefined percentage display format',
            component=gr.Dropdown,
            component_args=lambda: {
                'choices': tuple(_PREDEFINED_PERCENTAGES_DISPLAY_MAP.keys()),
            },
            section=section,
        ),
    )
