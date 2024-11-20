from base_fx import BaseFx
import numpy as np

class BlinkFx(BaseFx):
    def __init__(self, segment, color=(255, 255, 255), interval=500):
        """
        Parameters:
        - segment (Segment): The LED segment strip to apply the effect to.
        - color (tuple): RGB color tuple for the "on" state.
        - interval (int): Time in milliseconds between state toggles.
        """
        super().__init__(segment)
        self.color = color
        self.interval = interval  # milliseconds
        self.is_on = False

    def apply_effect(self):
        if self.elapsed_time >= self.interval:
            self.is_on = not self.is_on
            for pixel in self.segment:
                pixel.rgb = self.color if self.is_on else (0, 0, 0)
                print(pixel.rgb)
