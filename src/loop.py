from time import perf_counter

class Loop:
    def __init__(self):
        self.last_time = perf_counter() * 1000
        self.elapsed_time = 0.0
        self.delta = 0.0

    def update(self):
        current_time = perf_counter() * 1000
        self.delta = current_time - self.last_time
        self.elapsed_time += self.delta
        self.last_time = current_time