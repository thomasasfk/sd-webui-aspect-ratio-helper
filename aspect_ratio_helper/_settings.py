import gradio as gr
from modules import shared

from aspect_ratio_helper._constants import _ARH_EXPAND_BY_DEFAULT_KEY
from aspect_ratio_helper._constants import _ARH_MAX_WIDTH_OR_HEIGHT_KEY
from aspect_ratio_helper._constants import \
    _ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY
from aspect_ratio_helper._constants import _ARH_PREDEFINED_PERCENTAGES_KEY
from aspect_ratio_helper._constants import _ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY
from aspect_ratio_helper._constants import _ARH_SHOW_PREDEFINED_PERCENTAGES_KEY
from aspect_ratio_helper._constants import _ARH_UI_COMPONENT_ORDER_KEY
from aspect_ratio_helper._constants import _DEFAULT_PERCENTAGES_DISPLAY_KEY
from aspect_ratio_helper._constants import _DEFAULT_UI_COMPONENT_ORDER_KEY
from aspect_ratio_helper._constants import _EXTENSION_NAME
from aspect_ratio_helper._constants import _MAX_DIMENSION
from aspect_ratio_helper._constants import _MIN_DIMENSION
from aspect_ratio_helper._constants import _OPT_KEY_TO_DEFAULT_MAP
from aspect_ratio_helper._util import _display_minus_and_plus
from aspect_ratio_helper._util import _display_multiplication
from aspect_ratio_helper._util import _display_raw_percentage
from aspect_ratio_helper._util import _safe_opt_util

_PREDEFINED_PERCENTAGES_DISPLAY_MAP = {
    _DEFAULT_PERCENTAGES_DISPLAY_KEY: _display_minus_and_plus,
    'Raw percentage (50%, 150%)': _display_raw_percentage,
    'Multiplication (x0.5, x1.5)': _display_multiplication,
}


def _safe_opt(key):
    return _safe_opt_util(shared.opts, key)


def on_ui_settings():
    section = 'aspect_ratio_helper', _EXTENSION_NAME
    shared.opts.add_option(
        key=_ARH_EXPAND_BY_DEFAULT_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP.get(
                _ARH_EXPAND_BY_DEFAULT_KEY,
            ),
            label='Expand by default',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_UI_COMPONENT_ORDER_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP.get(
                _ARH_UI_COMPONENT_ORDER_KEY,
            ),
            label='UI Component order',
            #  todo: temporary drop-down to avoid user error!
            #   we only have two components so 2 possible orders.
            #   however, this will exponentially grow with more components.
            #   if that happens, permutations is impractical, revisit then.
            component=gr.Dropdown,
            component_args=lambda: {
                'choices': (
                    _DEFAULT_UI_COMPONENT_ORDER_KEY,
                    ', '.join(
                        _DEFAULT_UI_COMPONENT_ORDER_KEY.split(',')[::-1],
                    ),
                ),
            },
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP.get(
                _ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY,
            ),
            label='Show maximum width or height button',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_MAX_WIDTH_OR_HEIGHT_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP.get(
                _ARH_MAX_WIDTH_OR_HEIGHT_KEY,
            ),
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
            default=_OPT_KEY_TO_DEFAULT_MAP.get(
                _ARH_SHOW_PREDEFINED_PERCENTAGES_KEY,
            ),
            label='Show predefined percentage buttons',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_PREDEFINED_PERCENTAGES_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP.get(
                _ARH_PREDEFINED_PERCENTAGES_KEY,
            ),
            label='Predefined percentage buttons, applied to dimensions (75, '
                  '125, 150)',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY,
        info=shared.OptionInfo(
            default=_OPT_KEY_TO_DEFAULT_MAP.get(
                _ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY,
            ),
            label='Predefined percentage display format',
            component=gr.Dropdown,
            component_args=lambda: {
                'choices': tuple(_PREDEFINED_PERCENTAGES_DISPLAY_MAP.keys()),
            },
            section=section,
        ),
    )
