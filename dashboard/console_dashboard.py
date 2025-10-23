# dashboard ka console_dashboard.py wala code
import time
from threading import Thread
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.console import Group
from bus import topics
from bus.message import Message

class ConsoleDashboard(Thread):
    """Live terminal dashboard for MindOS telemetry."""
    def __init__(self, bus):
        super().__init__(daemon=True)
        self.bus = bus
        self._stop = False

        # subscribe to key streams
        self.q_hb = self.bus.subscribe(topics.TELEMETRY_HEARTBEAT)
        self.q_em = self.bus.subscribe(topics.EMOTION_STATE)
        self.q_int = self.bus.subscribe(topics.INTENT_PLAN)
        self.q_act = self.bus.subscribe(topics.ACTION_EXECUTED)

        self.heartbeats = []
        self.emotions = {"arousal": 0, "valence": 0}
        self.last_intent = "-"
        self.last_action = "-"

    def stop(self):
        self._stop = True

    def run(self):
        with Live(self.layout(), refresh_per_second=4, transient=False) as live:
            while not self._stop:
                self._poll()
                live.update(self.layout())
                time.sleep(0.25)

    def _poll(self):
        def drain(q):
            items = []
            while not q.empty():
                items.append(q.get_nowait())
            return items

        for m in drain(self.q_hb):
            self.heartbeats.append(m.payload["module"])
            self.heartbeats = self.heartbeats[-20:]

        for m in drain(self.q_em):
            self.emotions = m.payload

        for m in drain(self.q_int):
            self.last_intent = m.payload.get("action")

        for m in drain(self.q_act):
            self.last_action = m.payload.get("action")

    def layout(self):
        tbl = Table(title="🧠  Module Heartbeats (last 20)")
        tbl.add_column("Module")
        for mod in self.heartbeats[-10:]:
            tbl.add_row(mod)

        emo = Table(title="💓  Emotion State")
        emo.add_column("Arousal")
        emo.add_column("Valence")
        emo.add_row(f"{self.emotions['arousal']:.2f}", f"{self.emotions['valence']:.2f}")

        act = Table(title="⚙️  Cognitive Loop")
        act.add_column("Last Intent")
        act.add_column("Last Action")
        act.add_row(str(self.last_intent), str(self.last_action))

        return Panel(
            Group(tbl, emo, act),
            title="[bold cyan]MindOS Live Telemetry",
            border_style="bright_magenta",
        )
