import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class GradientColor:
    r: float
    g: float
    b: float
    position: float

class Gradient:
    def __init__(self, resolution: int = 1000, colors: List[GradientColor] = None):
        """
        Initialize the Gradient.

        Parameters:
        - resolution (int): Number of discrete steps between 0 and 1.
                            Higher resolution means smoother gradients but
                            increases memory usage.
        - colors (List[GradientColor]): Initial list of colors for the first group.
        """
        if colors is None:
            colors = []

        self.resolution = resolution
        # groups is a list of lists. Each element is a group (a list of GradientColor)
        self.groups: List[List[GradientColor]] = []
        self.group_caches: List[Dict[int, Tuple[float, float, float]]] = []

        # Internal shift value
        self._shift = 0.0

        if colors:
            self.add_color_group(colors)

    def add_color_group(self, colors: List[GradientColor]):
        """
        Add a full group of colors (one gradient definition).
        The group is stored, sorted by position, and a cache is precomputed.
        """
        # Sort the colors by their position
        sorted_colors = sorted(colors, key=lambda c: c.position)
        self.groups.append(sorted_colors)
        # Precompute the cache for this new group
        cache = self._precompute_group(sorted_colors)
        self.group_caches.append(cache)

    def _precompute_group(self, colors: List[GradientColor]) -> Dict[int, Tuple[float, float, float]]:
        """
        Precompute the color lookup table for a single group.
        """
        cache = {}
        if not colors:
            return cache

        for step in range(self.resolution + 1):
            position = step / self.resolution
            color = self._interpolate_position(position, colors)
            cache[step] = color
        return cache

    def add_color(self, r: float, g: float, b: float, position: float, group_index: int = 0):
        """
        Add a gradient stop to an existing group.

        Parameters:
        - r, g, b (float): Color components.
        - position (float): Position in the gradient (0 to 1).
        - group_index (int): Which group to add this color to.
        """
        if group_index < 0 or group_index >= len(self.groups):
            raise ValueError(f"Group index {group_index} out of range.")

        self.groups[group_index].append(GradientColor(r, g, b, position))
        self.groups[group_index].sort(key=lambda color: color.position)
        # Recompute that group's cache since we've modified it
        self.group_caches[group_index] = self._precompute_group(self.groups[group_index])

    def shift_color_group(self, n: float):
        """
        Set the "shift" that determines how we interpolate between groups.

        0 means fully the first group,
        0.5 means halfway between the first and second group,
        1 means fully the second group, etc.

        If we have N groups, we take n mod N to find which two groups to interpolate between.
        """
        self._shift = n

    def lerp(self, start: GradientColor, end: GradientColor, t: float) -> Tuple[float, float, float]:
        r = start.r + (end.r - start.r) * t
        g = start.g + (end.g - start.g) * t
        b = start.b + (end.b - start.b) * t
        return (r, g, b)

    def _interpolate_position(self, position: float, colors: List[GradientColor]) -> Tuple[float, float, float]:
        position = np.clip(position, 0.0, 1.0)
        # If there's only one color, just return it
        if len(colors) == 1:
            c = colors[0]
            return (c.r, c.g, c.b)

        # Find the interval [left, right] where left.position <= position < right.position
        left = colors[0]
        right = colors[-1]
        for i in range(1, len(colors)):
            if position < colors[i].position:
                left = colors[i - 1]
                right = colors[i]
                break

        # Compute interpolation factor
        interval = right.position - left.position
        t = 0.0 if interval == 0 else (position - left.position) / interval

        # Perform linear interpolation
        return self.lerp(left, right, t)

    def get_color_from_group(self, group_index: int, position: float) -> Tuple[float, float, float]:
        """
        Retrieve the color from a specific group's precomputed cache at a given position.
        """
        # Clamp position to [0, 1]
        position = np.clip(position, 0.0, 1.0)
        step = int(position * self.resolution)
        step = min(step, self.resolution)
        # Default to black if not found
        return self.group_caches[group_index].get(step, (0,0,0))

    def get_color(self, position: float) -> Tuple[float, float, float]:
        """
        Get the interpolated color considering both the position in the gradient (t)
        and the currently set group shift.
        """
        if not self.groups:
            return (0, 0, 0)

        num_groups = len(self.groups)
        if num_groups == 1:
            # If there's only one group, just get its color
            return self.get_color_from_group(0, position)

        # Determine which two groups we are interpolating between
        # shift mod num_groups gives a continuous index into the circular group array.
        s = self._shift % num_groups
        left_group_index = int(np.floor(s)) % num_groups
        right_group_index = (left_group_index + 1) % num_groups
        group_t = s - np.floor(s)  # fractional part for interpolation between groups

        # Get colors from both groups
        c_left = self.get_color_from_group(left_group_index, position)
        c_right = self.get_color_from_group(right_group_index, position)

        # Interpolate between these two group colors
        r = c_left[0] + (c_right[0] - c_left[0]) * group_t
        g = c_left[1] + (c_right[1] - c_left[1]) * group_t
        b = c_left[2] + (c_right[2] - c_left[2]) * group_t

        return (r, g, b)