from modules.base import BaseModule
from bus import topics
import random

class Perception(BaseModule):
    SUBSCRIPTIONS = []

    def __init__(self, bus, name="Perception"):
        super().__init__(bus, name)

    def loop(self):
        # Emit sensory data
        sensory_data = random.choice(["light", "sound", "motion"])
        self.publish(topics.SENSORY_INPUT, {"stimulus": sensory_data})
