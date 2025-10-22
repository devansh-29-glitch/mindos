import threading
import time
import random
from queue import Queue, Empty
from typing import List, Dict, Any
from rich.console import Console
from bus.neural_bus import NeuralBus
from bus.message import Message
from bus import topics

console = Console()


class BaseModule(threading.Thread):
    """Base class for all cognitive modules with message subscriptions."""
    SUBSCRIPTIONS: List[str] = []
    HEARTBEAT_EVERY: float = 2.0

    def __init__(self, bus: NeuralBus, name: str):
        super().__init__(daemon=True)
        self.name = name
        self.bus = bus

        # ✅ renamed from _stop to _stop_event (fixes TypeError)
        self._stop_event = threading.Event()

        self._inboxes: Dict[str, Queue] = {}
        self._last_heartbeat = 0.0

        # Subscribe to topics
        for t in self.SUBSCRIPTIONS:
            self._inboxes[t] = self.bus.subscribe(t)

    def publish(self, topic: str, payload: Any):
        """Publish a message to the shared NeuralBus."""
        self.bus.publish(Message(topic=topic, payload=payload, source=self.name))

    def on_message(self, topic: str, payload: Any):
        """Override this method to define custom message handling."""
        pass

    def setup(self):
        """Optional once-at-start hook for initialization."""
        pass

    def loop(self):
        """Optional loop for periodic background processes."""
        pass

    def run(self):
        console.log(f"[cyan]{self.name}[/cyan] starting…")
        self.setup()

        while not self._stop_event.is_set():
            # Heartbeat ping
            now = time.time()
            if now - self._last_heartbeat > self.HEARTBEAT_EVERY:
                self.publish(topics.TELEMETRY_HEARTBEAT, {"module": self.name, "ts": now})
                self._last_heartbeat = now

            # Handle messages from subscribed topics
            for topic, q in self._inboxes.items():
                try:
                    msg = q.get_nowait()
                    self.on_message(topic, msg.payload)
                except Empty:
                    pass

            # Background loop
            self.loop()
            # optional: small pulse animation
            if random.random() < 0.01:
                console.log(f"[dim]{self.name} processing…[/dim]")

            time.sleep(0.05)

        console.log(f"[cyan]{self.name}[/cyan] stopped.")

    def stop(self):
        """Gracefully signal the module to stop."""
        self._stop_event.set() 