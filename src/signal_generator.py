import numpy as np
import math

class SignalGenerator:
    def __init__(self, frequency=1.0, shape=1.0):
        self.shape = shape
        self.frequency = frequency
        self.level = 0.0

    def update(self, elapsed_time_ms):
        # Calculate the full cycle length based on frequency
        wave_length = (2 * math.pi) / self.frequency
        phase = (elapsed_time_ms / 1000) % wave_length

        # Calculate sine value and adjust shape using power function
        sine_value = math.sin((phase / wave_length) * math.pi)
        self.level = sine_value ** self.shape  # Use shape parameter to control the curve shape

    def get_level(self):
        return self.level

# Example usage
if __name__ == "__main__":
    signal = SignalGenerator(frequency=2.0, shape=10.0)
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
