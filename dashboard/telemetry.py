from typing import Dict, Any
from collections import deque

class TelemetryStore:
    def __init__(self, maxlen: int = 200):
        self.heartbeats = deque(maxlen=maxlen)
        self.actions = deque(maxlen=maxlen)

    def add_heartbeat(self, hb: Dict[str, Any]):
        self.heartbeats.append(hb)

    def add_action(self, act: Dict[str, Any]):
        self.actions.append(act)
