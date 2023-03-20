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
from aspect_ratio_helper._constants import _EXTENSION_NAME
from aspect_ratio_helper._constants import _MAX_DIMENSION
from aspect_ratio_helper._constants import _MIN_DIMENSION
from aspect_ratio_helper._settings import _PREDEFINED_PERCENTAGES_DISPLAY_MAP
from aspect_ratio_helper._settings import _safe_opt
from aspect_ratio_helper._settings import on_ui_settings
from aspect_ratio_helper._util import _scale_by_percentage
from aspect_ratio_helper._util import _scale_dimensions_to_max_dimension


class AspectRatioStepScript(scripts.Script):

    def title(self):
        return _EXTENSION_NAME

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        if not any([
            _safe_opt(_ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY),
            _safe_opt(_ARH_SHOW_PREDEFINED_PERCENTAGES_KEY),
        ]):
            return  # return early as no 'show' options enabled
        with (
            gr.Group(),
            gr.Accordion(
                _EXTENSION_NAME,
                open=_safe_opt(_ARH_EXPAND_BY_DEFAULT_KEY),
            ),
        ):
            if is_img2img:
                inputs = outputs = [self.i2i_w, self.i2i_h]
            else:
                inputs = outputs = [self.t2i_w, self.t2i_h]

            if _safe_opt(_ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY):
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
                        inputs=[*inputs, max_dimension],
                        outputs=outputs,
                    )

            if _safe_opt(_ARH_SHOW_PREDEFINED_PERCENTAGES_KEY):
                display_func = _PREDEFINED_PERCENTAGES_DISPLAY_MAP.get(
                    _safe_opt(_ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY),
                )
                with gr.Column(variant='panel'), gr.Row(variant='compact'):
                    pps = _safe_opt(_ARH_PREDEFINED_PERCENTAGES_KEY)
                    percentages = [
                        abs(int(x)) for x in pps.split(',')
                    ]
                    for percentage in percentages:
                        gr.Button(value=display_func(percentage)).click(
                            fn=partial(
                                _scale_by_percentage, pct=percentage / 100,
                            ),
                            inputs=inputs,
                            outputs=outputs,
                        )

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
