from modules.base import BaseModule
from bus import topics
import random

class Emotion(BaseModule):
    SUBSCRIPTIONS = [topics.SENSORY_INPUT]

    def __init__(self, bus, name="Emotion"):
        super().__init__(bus, name)

    def on_message(self, topic, payload):
        mood = random.choice(["calm", "alert", "curious"])
        self.publish(topics.EMOTIONAL_STATE, {"mood": mood})
