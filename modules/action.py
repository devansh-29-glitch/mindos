from modules.base import BaseModule
from bus import topics
import random

class Action(BaseModule):
    SUBSCRIPTIONS = [topics.REASONING_DECISION, topics.EMOTIONAL_STATE]

    def __init__(self, bus, name="Action"):
        super().__init__(bus, name)
        self.state = {}

    def on_message(self, topic, payload):
        self.state.update(payload)
        if len(self.state) == 2:
            self.publish(topics.ACTION_EXECUTED, {"action": random.choice(["move", "speak", "pause"])})
            self.state.clear()
