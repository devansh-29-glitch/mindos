import threading
import time
from typing import Callable
from bus.message import Message
from bus import topics

class Scheduler(threading.Thread):
    """Kernel tick generator."""
    def __init__(self, publish_fn: Callable[[Message], None], period: float = 0.5):
        super().__init__(daemon=True)
        self.publish = publish_fn
        self.period = period
        self._stop = threading.Event()
        self._step = 0

    def run(self) -> None:
        while not self._stop.is_set():
            self._step += 1
            self.publish(Message(topic=topics.KERNEL_TICK, payload={"step": self._step}, source="kernel"))
            time.sleep(self.period)

    def stop(self) -> None:
        self._stop.set()
