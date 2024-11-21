from base_fx import BaseFx
import numpy as np

class BlinkFx(BaseFx):
    def __init__(self, segment, color=(255, 255, 255), interval=500):
        super().__init__(segment)
        self.color = color
        self.interval = interval

    def apply_effect(self):
        is_on = np.floor(self.elapsed_time / self.interval) % 2 == 0
        for pixel in self.segment:
            pixel.brightness = 255 if is_on else 0
            pixel.rgb = self.color if is_on else (0, 0, 0)
