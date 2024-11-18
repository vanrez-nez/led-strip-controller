import numpy as np
from pixel import Pixel

class Segment:
    def __init__(self, strip):
        self.strip = strip
        self.indices = np.array([], dtype=int)  # Mapping from segment positions to strip indices

    def map_range(self, start, length, led_pos):
        """
        Map a range of LEDs from the strip to the segment.

        Parameters:
        - start: Starting position in the segment.
        - length: Number of LEDs to map.
        - led_pos: Starting position in the strip.
        """
        # Ensure the indices array is large enough
        end = start + length
        if end > len(self.indices):
            # Expand the indices array
            new_size = end
            new_indices = np.full(new_size, -1, dtype=int)  # Initialize with -1
            new_indices[:len(self.indices)] = self.indices
            self.indices = new_indices

        # Map the range
        self.indices[start:end] = np.arange(led_pos, led_pos + length)

    @property
    def data(self):
        # Return a view into the strip data using fancy indexing
        return self.strip.data[self.indices]

    def __getitem__(self, idx):
        strip_idx = self.indices[idx]
        if strip_idx == -1:
            raise IndexError("Segment index not mapped to any strip index.")
        return Pixel(self.strip, strip_idx)

    def __len__(self):
        return len(self.indices)
