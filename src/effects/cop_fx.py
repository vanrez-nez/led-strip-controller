from base_fx import BaseFx
import numpy as np

class CopFx(BaseFx):
    def __init__(self, segment, alternate_interval=100, strobe_interval=50, direction=1, reverse_colors=False):
        """
        Cop strobe effect with two modes:
        1. Alternating blue and red halves with strobe flicker.
        2. Flashing red on one half while blue is off on the other alternately, with configurable direction and color start.

        :param segment: The LED segment to control.
        :param alternate_interval: Time in milliseconds for alternating colors (red/blue).
        :param strobe_interval: Time in milliseconds for strobe flickering.
        :param direction: 1 for starting with red on the bottom half, 0 for starting with red on the upper half.
        :param reverse_colors: If True, starts with blue instead of red.
        """
        super().__init__(segment)
        self.alternate_interval = alternate_interval
        self.strobe_interval = strobe_interval
        self.direction = direction  # 1 for normal, 0 for reversed
        self.reverse_colors = reverse_colors  # If True, swaps starting colors
        self.effect_modes = {
            "cop": self.cop_strobe_fx,
            "flash": self.red_blue_flash_fx,
        }
        self.colors = {
            "blue": (0, 0, 255),
            "red": (255, 0, 0)
        }

    def _set_half_colors(self, bottom_color, upper_color, bottom_brightness=255, upper_brightness=255):
        """
        Set the bottom and upper halves of the segment to different colors and brightness levels.

        :param bottom_color: RGB color for the bottom half.
        :param upper_color: RGB color for the upper half.
        :param bottom_brightness: Brightness for the bottom half (0-255).
        :param upper_brightness: Brightness for the upper half (0-255).
        """
        segment_length = len(self.segment)
        half_length = segment_length // 2

        for i in range(segment_length):
            if i < half_length:  # Bottom half
                self.segment[i].rgb = bottom_color
                self.segment[i].brightness = bottom_brightness
            else:  # Upper half
                self.segment[i].rgb = upper_color
                self.segment[i].brightness = upper_brightness

    def cop_strobe_fx(self):
        """
        Alternates blue and red colors across segment halves with strobe flickering.
        """
        segment_length = len(self.segment)
        half_length = segment_length // 2

        is_blue_first = (np.floor(self.elapsed_time / self.alternate_interval) % 2 == 0)
        color1 = self.colors["blue"] if is_blue_first else self.colors["red"]
        color2 = self.colors["red"] if is_blue_first else self.colors["blue"]

        is_strobe_on = np.floor(self.elapsed_time / self.strobe_interval) % 2 == 0
        brightness = 255 if is_strobe_on else 0

        for i in range(segment_length):
            if i < half_length:
                self.segment[i].rgb = color1
            else:
                self.segment[i].rgb = color2
            self.segment[i].brightness = brightness

    def red_blue_flash_fx(self):
        """
        Flashes red on one half while blue is off on the other alternately, with configurable direction and color start.

        Sequence:
        - Default: Bottom half: Red flashes, Upper half: Off. Then: Bottom half: Off, Upper half: Blue flashes.
        - Reversed: Bottom half: Blue flashes, Upper half: Off. Then: Bottom half: Off, Upper half: Red flashes.
        """
        is_red_active = (np.floor(self.elapsed_time / self.alternate_interval) % 2 == 0)

        # Adjust colors based on reverse_colors parameter
        primary_color = self.colors["blue"] if self.reverse_colors else self.colors["red"]
        secondary_color = self.colors["red"] if self.reverse_colors else self.colors["blue"]

        if self.direction == 1:  # Default direction: primary color starts on the bottom half
            bottom_color = primary_color if is_red_active else (0, 0, 0)
            upper_color = (0, 0, 0) if is_red_active else secondary_color
        else:  # Reversed direction: primary color starts on the upper half
            bottom_color = (0, 0, 0) if is_red_active else secondary_color
            upper_color = primary_color if is_red_active else (0, 0, 0)

        # Strobe effect controls brightness
        is_strobe_on = np.floor(self.elapsed_time / self.strobe_interval) % 2 == 0
        bottom_brightness = 255 if is_strobe_on else 0
        upper_brightness = 255 if is_strobe_on else 0

        self._set_half_colors(bottom_color, upper_color, bottom_brightness, upper_brightness)