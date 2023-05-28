from __future__ import annotations

import itertools

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

COMPONENTS = (
    _components.MaxDimensionScaler,
    _components.MinDimensionScaler,
    _components.PredefinedAspectRatioButtons,
    _components.PredefinedPercentageButtons,
)

DEFAULT_UI_COMPONENT_ORDER_KEY_LIST = [e.__name__ for e in COMPONENTS]
DEFAULT_UI_COMPONENT_ORDER_KEY = ', '.join(
    DEFAULT_UI_COMPONENT_ORDER_KEY_LIST,
)
OPT_KEY_TO_DEFAULT_MAP = {
    _constants.ARH_EXPAND_BY_DEFAULT_KEY: False,
    _constants.ARH_HIDE_ACCORDION_BY_DEFAULT_KEY: True,
    _constants.ARH_UI_COMPONENT_ORDER_KEY:
        DEFAULT_UI_COMPONENT_ORDER_KEY,
    _constants.ARH_UI_JAVASCRIPT_SELECTION_METHOD: 'Aspect Ratios Dropdown',
    _constants.ARH_JAVASCRIPT_ASPECT_RATIO_SHOW_KEY: True,
    _constants.ARH_JAVASCRIPT_ASPECT_RATIOS_KEY:
        '1:1, 3:2, 4:3, 5:4, 16:9',
    _constants.ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY: False,
    _constants.ARH_MAX_WIDTH_OR_HEIGHT_KEY:
        _constants.MAX_DIMENSION / 2,
    _constants.ARH_SHOW_MIN_WIDTH_OR_HEIGHT_KEY: False,
    _constants.ARH_MIN_WIDTH_OR_HEIGHT_KEY:
        _constants.MAX_DIMENSION / 2,
    _constants.ARH_SHOW_PREDEFINED_PERCENTAGES_KEY: False,
    _constants.ARH_PREDEFINED_PERCENTAGES_KEY:
        '25, 50, 75, 125, 150, 175, 200',
    _constants.ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY:
        _constants.DEFAULT_PERCENTAGES_DISPLAY_KEY,
    _constants.ARH_SHOW_PREDEFINED_ASPECT_RATIOS_KEY: False,
    _constants.ARH_PREDEFINED_ASPECT_RATIO_USE_MAX_DIM_KEY: False,
    _constants.ARH_PREDEFINED_ASPECT_RATIOS_KEY:
        '1:1, 4:3, 16:9, 9:16, 21:9',
}


def safe_opt(key):
    return _util.safe_opt_util(shared.opts, key, OPT_KEY_TO_DEFAULT_MAP)


def sort_components_by_keys(
        components: list[_components.ArhUIComponent],
) -> list[_components.ArhUIComponent]:
    ordered_component_keys = safe_opt(
        _constants.ARH_UI_COMPONENT_ORDER_KEY,
    ).split(',')

    # this can happen if we add new components, but the user has old settings.
    # if this happens, we find the missing components, and append them.
    if len(ordered_component_keys) != len(COMPONENTS):
        all_components = set(DEFAULT_UI_COMPONENT_ORDER_KEY_LIST)
        missing_components = all_components - set(ordered_component_keys)
        ordered_component_keys.extend(missing_components)

    try:
        component_key_to_order_dict = {
            key: order for order, key in enumerate(
                [k.strip() for k in ordered_component_keys],
            )
        }
        return sorted(
            components,
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
        return components


def on_ui_settings():
    # javascript ui options
    shared.opts.add_option(
        key=_constants.ARH_JAVASCRIPT_ASPECT_RATIO_SHOW_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_JAVASCRIPT_ASPECT_RATIO_SHOW_KEY,
            ),
            label='Enable JavaScript aspect ratio controls',
            section=_constants.SECTION,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_JAVASCRIPT_ASPECT_RATIOS_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_JAVASCRIPT_ASPECT_RATIOS_KEY,
            ),
            label='JavaScript aspect ratio buttons'
                  ' (1:1, 4:3, 16:9, 9:16, 21:9)',
            section=_constants.SECTION,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_UI_JAVASCRIPT_SELECTION_METHOD,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_UI_JAVASCRIPT_SELECTION_METHOD,
            ),
            label='JavaScript selection method',
            component=gr.Dropdown,
            component_args=lambda: {
                'choices': [
                    'Aspect Ratios Dropdown',
                    'Default Options Button',
                ],
            },
            section=_constants.SECTION,
        ),
    )

    # accordion options
    shared.opts.add_option(
        key=_constants.ARH_HIDE_ACCORDION_BY_DEFAULT_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_HIDE_ACCORDION_BY_DEFAULT_KEY,
            ),
            label='Hide accordion by default',
            section=_constants.SECTION,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_EXPAND_BY_DEFAULT_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_EXPAND_BY_DEFAULT_KEY,
            ),
            label='Expand accordion by default',
            section=_constants.SECTION,
        ),
    )
    shared.opts.add_option(
        key=_constants.ARH_UI_COMPONENT_ORDER_KEY,
        info=shared.OptionInfo(
            default=OPT_KEY_TO_DEFAULT_MAP.get(
                _constants.ARH_UI_COMPONENT_ORDER_KEY,
            ),
            label='UI Component order',
            component=gr.Dropdown,
            component_args=lambda: {
                'choices': [
                    ', '.join(p) for p in itertools.permutations(  # TODO:  Rethink this, exponential growth...
                        DEFAULT_UI_COMPONENT_ORDER_KEY_LIST,
                    )
                ],
            },
            section=_constants.SECTION,
        ),
    )

    for component in COMPONENTS:
        component.add_options(shared)
