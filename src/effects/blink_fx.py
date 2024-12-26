from base_fx import BaseFx
import numpy as np
from gradient import Gradient

class BlinkFx(BaseFx):
    def __init__(self, segment, color=(255, 255, 255), gradient: Gradient = None, interval = 500, smooth = False):
        super().__init__(segment)
        self.color = color
        self.gradient = gradient
        self.interval = interval
        self.smooth = smooth
        self._decay = 0.92
        self._last_level = 0.0
        self.effect_modes = {
            "strobe": self.strobe_fx,
            "smooth": self.smooth_fx,
        }

    def _set_color(self, t, brightness=255):
        use_gradient = self.gradient and t is not None
        color = self.gradient.get_color(t) if use_gradient else self.color
        self.gradient.shift_color_group(self.elapsed_time * 0.0001)
        for pixel in self.segment:
            pixel.rgb = color
            pixel.brightness = brightness

    def smooth_fx(self):
        self._last_level *= self._decay
        if self.level > self._last_level:
            self._last_level = self.level
        self._set_color(self._last_level)

    def strobe_fx(self):
        self._set_color(self.level)
