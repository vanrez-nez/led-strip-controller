from time import perf_counter

class Loop:
    def __init__(self, mode="per_frame", avg_interval=1.0):
        """
        mode: "per_frame" for instantaneous FPS per frame, "avg" for average FPS over a specified interval.
        avg_interval: Interval in seconds over which to average FPS, only used if mode="avg".
        """
        self.mode = mode
        self.avg_interval_ms = avg_interval * 1000.0

        self.last_time = perf_counter() * 1000
        self.elapsed_time = 0.0
        self.delta = 0.0

        # For averaging
        self.accum_time = 0.0
        self.frame_count = 0

    def update(self):
        current_time = perf_counter() * 1000
        self.delta = current_time - self.last_time
        self.elapsed_time += self.delta
        self.last_time = current_time

        self.frame_count += 1
        self.accum_time += self.delta

    def print_fps(self):
        if self.mode == "per_frame":
            # Print instantaneous FPS
            fps = 1000.0 / self.delta if self.delta > 0 else float('inf')
            print(f"FPS: {fps:.2f}")
        elif self.mode == "avg":
            # Only print after the averaging interval has passed
            if self.accum_time >= self.avg_interval_ms:
                avg_fps = (self.frame_count / (self.accum_time / 1000.0))
                print(f"Avg FPS: {avg_fps:.2f}")

                # Reset accumulators
                self.frame_count = 0
                self.accum_time = 0.0
        else:
            raise ValueError("Invalid mode. Use 'per_frame' or 'avg'.")