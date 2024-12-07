from pixel import Pixel

class MultiSegment:
    def __init__(self, mode="mirror"):
        """
        mode: "mirror" or "add"
          - "mirror": all segments must have the same length. Indexing one index updates all segments at that index.
          - "add": segments are concatenated end-to-end, forming a longer virtual segment.
        """
        if mode not in ("mirror", "add"):
            raise ValueError("Mode must be 'mirror' or 'add'.")

        self.mode = mode
        self.segments = []
        self._length = 0
        self._initialized = False

        # For "mirror" mode:
        self._segment_length = None

        # For "add" mode:
        self.cumulative_lengths = []  # Tracks the end index of each segment in the combined array

    def addSegment(self, segment):
        if self.mode == "mirror":
            if self._segment_length is None:
                self._segment_length = len(segment)
            else:
                if len(segment) != self._segment_length:
                    raise ValueError("All segments in 'mirror' mode must have the same length.")
            # Length is just the length of one segment in mirror mode
            self._length = self._segment_length
            self.segments.append(segment)

        elif self.mode == "add":
            # Just append and sum lengths
            self.segments.append(segment)
            self._length += len(segment)
            self.cumulative_lengths.append(self._length)

    def clear(self):
        for seg in self.segments:
            seg.clear()

    def __len__(self):
        return self._length

    def __getitem__(self, index):
        if not 0 <= index < self._length:
            raise IndexError("MultiSegment index out of range.")

        if self.mode == "mirror":
            # mirror: same index on all segments
            pixels = [seg[index] for seg in self.segments]
            return self._MultiPixel(pixels)

        elif self.mode == "add":
            # add: find which segment this index falls into
            # Use cumulative_lengths to find the segment
            # cumulative_lengths is sorted by definition
            # Example: segments: len=30, len=30 => cumulative_lengths=[30,60]
            # index=0 => falls in segment 0
            # index=30 => falls in segment 1 (index-30=0 within that segment)
            seg_idx = self._find_segment(index)
            seg_start = self.cumulative_lengths[seg_idx-1] if seg_idx > 0 else 0
            pixel_index = index - seg_start
            pixel = self.segments[seg_idx][pixel_index]
            return self._MultiPixel([pixel])

    def _find_segment(self, idx):
        # Binary search could be used, but linear is fine for small N.
        # For large N, consider bisect. Here we just do a simple loop.
        for i, cum_len in enumerate(self.cumulative_lengths):
            if idx < cum_len:
                return i
        # Should never reach here if indexing is correct
        raise IndexError("Index out of range in cumulative length search.")

    class _MultiPixel:
        def __init__(self, pixels):
            self.pixels = pixels

        @property
        def rgb(self):
            return self.pixels[0].rgb

        @rgb.setter
        def rgb(self, value):
            for p in self.pixels:
                p.rgb = value

        @property
        def brightness(self):
            return self.pixels[0].brightness

        @brightness.setter
        def brightness(self, val):
            for p in self.pixels:
                p.brightness = val

        def copy(self, other_pixel):
            rgb = other_pixel.rgb
            brightness = other_pixel.brightness
            for p in self.pixels:
                p.rgb = rgb
                p.brightness = brightness