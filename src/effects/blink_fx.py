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

    def strobe_effect(self):
        is_on = np.floor(self.elapsed_time / self.interval) % 2 == 0
        for pixel in self.segment:
            pixel.brightness = 255 if is_on else 0
            pixel.rgb = self.color if is_on else (0, 0, 0)

    def smooth_effect(self):
        t = self.elapsed_time / self.interval
        t = t - np.floor(t)
        brightness = 255 * np.sin(t * np.pi)
        color = self.color
        if self.gradient:
            color = self.gradient.get_color(t)
        for pixel in self.segment:
            pixel.brightness = brightness
            pixel.rgb = color

    def apply_effect(self):
        if self.smooth:
            self.smooth_effect()
        else:
            self.strobe_effect()
