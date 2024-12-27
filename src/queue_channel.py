from multiprocessing import Queue
from typing import Callable, Dict, Any

class QueueChannel:
    def __init__(self):
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.handlers: Dict[str, Callable] = {}

    def on(self, event: str, callback: Callable):
        """Register a callback for a specific event"""
        self.handlers[event] = callback

    def send(self, event: str, data: Any = None):
        """Send an event with optional data"""
        try:
            self.input_queue.put_nowait((event, data))
        except:
            pass

    def respond(self, data: Any):
        """Send response back through output queue"""
        try:
            self.output_queue.put_nowait(data)
        except:
            pass

    def receive(self):
        """Receive response from output queue"""
        try:
            return self.output_queue.get_nowait()
        except:
            return None

    def process_events(self):
        """Process all pending events in the queue"""
        try:
            while True:
                event, data = self.input_queue.get_nowait()
                if event in self.handlers:
                    self.handlers[event](data)
        except:
            pass