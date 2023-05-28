from __future__ import annotations

import gradio as gr
from modules import script_callbacks
from modules import scripts

import aspect_ratio_helper._constants as _constants
import aspect_ratio_helper._settings as _settings


class AspectRatioStepScript(scripts.Script):

    def __init__(self):
        self.t2i_w: gr.components.Slider | None = None
        self.t2i_h: gr.components.Slider | None = None
        self.i2i_w: gr.components.Slider | None = None
        self.i2i_h: gr.components.Slider | None = None
        self.wc: gr.components.Slider
        self.hc: gr.components.Slider
        self.max_dimension: float

    def title(self) -> str:
        return _constants.EXTENSION_NAME

    def show(self, _) -> scripts.AlwaysVisible:
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        if is_img2img:
            self.wc, self.hc = self.i2i_w, self.i2i_h
        else:
            self.wc, self.hc = self.t2i_w, self.t2i_h  # noqa

        components = _settings.sort_components_by_keys(
            [component(self) for component in _settings.COMPONENTS],
        )

        hide_accordion: bool = _settings.safe_opt(
            _constants.ARH_HIDE_ACCORDION_BY_DEFAULT_KEY,
        )

        if hide_accordion or not any(c.should_show() for c in components):
            return  # no components should render, so just return.

        start_expanded: bool = _settings.safe_opt(
            _constants.ARH_EXPAND_BY_DEFAULT_KEY,
        )
        with gr.Group(), gr.Accordion(
                _constants.EXTENSION_NAME,
                open=start_expanded,
        ):
            for component in components:
                # we deliberately DON'T check component.should_show() here.
                # we need to call render to instantiate the components, we use
                # the visible property on each component to hide them.
                component.render()

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
