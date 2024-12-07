from base_fx import BaseFx
import random
from gradient import Gradient


class RandomFx(BaseFx):
    def __init__(self, segment, gradient: Gradient = None, px_size=1, threshold=0.25, scroll_speed=0.55):
        """
        Random effect lights up randomized subsegments based on the threshold level, with scrolling.

        :param segment: The LED segment to control.
        :param gradient: Gradient object to determine colors.
        :param px_size: Size of each subsegment in pixels.
        :param threshold: Activation threshold level (0-1).
        :param scroll_speed: Pixels to scroll per update (supports float values).
        """
        super().__init__(segment)
        self.gradient = gradient
        self.px_size = px_size
        self.threshold = threshold
        self.scroll_speed = scroll_speed
        self.scroll_offset = 0.0  # Tracks the current scroll position as a float
        self._decay = 0.7  # Brightness decay factor
        self._subsegment_states = [
            {"brightness": 0.0, "active": False, "t": random.random(), "flash": False}
            for _ in range(len(segment) // px_size)
        ]
        self.effect_modes = {"random": self.random_fx}

    def _set_subsegment(self, start, end, color, brightness):
        """
        Set the brightness and color for a subsegment.

        :param start: Starting pixel index of the subsegment.
        :param end: Ending pixel index of the subsegment.
        :param color: RGB color tuple.
        :param brightness: Brightness level (0-255).
        """
        for i in range(start, end):
            if 0 <= i < len(self.segment):  # Ensure within bounds
                self.segment[i].rgb = color
                self.segment[i].brightness = int(brightness)

    def random_fx(self):
        """
        Activates and decays subsegments based on the current level and threshold, with scrolling.
        """
        # Update the gradient to shift colors over time
        self.gradient.shift_color_group(self.elapsed_time * 0.0001)

        # Update the scroll offset (supports fractional values)
        self.scroll_offset += self.scroll_speed
        total_pixels = len(self.segment)
        self.scroll_offset %= total_pixels  # Ensure the offset loops around the strip

        # Adjust subsegment processing for the scroll effect
        total_subsegments = len(self._subsegment_states)
        for i, state in enumerate(self._subsegment_states):
            # Calculate the scrolled subsegment index (adjusting for fractional scroll offset)
            scrolled_start = (i * self.px_size + int(self.scroll_offset)) % total_pixels
            scrolled_end = scrolled_start + self.px_size

            # Free the subsegment if it is out of bounds
            if scrolled_start >= total_pixels or scrolled_end < 0:
                state["active"] = False
                continue

            # Update existing subsegment brightness
            if state["active"]:
                state["brightness"] *= self._decay
                if state["brightness"] < 1:  # Fully faded out
                    state["brightness"] = 0.0
                    state["active"] = False
                    state["flash"] = False

            # Activate new subsegments based on threshold and random chance
            if not state["active"] and self.level > self.threshold and random.random() > 0.7:
                if random.random() < self.level:  # Higher level = higher chance
                    state["brightness"] = 255
                    state["active"] = True
                    state["t"] = random.random()  # Assign a new random gradient position
                    state["flash"] = self.level > 0.85  # Flash white on activation

            # Determine the color
            if state["flash"]:
                color = (255, 255, 255)  # Flash white
                state["flash"] = False  # Flash only for one frame
            else:
                color = self.gradient.get_color(state["t"]) if state["active"] else (0, 0, 0)

            # Apply brightness and color to the subsegment
            self._set_subsegment(scrolled_start, scrolled_end, color, state["brightness"])