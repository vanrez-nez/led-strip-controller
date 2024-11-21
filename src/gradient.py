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
    def __init__(self, resolution: int = 1000, colors: List[GradientColor] = []):
        """
        Initialize the Gradient.

        Parameters:
        - resolution (int): Number of discrete steps between 0 and 1.
                            Higher resolution means smoother gradients but
                            increases memory usage.
        """
        self.colors: List[GradientColor] = []
        self.cache: Dict[int, Tuple[float, float, float]] = {}
        self.resolution = resolution
        for color in colors:
            self.add_color(color.r, color.g, color.b, color.position)

    def add_color(self, r: float, g: float, b: float, position: float):
        """
        Add a gradient stop.

        Parameters:
        - r, g, b, a (float): Color components.
        - position (float): Position in the gradient (0 to 1).
        """
        self.colors.append(GradientColor(r, g, b, position))
        # Keep colors sorted by position after each addition
        self.colors.sort(key=lambda color: color.position)

    def lerp(self, start: GradientColor, end: GradientColor, t: float) -> Tuple[float, float, float]:
        r = start.r + (end.r - start.r) * t
        g = start.g + (end.g - start.g) * t
        b = start.b + (end.b - start.b) * t
        return (r, g, b)

    def precompute(self):
        # Initialize the cache
        self.cache = {}
        if not self.colors:
            return

        # Iterate through each discrete step
        for step in range(self.resolution + 1):
            position = step / self.resolution
            color = self._interpolate_position(position)
            self.cache[step] = color

    def _interpolate_position(self, position: float) -> Tuple[float, float, float]:
        position = np.clip(position, 0.0, 1.0)
        # Find the interval [left, right] where left.position <= position < right.position
        left = self.colors[0]
        right = self.colors[-1]
        for i in range(1, len(self.colors)):
            if position < self.colors[i].position:
                left = self.colors[i - 1]
                right = self.colors[i]
                break

        # Compute interpolation factor
        interval = right.position - left.position
        if interval == 0:
            t = 0
        else:
            t = (position - left.position) / interval

        # Perform linear interpolation
        return self.lerp(left, right, t)

    def get_color(self, position: float) -> Tuple[float, float, float]:
        if not self.cache:
            self.precompute()

        # Clamp position to [0, 1]
        position = np.clip(position, 0.0, 1.0)
        step = int(position * self.resolution)
        step = min(step, self.resolution)
        # Retrieve the color from the cache
        # Default to transparent black if not found
        return self.cache.get(step, (0, 0, 0))