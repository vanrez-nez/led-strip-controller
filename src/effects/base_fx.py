from abc import ABC, abstractmethod

class BaseFx(ABC):
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

    def update(self, delta_ms):
        """
        Update the effect based on the elapsed time.

        Parameters:
        - delta_ms (float): Time elapsed since the last update in milliseconds.
        """
        self.delta = delta_ms
        self.elapsed_time += delta_ms
        self.apply_effect()

    @abstractmethod
    def apply_effect(self):
        """
        Define the specific effect logic.
        Must be implemented by subclasses.
        """
        pass