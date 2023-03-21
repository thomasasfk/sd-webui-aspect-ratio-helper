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
        inputs = outputs = [self.script.wc, self.script.hc]
        with gr.Row():
            max_dimension = gr.inputs.Slider(
                minimum=_constants.MIN_DIMENSION,
                maximum=_constants.MAX_DIMENSION,
                step=1,
                default=_settings.safe_opt(
                    _constants.ARH_MAX_WIDTH_OR_HEIGHT_KEY,
                ),
                label='Maximum width or height (whichever is higher)',
            )
            gr.Button(value='Scale to maximum width or height').click(
                fn=_util.scale_dimensions_to,
                inputs=[*inputs, max_dimension],
                outputs=outputs,
            )

    @staticmethod
    def should_show() -> bool:
        return _settings.safe_opt(_constants.ARH_SHOW_MAX_WIDTH_OR_HEIGHT_KEY)


class PredefinedPercentageButtons(ArhUIComponent):

    def render(self):
        inputs = outputs = [self.script.wc, self.script.hc]
        with gr.Column(variant='panel'), gr.Row(variant='compact'):
            pps = _settings.safe_opt(_constants.ARH_PREDEFINED_PERCENTAGES_KEY)
            percentages = [abs(int(x)) for x in pps.split(',')]
            for percentage in percentages:
                display = self.display_func(percentage)
                gr.Button(value=display).click(
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
