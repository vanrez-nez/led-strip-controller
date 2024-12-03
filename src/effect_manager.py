class EffectManager:
    def __init__(self, mode='manual_cycle', time_cycle_duration=30000):
        """
        Initialize the EffectManager.

        Parameters:
        - mode (str): The cycling mode ('manual_cycle', 'time_cycle', 'auto_cycle').
        - time_cycle_duration (int): Duration in milliseconds for time-based cycling.
        """
        self.effects = []
        self.current_index = 0
        self.current_effect = None
        self.mode = mode
        self.time_cycle_duration = time_cycle_duration  # in milliseconds
        self.time_since_last_switch = 0
        self.idle_level_threshold = 0.1  # Level considered idle
        self.idle_time_duration = 1000  # in milliseconds, time to consider before switching in auto_cycle
        self.idle_time = 0

    def add(self, effect):
        """
        Add an effect to the manager.

        Parameters:
        - effect (BaseFx): An instance of an effect implementing BaseFx.
        """
        self.effects.append(effect)
        if self.current_effect is None:
            self.current_effect = effect

    def next(self):
        """Switch to the next effect."""
        # if self.current_effect is not None:
            # self.current_effect.on_deactivate()
        self.current_index = (self.current_index + 1) % len(self.effects)
        self.current_effect = self.effects[self.current_index]
        # self.current_effect.on_activate()
        self.time_since_last_switch = 0

    def prev(self):
        """Switch to the previous effect."""
        # if self.current_effect is not None:
        #     self.current_effect.on_deactivate()
        self.current_index = (self.current_index - 1) % len(self.effects)
        self.current_effect = self.effects[self.current_index]
        # self.current_effect.on_activate()
        self.time_since_last_switch = 0

    def update(self, delta_ms, level):
        """
        Update the current effect and handle cycling logic.

        Parameters:
        - delta_ms (float): Time elapsed since the last update in milliseconds.
        - level (float): The current level (e.g., audio level).
        """
        if self.current_effect is None:
            return
        self.current_effect.update(delta_ms, level)
        self.time_since_last_switch += delta_ms
        print(self.time_since_last_switch)
        if self.mode == 'time_cycle':
            if self.time_since_last_switch >= self.time_cycle_duration:
                self.next()
        elif self.mode == 'auto_cycle':
            if level <= self.idle_level_threshold:
                self.idle_time += delta_ms
            else:
                self.idle_time = 0
            if (self.idle_time >= self.idle_time_duration and
                    self.time_since_last_switch >= self.time_cycle_duration):
                self.next()

    def list_effects(self):
        """List all effects and their configurations for debugging."""
        for idx, effect in enumerate(self.effects):
            active = ' (active)' if idx == self.current_index else ''
            effect_modes = ', '.join(effect.effect_modes.keys())
            current_mode = effect.mode
            print(f"{idx}: {effect.__class__.__name__} - Mode: {current_mode} "
                  f"(Available modes: {effect_modes}){active}")

    def set_mode(self, mode):
        """
        Set the cycling mode.

        Parameters:
        - mode (str): The cycling mode ('manual_cycle', 'time_cycle', 'auto_cycle').
        """
        if mode not in ['manual_cycle', 'time_cycle', 'auto_cycle']:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode