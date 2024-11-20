import numpy as np
from pixel import Pixel

class Segment:
    def __init__(self, strip, start, end, direction=1):
        if end - start > len(strip):
            raise ValueError("Segment range exceeds strip length.")
        self.strip = strip
        self.start = start
        self.end = end
        self.data = strip.data[start:end]
        self.direction = direction

    def __len__(self):
        return len(self.data)
