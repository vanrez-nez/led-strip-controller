from base_fx import BaseFx
import numpy as np
import random;
from gradient import Gradient


class ScrollFx(BaseFx):
    def __init__(self, segment, gradient: Gradient = None, level_threshold=0.2, lit_background=False, speed=0.85):
        """
        Scrolling effect where LEDs originate at the center and scroll outward symmetrically,
        reactive to the level.

        :param segment: The LED segment to control.
        :param gradient: Gradient object to determine colors.
        :param level_threshold: Minimum level required to trigger a new pixel emission.
        :param lit_background: If True, the background will remain lit.
        :param speed: Scrolling speed as a float (supports fractional values).
        """
        super().__init__(segment)
        self.gradient = gradient
        self.level_threshold = level_threshold
        self.lit_background = lit_background
        self.speed = speed
        self.decay = 0.95  # Default decay for fading pixels
        self.scroll_states = []  # Tracks active scrolling pixels
        self.effect_modes = {
            "scroll_center": self.scroll_fx,
        }

    def clear_background(self):
        """
        Clears the background by setting all pixels to off unless lit_background is True.
        """
        if not self.lit_background:
            for pixel in self.segment:
                pixel.rgb = (0, 0, 0)
                pixel.brightness = 0

    def scroll_fx(self):
        """
        Creates a scrolling effect where LEDs originate at the center and scroll outward symmetrically.
        """
        # Compute `t` value for color cycling (0 to 1 based on elapsed time)
        t = (self.elapsed_time * 0.0001) % 1.0
        self.gradient.shift_color_group(self.elapsed_time * 0.0001)
        self.clear_background()
        segment_length = len(self.segment)
        center = segment_length // 2

        # Emit a new pixel if the level exceeds the threshold
        if self.level > self.level_threshold:
            self.scroll_states.append({
                "offset": 0.0,
                "color": self.gradient.get_color(random.random()),
                "brightness": 255,
                "flash": self.level > 0.85  # Flash state for newly spawned pixel
            })

        # Process each active scrolling pixel
        for state in list(self.scroll_states):  # Copy the list to allow safe modification
            offset = state["offset"]
            color = state["color"]
            brightness = state["brightness"]

            # Handle flash
            if state["flash"]:
                current_color = (255, 255, 255)  # Quick white flash
                state["flash"] = False  # Flash only for one frame
            else:
                current_color = color

            # Update left and right pixels
            left_index = int(center - offset)
            right_index = int(center + offset)

            if 0 <= left_index < segment_length:
                self.segment[left_index].rgb = current_color
                self.segment[left_index].brightness = brightness
            if 0 <= right_index < segment_length:
                self.segment[right_index].rgb = current_color
                self.segment[right_index].brightness = brightness

            # Apply fading with decay
            state["brightness"] *= self.decay

            # Increment the offset to scroll outward based on speed
            state["offset"] += self.speed

            # Remove pixel if it has scrolled out of bounds or faded out
            if (left_index < 0 and right_index >= segment_length) or state["brightness"] < 1:
                self.scroll_states.remove(state)