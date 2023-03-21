from abc import ABC
from abc import abstractmethod
from functools import partial

import gradio as gr
from modules import script_callbacks
from modules import scripts

from aspect_ratio_helper._constants import _ARH_EXPAND_BY_DEFAULT_KEY
from aspect_ratio_helper._constants import _ARH_MAX_WIDTH_OR_HEIGHT_KEY
from aspect_ratio_helper._constants import \
    _ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY
from aspect_ratio_helper._constants import _ARH_PREDEFINED_PERCENTAGES_KEY
from aspect_ratio_helper._constants import _ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY
from aspect_ratio_helper._constants import _ARH_SHOW_PREDEFINED_PERCENTAGES_KEY
from aspect_ratio_helper._constants import _ARH_UI_COMPONENT_ORDER_KEY
from aspect_ratio_helper._constants import _EXTENSION_NAME
from aspect_ratio_helper._constants import _MAX_DIMENSION
from aspect_ratio_helper._constants import _MIN_DIMENSION
from aspect_ratio_helper._settings import _PREDEFINED_PERCENTAGES_DISPLAY_MAP
from aspect_ratio_helper._settings import _safe_opt
from aspect_ratio_helper._settings import on_ui_settings
from aspect_ratio_helper._util import _scale_by_percentage
from aspect_ratio_helper._util import _scale_dimensions_to_max_dimension


class _ArhUIElement(ABC):
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs

    @abstractmethod
    def render(self): ...

    @property
    @abstractmethod
    def should_show(self): ...

    @property
    def unique_key(self):
        return self.__class__.__name__


class _MaxDimensionScaler(_ArhUIElement):
    def render(self):
        with gr.Row():
            max_dimension = gr.inputs.Slider(
                minimum=_MIN_DIMENSION,
                maximum=_MAX_DIMENSION,
                step=1,
                default=_safe_opt(_ARH_MAX_WIDTH_OR_HEIGHT_KEY),
                label='Maximum width or height (whichever is higher)',
            )
            gr.Button(value='Scale to maximum width or height').click(
                fn=_scale_dimensions_to_max_dimension,
                inputs=[*self.inputs, max_dimension],
                outputs=self.outputs,
            )

    @property
    def should_show(self):
        return _safe_opt(_ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY)


class _PredefinedPercentageButtons(_ArhUIElement):

    def render(self):
        with gr.Column(variant='panel'), gr.Row(variant='compact'):
            pps = _safe_opt(_ARH_PREDEFINED_PERCENTAGES_KEY)
            percentages = [abs(int(x)) for x in pps.split(',')]
            for percentage in percentages:
                display = self.display_func(percentage)
                gr.Button(value=display).click(
                    fn=partial(_scale_by_percentage, pct=percentage / 100),
                    inputs=self.inputs,
                    outputs=self.outputs,
                )

    @property
    def should_show(self):
        return _safe_opt(_ARH_SHOW_PREDEFINED_PERCENTAGES_KEY)

    @property
    def display_func(self):
        return _PREDEFINED_PERCENTAGES_DISPLAY_MAP.get(
            _safe_opt(_ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY),
        )


class AspectRatioStepScript(scripts.Script):

    def title(self):
        return _EXTENSION_NAME

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        if is_img2img:
            inputs = outputs = [self.i2i_w, self.i2i_h]
        else:
            inputs = outputs = [self.t2i_w, self.t2i_h]

        elements: list[_ArhUIElement] = [
            _MaxDimensionScaler(inputs, outputs),
            _PredefinedPercentageButtons(inputs, outputs),
        ]

        if not any([e.should_show for e in elements]):
            return  # no elements should render, so just return.

        try:
            el_key_order = _safe_opt(_ARH_UI_COMPONENT_ORDER_KEY).split(',')
            eo_dict = {
                key: o for o, key in enumerate(
                    [x.strip() for x in el_key_order],
                )
            }
            sorted_elements = sorted(
                elements, key=lambda el: eo_dict.get(el.unique_key),
            )
        except ValueError:
            print(
                f'{_EXTENSION_NAME} UI component order is erroneous. '
                f'Defaulting to regular order, to fix this, please use'
                f'the intended syntax for the setting, i.e '
                f'"{_MaxDimensionScaler}, {_PredefinedPercentageButtons}"',
            )
            sorted_elements = elements

        start_expanded = _safe_opt(_ARH_EXPAND_BY_DEFAULT_KEY)
        with gr.Group(), gr.Accordion(_EXTENSION_NAME, open=start_expanded):
            for element in sorted_elements:
                if element.should_show:
                    element.render()

    def after_component(self, component, **kwargs):
        element_id = kwargs.get('elem_id')

        if element_id == 'txt2img_width':
            self.t2i_w = component
        elif element_id == 'txt2img_height':
            self.t2i_h = component
        elif element_id == 'img2img_width':
            self.i2i_w = component
        elif element_id == 'img2img_height':
            self.i2i_h = component


script_callbacks.on_ui_settings(on_ui_settings)
