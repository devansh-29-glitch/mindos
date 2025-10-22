from modules.base import BaseModule
from bus import topics
import random
import numpy as np

class Reasoning(BaseModule):
    SUBSCRIPTIONS = [topics.MEMORY_UPDATED]

    def __init__(self, bus, name="Reasoning"):
        super().__init__(bus, name)

    def on_message(self, topic, payload):
        if "stored" in payload:
            decision = random.choice(["analyze", "predict", "reflect"])
            self.publish(topics.REASONING_DECISION, {"decision": decision})
