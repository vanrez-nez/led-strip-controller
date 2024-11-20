import numpy as np
from pixel import Pixel

class Segment:
    def __init__(self, strip, start, end, direction=1):
        if end - start > len(strip):
            raise ValueError("Segment range exceeds strip length.")
        self.strip = strip
        self.start = start
        self.end = end
        self.direction = direction

    def clear(self):
        """Clear the segment data."""
        self.strip.data[self.start:self.end] = 0

    def __len__(self):
        return abs(self.end - self.start)

    def __iter__(self):
        if self.direction >= 0:
            indices = range(self.start, self.end)
        else:
            indices = range(self.end - 1, self.start - 1, -1)
        for i in indices:
            yield Pixel(self.strip, i)

    def __getitem__(self, index):
        if not 0 <= index < len(self):
            raise IndexError("Segment index out of range.")
        if self.direction >= 0:
            actual_index = self.start + index
        else:
            actual_index = self.end - 1 - index
        return Pixel(self.strip, actual_index)
