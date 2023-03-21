import gradio as gr
from modules import shared

import aspect_ratio_helper._components as _components
import aspect_ratio_helper._constants as _constants
import aspect_ratio_helper._util as _util

PREDEFINED_PERCENTAGES_DISPLAY_MAP = {
    _constants.DEFAULT_PERCENTAGES_DISPLAY_KEY: _util.display_minus_and_plus,
    'Raw percentage (50%, 150%)': _util.display_raw_percentage,
    'Multiplication (x0.5, x1.5)': _util.display_multiplication,
}

ELEMENTS = (
    _components.MaxDimensionScaler,
    _components.PredefinedPercentageButtons,
)

DEFAULT_UI_COMPONENT_ORDER_KEY = ', '.join(
    [e.__name__ for e in ELEMENTS],  # noqa
)
OPT_KEY_TO_DEFAULT_MAP = {
    _constants.ARH_EXPAND_BY_DEFAULT_KEY: False,
    _constants.ARH_UI_COMPONENT_ORDER_KEY:
        DEFAULT_UI_COMPONENT_ORDER_KEY,
    _constants.ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY: True,
    _constants.ARH_MAX_WIDTH_OR_HEIGHT_KEY:
        _constants.MAX_DIMENSION / 2,
    _constants.ARH_SHOW_PREDEFINED_PERCENTAGES_KEY: True,
    _constants.ARH_PREDEFINED_PERCENTAGES_KEY:
        '25, 50, 75, 125, 150, 175, 200',
    _constants.ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY:
        _constants.DEFAULT_PERCENTAGES_DISPLAY_KEY,
}


def safe_opt(key):
    return _util.safe_opt_util(shared.opts, key, OPT_KEY_TO_DEFAULT_MAP)


def sort_elements_by_keys(
        elements: list[_components.ArhUIComponent],
) -> list[_components.ArhUIComponent]:
    ordered_component_keys = safe_opt(
        _constants.ARH_UI_COMPONENT_ORDER_KEY,
    ).split(',')
    try:
        component_key_to_order_dict = {
            key: order for order, key in enumerate(
                [k.strip() for k in ordered_component_keys],
            )
        }
        return sorted(
            elements,
            key=lambda c: component_key_to_order_dict.get(
                c.__class__.__name__,
            ),
        )
    except ValueError:
        print(
            f'{_constants.EXTENSION_NAME} UI component order is erroneous. '
            f'Defaulting to regular order, to fix this, please use'
            f'the intended syntax for the setting, i.e '
            f'"{DEFAULT_UI_COMPONENT_ORDER_KEY}"',
        )
        return elements


def on_ui_settings():
    section = 'aspect_ratio_helper', _constants.EXTENSION_NAME
    shared.opts.add_option(
        key=_constants.ARH_EXPAND_BY_DEFAULT_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_EXPAND_BY_DEFAULT_KEY,
            ),
            label='Expand by default',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_UI_COMPONENT_ORDER_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_UI_COMPONENT_ORDER_KEY,
            ),
            label='UI Component order',
            #  todo: temporary drop-down to avoid user error!
            #   we only have two components so 2 possible orders.
            #   however, this will exponentially grow with more components.
            #   if that happens, permutations is impractical, revisit then.
            component=gr.Dropdown,
            component_args=lambda: {
                'choices': (
                    DEFAULT_UI_COMPONENT_ORDER_KEY,
                    ', '.join(
                        DEFAULT_UI_COMPONENT_ORDER_KEY.split(',')[::-1],
                    ),
                ),
            },
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY,
            ),
            label='Show maximum width or height button',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_MAX_WIDTH_OR_HEIGHT_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_MAX_WIDTH_OR_HEIGHT_KEY,
            ),
            label='Maximum width or height default',
            component=gr.Slider,
            component_args={
                'minimum': _constants.MIN_DIMENSION,
                'maximum': _constants.MAX_DIMENSION,
                'step': 1,
            },
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_SHOW_PREDEFINED_PERCENTAGES_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_SHOW_PREDEFINED_PERCENTAGES_KEY,
            ),
            label='Show predefined percentage buttons',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_PREDEFINED_PERCENTAGES_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_PREDEFINED_PERCENTAGES_KEY,
            ),
            label='Predefined percentage buttons, applied to dimensions (75, '
                  '125, 150)',
            section=section,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY,
            ),
            label='Predefined percentage display format',
            component=gr.Dropdown,
            component_args=lambda: {
                'choices': tuple(PREDEFINED_PERCENTAGES_DISPLAY_MAP.keys()),
            },
            section=section,
        ),
    )
