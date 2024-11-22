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
            "strobe_level": self.level_strobe_fx,
            "smooth_level": self.level_smooth_fx,
        }

    def level_smooth_fx(self):
        for pixel in self.segment:
            pixel.brightness = 255
            pixel.rgb = self.gradient.get_color(self.signal_level) if self.gradient else self.color

    def level_strobe_fx(self):
        self._last_level *= self._decay
        if self.signal_level > self._last_level:
            self._last_level = self.signal_level
        for pixel in self.segment:
            pixel.brightness = 255
            pixel.rgb = self.gradient.get_color(self._last_level) if self.gradient else self.color

    def strobe_fx(self):
        is_on = np.floor(self.elapsed_time / self.interval) % 2 == 0
        for pixel in self.segment:
            pixel.brightness = 255 if is_on else 0
            pixel.rgb = self.color if is_on else (0, 0, 0)

    def smooth_fx(self):
        t = self.elapsed_time / self.interval
        t = t - np.floor(t)
        brightness = 255 * np.sin(t * np.pi)
        color = self.color
        if self.gradient:
            color = self.gradient.get_color(t)
        for pixel in self.segment:
            pixel.brightness = brightness
            pixel.rgb = color