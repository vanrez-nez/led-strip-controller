from base_fx import BaseFx
import numpy as np
from gradient import Gradient
from color import lerp as lerp_color

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

    def linear_decay(self, value, decay_rate):
        """Linear decay function."""
        return value * decay_rate

    def ease_out_quad_decay(self, value, decay_rate):
        """Easing out quadratic decay where decay starts slow and accelerates."""
        return value * (1 - (1 - decay_rate) ** 2)

    def ease_in_quad_decay(self, value, decay_rate):
        """Easing in quadratic decay where decay starts fast and then slows down."""
        return value * (decay_rate ** 2)

    def ease_in_out_quad_decay(self, value, decay_rate):
        """Easing in and out quadratic decay for a more natural curve."""
        if decay_rate < 0.5:
            return value * (2 * decay_rate ** 2)
        else:
            return value * (1 - (2 * (1 - decay_rate) ** 2))

    def meter_fx(self):
        # Apply easing decay to last_level
        self.last_level = self.ease_out_quad_decay(self.last_level, self.decay)
        if self.level > self.last_level:
            self.last_level = self.level

        # Apply easing decay to last_peak
        self.last_peak = self.ease_out_quad_decay(self.last_peak, self.peak_decay)
        self.peak_heat = self.ease_in_quad_decay(self.peak_heat, self.peak_heat_decay)
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
                peak_pixel.rgb = lerp_color(self.gradient.get_color(self.last_peak), (255, 255, 255), self.peak_heat)
