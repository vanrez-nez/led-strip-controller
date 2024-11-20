import numpy as np

class Strip:
    def __init__(self, num_leds):
        # Initialize strip data with zeros
        # Each LED has 4 components: R, G, B, Brightness
        self.data = np.zeros((num_leds, 4), dtype=np.uint8)

    def __len__(self):
        return len(self.data)
