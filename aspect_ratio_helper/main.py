import gradio as gr
from modules import script_callbacks
from modules import scripts

import aspect_ratio_helper._constants as _constants
import aspect_ratio_helper._settings as _settings


class AspectRatioStepScript(scripts.Script):

    def __init__(self):
        self.t2i_w = None
        self.t2i_h = None
        self.i2i_w = None
        self.i2i_h = None
        self.wc = None
        self.hc = None

    def title(self) -> str:
        return _constants.EXTENSION_NAME

    def show(self, _) -> scripts.AlwaysVisible:
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        if is_img2img:
            self.wc, self.hc = self.i2i_w, self.i2i_h
        else:
            self.wc, self.hc = self.t2i_h, self.t2i_w

        elements = _settings.sort_elements_by_keys(
            [element(self) for element in _settings.ELEMENTS],
        )

        if not any(element.should_show() for element in elements):
            return  # no elements should render, so just return.

        start_expanded: bool = _settings.safe_opt(
            _constants.ARH_EXPAND_BY_DEFAULT_KEY,
        )
        with gr.Group(), gr.Accordion(
                _constants.EXTENSION_NAME,
                open=start_expanded,
        ):
            for element in elements:
                if element.should_show():
                    element.render()

    def after_component(self, component: gr.components.Component, **kwargs):
        element_id = kwargs.get('elem_id')

        if isinstance(component, gr.components.Slider):
            if element_id == 'txt2img_width':
                self.t2i_w: gr.components.Slider = component
            elif element_id == 'txt2img_height':
                self.t2i_h: gr.components.Slider = component
            elif element_id == 'img2img_width':
                self.i2i_w: gr.components.Slider = component
            elif element_id == 'img2img_height':
                self.i2i_h: gr.components.Slider = component


script_callbacks.on_ui_settings(_settings.on_ui_settings)
