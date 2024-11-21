import numpy as np
import math

class SignalGenerator:
    def __init__(self, peak_time=2.0, duration=5.0, amplitude=1.0, frequency=1.0):
        """
        Initialize the SignalGenerator.

        Args:
            peak_time (float): The time at which the signal reaches its peak value.
            duration (float): The duration of the signal (controls spread).
            amplitude (float): The maximum amplitude of the signal.
            frequency (float): The frequency of the periodic signal.
        """
        self.peak_time = peak_time
        self.duration = duration
        self.amplitude = amplitude
        self.frequency = frequency
        self.level = 0.0

    def update(self, elapsed_time_ms):
        """
        Update the level of the signal based on the elapsed time.

        Args:
            elapsed_time_ms (float): The time that has elapsed, in milliseconds.
        """
        # Convert elapsed time from milliseconds to seconds
        elapsed_time = elapsed_time_ms / 1000.0

        # Calculate the periodic Gaussian-like signal value
        gaussian = math.exp(-((elapsed_time % (1 / self.frequency) - self.peak_time) ** 2) / (2 * self.duration ** 2))
        oscillation = (math.sin(2 * math.pi * self.frequency * elapsed_time) + 1) * 0.5
        self.level = self.amplitude * gaussian * oscillation

    def get_level(self):
        """
        Get the current level of the signal.

        Returns:
            float: The current level of the signal.
        """
        return self.level

# Example usage
if __name__ == "__main__":
    signal = SignalGenerator(peak_time=1, duration=0.1, amplitude=1.0, frequency=0.5)
    total_time_ms = 10000  # Total time in milliseconds
    fps = 60  # Frames per second
    num_samples = int(total_time_ms / 1000.0 * fps)  # Number of samples for 60 fps
    time_values = np.linspace(0, total_time_ms, num_samples)  # Time values in milliseconds
    levels = []

    for t in time_values:
        signal.update(t)
        levels.append(signal.get_level())

    # Plotting the signal to visualize
    import matplotlib.pyplot as plt
    plt.plot(time_values, levels, 'r')
    plt.xlabel('Time (ms)')
    plt.ylabel('Level')
    plt.title('Generated Signal')
    plt.show()
