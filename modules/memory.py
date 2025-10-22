from modules.base import BaseModule
from bus import topics
from collections import deque
from core.persistence import save_memory, load_memory
import random

class Memory(BaseModule):
    SUBSCRIPTIONS = [topics.SENSORY_INPUT, topics.REASONING_DECISION]

    def __init__(self, bus, name="Memory"):
        super().__init__(bus, name)
        self.buffer = deque(maxlen=15)
        self.loaded = load_memory()

    def on_message(self, topic, payload):
        """Stores sensory and reasoning data."""
        if topic == topics.SENSORY_INPUT:
            entry = {"stimulus": payload["stimulus"], "emotion": None}
            self.buffer.append(entry)
        elif topic == topics.REASONING_DECISION:
            if self.buffer:
                self.buffer[-1]["emotion"] = random.choice(["curious", "focused", "bored"])
        self.publish(topics.MEMORY_UPDATED, {"stored": list(self.buffer)})

    def stop(self):
        """On shutdown, persist current memory."""
        save_memory({"memory_trace": list(self.buffer)})
        super().stop()
