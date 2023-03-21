_EXTENSION_NAME = 'Aspect Ratio Helper'

_MAX_DIMENSION = 2048
_MIN_DIMENSION = 64

_ARH_EXPAND_BY_DEFAULT_KEY = 'arh_expand_by_default'
_ARH_UI_COMPONENT_ORDER_KEY = 'arh_ui_component_order_key'
_ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY = 'arh_show_max_width_or_height'
_ARH_MAX_WIDTH_OR_HEIGHT_KEY = 'arh_max_width_or_height'
_ARH_SHOW_PREDEFINED_PERCENTAGES_KEY = 'arh_show_predefined_percentages'
_ARH_PREDEFINED_PERCENTAGES_KEY = 'arh_predefined_percentages'
_ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY \
    = 'arh_predefined_percentages_display_key'

_DEFAULT_PERCENTAGES_DISPLAY_KEY \
    = 'Incremental/decremental percentage (-50%, +50%)'
_DEFAULT_UI_COMPONENT_ORDER_KEY =\
    '_MaxDimensionScaler, _PredefinedPercentageButtons'  # todo: dynamic.
_OPT_KEY_TO_DEFAULT_MAP = {
    _ARH_EXPAND_BY_DEFAULT_KEY: False,
    _ARH_UI_COMPONENT_ORDER_KEY: _DEFAULT_UI_COMPONENT_ORDER_KEY,
    _ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY: True,
    _ARH_MAX_WIDTH_OR_HEIGHT_KEY: _MAX_DIMENSION / 2,
    _ARH_SHOW_PREDEFINED_PERCENTAGES_KEY: True,
    _ARH_PREDEFINED_PERCENTAGES_KEY: '25, 50, 75, 125, 150, 175, 200',
    _ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY: _DEFAULT_PERCENTAGES_DISPLAY_KEY,
}
