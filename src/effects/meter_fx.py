from base_fx import BaseFx
import numpy as np
from gradient import Gradient

class MeterFx(BaseFx):
    def __init__(self, segment, gradient: Gradient = None):
        super().__init__(segment)
        self.gradient = gradient
        self._decay = 0.9
        self._last_level = 0.0
        self.show_peak = True
        self.last_peak = 0.0
        self.effect_modes = {
            "meter": self.meter_fx,
        }

    def meter_fx(self):
        self._last_level *= self._decay
        if self.level > self._last_level:
            self._last_level = self.level
        for idx, pixel in enumerate(self.segment):
            i = self._last_level * len(self.segment)
            brightness = 255 if i >= idx else 0
            color_pos = (idx + 1) / len(self.segment)
            pixel.rgb = self.gradient.get_color(color_pos)
            pixel.brightness = brightness