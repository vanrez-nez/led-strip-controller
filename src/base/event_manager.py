from collections import defaultdict

class EventManager:
    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_name, callback):
        """Subscribe a callback to an event."""
        self.listeners[event_name].append(callback)

    def unsubscribe(self, event_name, callback):
        """Unsubscribe a callback from an event."""
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)

    def publish(self, event_name, *args, **kwargs):
        """Publish an event to notify all subscribers."""
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(*args, **kwargs)