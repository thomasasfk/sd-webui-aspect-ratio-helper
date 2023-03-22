from abc import ABC
from abc import abstractmethod
from functools import partial

import gradio as gr

import aspect_ratio_helper._constants as _constants
import aspect_ratio_helper._settings as _settings
import aspect_ratio_helper._util as _util


class ArhUIComponent(ABC):

    def __init__(self, script):
        self.script = script

    @abstractmethod
    def render(self): ...

    @staticmethod
    @abstractmethod
    def should_show() -> bool: ...


class MaxDimensionScaler(ArhUIComponent):
    def render(self):
        max_dim_default = _settings.safe_opt(
            _constants.ARH_MAX_WIDTH_OR_HEIGHT_KEY,
        )
        self.script.max_dimension = float(max_dim_default)

        inputs = outputs = [self.script.wc, self.script.hc]

        with gr.Row(
                visible=self.should_show(),
        ):
            max_dim_default = _settings.safe_opt(
                _constants.ARH_MAX_WIDTH_OR_HEIGHT_KEY,
            )
            # todo: when using gr.Slider (not deprecated), the default value
            #  is somehow always 270?... can't figure out why.
            #  using legacy inputs.Slider for now as it doesn't have the issue.
            max_dimension_slider = gr.inputs.Slider(
                minimum=_constants.MIN_DIMENSION,
                maximum=_constants.MAX_DIMENSION,
                step=1,
                default=max_dim_default,
                label='Maximum width or height (whichever is higher)',
            )

            def _update_max_dimension(_max_dimension):
                self.script.max_dimension = _max_dimension
            max_dimension_slider.change(
                _update_max_dimension,
                inputs=[max_dimension_slider],
                show_progress=False,
            )

            gr.Button(
                value='Scale to maximum width or height',
                visible=self.should_show(),
            ).click(
                fn=_util.scale_dimensions_to_max_dim,
                inputs=[*inputs, max_dimension_slider],
                outputs=outputs,
            )

    @staticmethod
    def should_show() -> bool:
        return _settings.safe_opt(_constants.ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY)


class PredefinedPercentageButtons(ArhUIComponent):

    def render(self):
        inputs = outputs = [self.script.wc, self.script.hc]
        with gr.Column(
                variant='panel',
                visible=self.should_show(),
        ), gr.Row(
            variant='compact',
            visible=self.should_show(),
        ):
            pps = _settings.safe_opt(_constants.ARH_PREDEFINED_PERCENTAGES_KEY)
            percentages = [abs(int(x)) for x in pps.split(',')]

            for percentage in percentages:
                display = self.display_func(percentage)
                gr.Button(
                    value=display,
                    visible=self.should_show(),
                ).click(
                    fn=partial(
                        _util.scale_by_percentage,
                        pct=percentage / 100,
                    ),
                    inputs=inputs,
                    outputs=outputs,
                )

    @staticmethod
    def should_show() -> bool:
        return _settings.safe_opt(
            _constants.ARH_SHOW_PREDEFINED_PERCENTAGES_KEY,
        )

    @property
    def display_func(self) -> callable:
        return _settings.PREDEFINED_PERCENTAGES_DISPLAY_MAP.get(
            _settings.safe_opt(
                _constants.ARH_PREDEFINED_PERCENTAGES_DISPLAY_KEY,
            ),
        )


class PredefinedAspectRatioButtons(ArhUIComponent):

    def render(self):
        use_max_dim_op = _settings.safe_opt(
            _constants.ARH_PREDEFINED_ASPECT_RATIO_USE_MAX_DIM_KEY,
        )

        with gr.Column(
                variant='panel',
                visible=self.should_show(),
        ), gr.Row(
            variant='compact',
            visible=self.should_show(),
        ):
            aspect_ratios = _settings.safe_opt(
                _constants.ARH_PREDEFINED_ASPECT_RATIOS_KEY,
            ).split(',')

            for ar_str in aspect_ratios:
                w, h, *_ = [abs(float(d)) for d in ar_str.split(':')]

                if use_max_dim_op:
                    ar_func = partial(
                        _util.scale_dimensions_to_max_dim_func,
                        width=w, height=h,
                        max_dim=lambda: self.script.max_dimension,
                    )
                    inputs = []
                else:
                    ar_func = partial(
                        _util.scale_dimensions_to_ui_width_or_height,
                        arw=w, arh=h,
                    )
                    inputs = [self.script.wc, self.script.hc]

                display = self.display_func(ar_str) or ar_str
                btn = gr.Button(
                    value=display,
                    visible=self.should_show(),
                )
                btn.click(
                    fn=ar_func,
                    inputs=inputs,
                    outputs=[self.script.wc, self.script.hc],
                )

    @staticmethod
    def should_show() -> bool:
        return _settings.safe_opt(
            _constants.ARH_SHOW_PREDEFINED_ASPECT_RATIOS_KEY,
        )

    @property
    def display_func(self) -> callable:
        return lambda _: None  # todo, different displays for aspect ratios.
