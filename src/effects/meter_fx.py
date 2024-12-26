from base_fx import BaseFx
import numpy as np
from gradient import Gradient
from color import lerp as lerp_color
from color import multiply as multiply_color
import easing

class MeterFx(BaseFx):
    def __init__(self, segment, gradient: Gradient = None):
        super().__init__(segment)
        self.gradient = gradient
        self.decay = 0.85
        self.peak_decay = 0.98
        self.last_level = 0.0
        self.show_peak = True
        self.ghost_decay = 0.65
        self.peak_heat = 0.0
        self.peak_heat_decay = 0.9
        self.last_peak = 0
        self.effect_modes = {
            "from_bottom": self.meter_fx,
            "center": self.meter_center_fx,
            "sides": self.meter_sides_fx,
        }

    def update_decay(self):
        # Apply easing decay to last_level
        self.last_level *= self.decay
        if self.level > self.last_level:
            self.last_level = self.level

        # Apply easing decay to last_peak
        self.last_peak *= np.clip(easing.easeOutSine(self.last_peak * self.peak_decay), 0.95, 1)
        self.peak_heat *= np.clip(easing.easeOutSine(self.peak_heat * self.peak_heat_decay), 0.92, 1)
        if self.last_level > self.last_peak:
            self.last_peak = self.last_level
            self.peak_heat = 1

    def meter_fx(self):
        self.update_decay()
        peak_idx = int(self.last_peak * len(self.segment))
        for idx, pixel in enumerate(self.segment):
            i = self.last_level * len(self.segment)
            if (idx == peak_idx) and self.show_peak:
                pixel.rgb = lerp_color(self.gradient.get_color(self.last_peak), (255, 250, 250), self.peak_heat)
                pixel.brightness = 255
            elif i >= idx:
                color_pos = (idx + 1) / len(self.segment)
                color = self.gradient.get_color(color_pos)
                pixel.rgb = color
                pixel.brightness = 255
            else:
                pixel.brightness *= self.ghost_decay

    def meter_center_fx(self):
        self.update_decay()
        segment_length = len(self.segment)
        center = segment_length // 2

        # Compute mirrored level
        level_position = int(self.last_level * center)

        # Update pixels from center to both sides
        for idx in range(center):
            color = (0, 0, 0)
            if idx <= level_position:
                color_pos = (idx + 1) / center
                brightness = 255
                color = self.gradient.get_color(color_pos)

            # Left side
            left_pixel = self.segment[center - idx - 1]
            if level_position <= idx:
                left_pixel.brightness *= self.ghost_decay
            else:
                left_pixel.rgb = color
                left_pixel.brightness = brightness

            #Right side
            right_pixel = self.segment[center + idx]
            right_pixel.copy(left_pixel)

        # Show peak if enabled
        if self.show_peak:
            peak_position = np.clip(int(self.last_peak * center), 0, center - 1)
            peak_color = lerp_color(self.gradient.get_color(self.last_peak), (255, 250, 250), self.peak_heat)

            # Left peak
            left_peak_pixel = self.segment[center - peak_position - 1]
            if self.peak_heat > 0.01:
                left_peak_pixel.brightness = 255
            else:
                left_peak_pixel.brightness *= 0.995
            left_peak_pixel.rgb = peak_color

            # Right peak
            right_peak_pixel = self.segment[center + peak_position]
            right_peak_pixel.copy(left_peak_pixel)

    def meter_sides_fx(self):
        self.update_decay()
        segment_length = len(self.segment)
        center = segment_length // 2
        # Compute mirrored level from sides towards center
        level_position = int(self.last_level * center)

        # Update pixels from sides to the center
        for idx in range(center):
            color = (0, 0, 0)
            if idx <= level_position:
                color_pos = (idx + 1) / center
                brightness = 255
                color = self.gradient.get_color(color_pos)

            # Left side towards center
            left_pixel = self.segment[idx]
            if level_position <= idx:
                left_pixel.brightness *= self.ghost_decay
            else:
                left_pixel.rgb = color
                left_pixel.brightness = brightness

            # Right side towards center
            right_pixel = self.segment[segment_length - idx - 1]
            right_pixel.copy(left_pixel)

        # Show peak if enabled
        if self.show_peak:
            peak_position = int(self.last_peak * center)
            peak_color = lerp_color(self.gradient.get_color(self.last_peak), (255, 250, 250), self.peak_heat)

            # Left peak
            left_peak_pixel = self.segment[peak_position]
            if self.peak_heat > 0.01:
                left_peak_pixel.brightness = 255
            else:
                left_peak_pixel.brightness *= 0.995
            left_peak_pixel.rgb = peak_color

            # Right peak
            right_peak_pixel = self.segment[segment_length - peak_position - 1]
            right_peak_pixel.copy(left_peak_pixel)
