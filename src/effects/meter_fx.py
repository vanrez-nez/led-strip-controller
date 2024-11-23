from base_fx import BaseFx
import numpy as np
from gradient import Gradient
from color import lerp as lerp_color
import easing

class MeterFx(BaseFx):
    def __init__(self, segment, gradient: Gradient = None):
        super().__init__(segment)
        self.gradient = gradient
        self.decay = 0.6
        self.peak_decay = 0.94
        self.last_level = 0.0
        self.show_peak = True
        self.peak_heat = 0.0
        self.peak_heat_decay = 0.9
        self.last_peak = 0.0
        self.effect_modes = {
            "meter": self.meter_fx,
        }

    def meter_fx(self):
        # Apply easing decay to last_level
        self.last_level *= easing.easeInQuad(self.decay)
        if self.level > self.last_level:
            self.last_level = self.level

        # Apply easing decay to last_peak
        self.last_peak *= easing.easeOutQuad(self.peak_decay)
        self.peak_heat *= easing.easeInQuad(self.peak_heat_decay)
        if self.level > self.last_peak:
            self.peak_heat = 1
            self.last_peak = self.level

        for idx, pixel in enumerate(self.segment):
            i = self.last_level * len(self.segment)
            brightness = 255 if i >= idx else 0
            color_pos = (idx + 1) / len(self.segment)
            pixel.rgb = self.gradient.get_color(color_pos)
            pixel.brightness = brightness

        if self.show_peak:
            peak_idx = int(min(self.last_peak * len(self.segment), len(self.segment) - 1))
            if peak_idx < len(self.segment):
                peak_pixel = self.segment[peak_idx]
                peak_pixel.brightness = 255
                peak_pixel.rgb = lerp_color(self.gradient.get_color(self.last_peak), (255, 250, 250), self.peak_heat)
