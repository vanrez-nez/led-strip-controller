class EffectManager:
    def __init__(self, mode='manual_cycle', time_cycle_duration=30000):
        """
        Initialize the EffectManager.

        Parameters:
        - mode (str): The cycling mode ('manual_cycle', 'time_cycle', 'auto_cycle').
        - time_cycle_duration (int): Duration in milliseconds for time-based cycling.
        """
        self.effects = {}  # Dictionary with group names as keys and group data as values
        self.current_index = 0
        self.current_group = None
        self.cycle_groups = []  # List of group names currently active in the cycle
        self.mode = mode
        self.time_cycle_duration = time_cycle_duration  # in milliseconds
        self.cycle_timeout_duration = time_cycle_duration * 2
        self.time_since_last_switch = 0
        self.idle_level_threshold = 0.1  # Level considered idle
        self.idle_time_duration = 1000  # in milliseconds, time to consider before switching in auto_cycle
        self.idle_time = 0

    def add(self, name, new_effects):
        """
        Add effect(s) to the manager with a name.

        Parameters:
        - name (str): Name of the group being added.
        - new_effects (BaseFx or list of BaseFx): A single effect or a list of effects.
        """
        if not isinstance(new_effects, list):
            new_effects = [new_effects]

        self.effects[name] = {"effects": new_effects, "enabled": True}
        if self.current_group is None:
            self.current_group = self.effects[name]
        if name not in self.cycle_groups:
            self.cycle_groups.append(name)

    def set_current(self, name):
        """
        Set the current group by name.

        Parameters:
        - name (str): The name of the group to set as current.
        """
        if name not in self.effects:
            raise ValueError(f"Group '{name}' not found.")

        self.current_index = self.cycle_groups.index(name) if name in self.cycle_groups else 0
        self.current_group = self.effects[name]
        self.time_since_last_switch = 0

    def list_effects(self):
        """
        List all effect groups and their configurations.

        Returns:
        - list: A list of dictionaries representing group states.
        """
        return [
            {
                "name": group_name,
                "enabled": group_data["enabled"],
                "current": (self.current_group == group_data)
            }
            for group_name, group_data in self.effects.items()
        ]

    def set_config(self, config_array):
        """
        Configure active groups and their enabled states for cycling.

        Parameters:
        - config_array (list of dict): List of dictionaries with 'name' and 'enabled' keys
                                    Example: [{'name': 'scroll', 'enabled': True}, ...]
        """
        # Update enabled states in effects dictionary
        for config in config_array:
            name = config['name']
            if name in self.effects:
                self.effects[name]['enabled'] = config['enabled']

        # Update cycle groups to only include enabled effects
        self.cycle_groups = [
            name for name in self.effects
            if name in [cfg['name'] for cfg in config_array]
            and self.effects[name]['enabled']
        ]

        if not self.cycle_groups:
            raise ValueError("At least one group must be active.")

        # Reset current if it's not in the enabled groups
        if self.current_group and self.current_group not in [
            self.effects[name] for name in self.cycle_groups
        ]:
            self.current_index = 0
            self.current_group = self.effects[self.cycle_groups[0]]

    def next(self):
        """Switch to the next group of effects."""
        if not self.cycle_groups:
            return
        self.current_index = (self.current_index + 1) % len(self.cycle_groups)
        self.current_group = self.effects[self.cycle_groups[self.current_index]]
        self.time_since_last_switch = 0

    def prev(self):
        """Switch to the previous group of effects."""
        if not self.cycle_groups:
            return
        self.current_index = (self.current_index - 1) % len(self.cycle_groups)
        self.current_group = self.effects[self.cycle_groups[self.current_index]]
        self.time_since_last_switch = 0

    def update(self, delta_ms, level):
        """
        Update the current group of effects and handle cycling logic.

        Parameters:
        - delta_ms (float): Time elapsed since the last update in milliseconds.
        - level (float): The current level (e.g., audio level).
        """
        if not self.current_group or not self.cycle_groups:
            return

        # Update all effects in the current group
        for effect in self.current_group["effects"]:
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
                    self.time_since_last_switch >= self.time_cycle_duration or
                    self.time_since_last_switch > self.cycle_timeout_duration):
                self.next()

    def clear(self):
        """Clear all effect groups."""
        self.effects = {}
        self.current_index = 0
        self.current_group = None
        self.cycle_groups = []