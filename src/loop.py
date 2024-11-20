import time

class Loop:
    def __init__(self, callback, fps=60):
        """
        Initialize the Loop.

        Parameters:
        - callback (function): The function to call on each frame.
                                It should accept two parameters: delta_ms and elapsed_ms.
        - fps (int): Frames per second. Default is 60.
        """
        self.callback = callback
        self.fps = fps
        self.interval = 1.0 / self.fps  # Interval in seconds
        self.running = False
        self.elapsed_time = 0.0  # Total elapsed time in milliseconds

    def start(self):
        """Start the loop in a separate thread."""
        if not self.running:
            self.running = True
            print("[Loop] Started.")

    def stop(self):
        """Stop the loop."""
        self.running = False
        print("[Loop] Stopped.")

    def update(self):
        """Internal method that runs the loop."""
        if not self.running:
            return
        previous_time = time.perf_counter()
        current_time = time.perf_counter()
        delta_time = (current_time - previous_time) * 1000.0
        previous_time = current_time
        self.elapsed_time += delta_time
        try:
            self.callback(delta_ms=delta_time, elapsed_ms=self.elapsed_time)
        except Exception as e:
            print(f"[Loop] Error in callback: {e}")