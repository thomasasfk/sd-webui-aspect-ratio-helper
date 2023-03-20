import contextlib
from functools import partial

import gradio as gr
from modules import script_callbacks
from modules import scripts
from modules import shared
from modules.shared import opts

_MIN_DIMENSION = 64
_MAX_DIMENSION = 2048
_EXTENSION_NAME = 'Aspect Ratio Helper'


def on_ui_settings():
    section = 'aspect_ratio_helper', _EXTENSION_NAME
    shared.opts.add_option(
        key='arh_expand_by_default',
        info=shared.OptionInfo(
            default=False,
            label='Expand by default',
            section=section,
        ),
    )
    shared.opts.add_option(
        key='arh_show_max_width_or_height',
        info=shared.OptionInfo(
            default=True,
            label='Show maximum width or height button',
            section=section,
        ),
    )
    shared.opts.add_option(
        key='arh_max_width_or_height',
        info=shared.OptionInfo(
            default=1024,
            label='Maximum width or height default',
            section=section,
        ),
    )
    shared.opts.add_option(
        key='arh_show_predefined_percentages',
        info=shared.OptionInfo(
            default=True,
            label='Show percentage buttons',
            section=section,
        ),
    )
    shared.opts.add_option(
        key='arh_predefined_percentages',
        info=shared.OptionInfo(
            default='25, 50, 75, 125, 150, 175, 200',
            label='Percentage buttons (75, 125, 150)',
            section=section,
        ),
    )


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
    if max_dim == max(width, height):
        return width, height
    aspect_ratio = float(width) / float(height)
    if width > height:
        return max_dim, max(int(round(max_dim / aspect_ratio)), 1)
    return max(int(round(max_dim * aspect_ratio)), 1), max_dim


class AspectRatioStepScript(scripts.Script):

    def title(self):
        return _EXTENSION_NAME

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        if not any([
            opts.arh_show_max_width_or_height,
            opts.arh_show_predefined_percentages,
        ]):
            return  # return early as no 'show' options enabled

        with (
            gr.Group(),
            gr.Accordion(_EXTENSION_NAME, open=opts.arh_expand_by_default),
            contextlib.suppress(AttributeError),
        ):
            if is_img2img:
                inputs = outputs = [self.i2i_w, self.i2i_h]
            else:
                inputs = outputs = [self.t2i_w, self.t2i_h]

            if opts.arh_show_max_width_or_height:
                with gr.Row():
                    max_dimension = gr.inputs.Slider(
                        minimum=64,
                        maximum=2048,
                        step=16,
                        default=opts.arh_max_width_or_height,
                        label='Maximum width or height (whichever is higher)',
                    )
                    gr.Button(value='Scale to maximum width or height').click(
                        fn=_scale_dimensions_to_max_dimension,
                        inputs=[*inputs, max_dimension],
                        outputs=outputs,
                    )

            if opts.arh_show_predefined_percentages:
                with gr.Column(variant='panel'), gr.Row(variant='compact'):
                    pps = opts.arh_predefined_percentages
                    percentages = [
                        int(x) for x in pps.split(',')
                    ]
                    for percentage in percentages:
                        gr.Button(value=f'{str(percentage)}%').click(
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
