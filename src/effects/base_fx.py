class BaseFx():
    def __init__(self, segment):
        """
        Initialize the StripFxBase with a given Segment instance.

        Parameters:
        - segment (Segment): The LED strip to apply effects to.
        """
        super().__init__()
        self.segment = segment
        self.elapsed_time = 0.0
        self.delta = 0.0
        self.signal_level = 0.0
        self.mode = "default"
        self.effect_modes = {}

    def set_mode(self, mode):
        if mode not in self.effect_modes:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode

    def update(self, delta_ms, signal_level = 0):
        """
        Update the effect based on the elapsed time.

        Parameters:
        - delta_ms (float): Time elapsed since the last update in milliseconds.
        """
        self.signal_level = signal_level
        self.delta = delta_ms
        self.elapsed_time += delta_ms
        self.apply_effect()

    def apply_effect(self):
        if self.mode == "default" and self.effect_modes:
            self.effect_modes[next(iter(self.effect_modes))]()
        elif self.mode in self.effect_modes:
            self.effect_modes[self.mode]()