class EffectManager:
    def __init__(self, mode='manual_cycle', time_cycle_duration=30000):
        """
        Initialize the EffectManager.

        Parameters:
        - mode (str): The cycling mode ('manual_cycle', 'time_cycle', 'auto_cycle').
        - time_cycle_duration (int): Duration in milliseconds for time-based cycling.
        """
        # Now 'effects' is a list of groups, where each group is a list of effects.
        self.effects = []
        self.current_index = 0
        self.current_group = None
        self.mode = mode
        self.time_cycle_duration = time_cycle_duration  # in milliseconds
        self.time_since_last_switch = 0
        self.idle_level_threshold = 0.1  # Level considered idle
        self.idle_time_duration = 1000  # in milliseconds, time to consider before switching in auto_cycle
        self.idle_time = 0

    def add(self, new_effects):
        """
        Add effect(s) to the manager.

        Parameters:
        - new_effects (BaseFx or list of BaseFx): Either a single effect instance
          or a list of effect instances to be treated as a group.
        """
        if not isinstance(new_effects, list):
            # Wrap single effect into a list to form a single group
            new_effects = [new_effects]

        self.effects.append(new_effects)
        if self.current_group is None:
            self.current_group = new_effects

    def next(self):
        """Switch to the next group of effects."""
        self.current_index = (self.current_index + 1) % len(self.effects)
        self.current_group = self.effects[self.current_index]
        self.time_since_last_switch = 0

    def prev(self):
        """Switch to the previous group of effects."""
        self.current_index = (self.current_index - 1) % len(self.effects)
        self.current_group = self.effects[self.current_index]
        self.time_since_last_switch = 0

    def update(self, delta_ms, level):
        """
        Update the current group of effects and handle cycling logic.

        Parameters:
        - delta_ms (float): Time elapsed since the last update in milliseconds.
        - level (float): The current level (e.g., audio level).
        """
        if self.current_group is None:
            return

        # Update all effects in the current group
        for effect in self.current_group:
            effect.update(delta_ms, level)

        self.time_since_last_switch += delta_ms

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

    def clear(self):
        """Clear all effect groups."""
        self.effects = []
        self.current_index = 0
        self.current_group = None

    def list_effects(self):
        """List all effect groups and their configurations for debugging."""
        for idx, group in enumerate(self.effects):
            active = ' (active)' if idx == self.current_index else ''
            print(f"Group {idx}{active}:")
            for eff in group:
                effect_modes = ', '.join(eff.effect_modes.keys()) if hasattr(eff, 'effect_modes') else 'N/A'
                current_mode = eff.mode if hasattr(eff, 'mode') else 'N/A'
                print(f"  - {eff.__class__.__name__} - Mode: {current_mode} (Available modes: {effect_modes})")

    def set_mode(self, mode):
        """
        Set the cycling mode.

        Parameters:
        - mode (str): The cycling mode ('manual_cycle', 'time_cycle', 'auto_cycle').
        """
        if mode not in ['manual_cycle', 'time_cycle', 'auto_cycle']:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode