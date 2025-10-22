from queue import Queue
from collections import defaultdict

class NeuralBus:
    """Central communication bus for all modules."""

    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, topic):
        q = Queue()
        self.subscribers[topic].append(q)
        return q

    def publish(self, message):
        for q in self.subscribers.get(message.topic, []):
            q.put(message)
