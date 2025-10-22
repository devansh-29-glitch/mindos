from modules.base import BaseModule
from bus import topics
import random

class Homeostasis(BaseModule):
    SUBSCRIPTIONS = [topics.TELEMETRY_HEARTBEAT]

    def __init__(self, bus, name="Homeostasis"):
        super().__init__(bus, name)
        self.energy = 100

    def on_message(self, topic, payload):
        self.energy -= random.uniform(0.1, 1.0)
        if self.energy <= 90:
            self.publish(topics.HOMEOSTASIS_SIGNAL, {"energy": self.energy})
            self.energy = 100
