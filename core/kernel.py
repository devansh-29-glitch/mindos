import json
from pathlib import Path
from modules.perception import Perception
from modules.memory import Memory
from modules.reasoning import Reasoning
from modules.emotion import Emotion
from modules.action import Action
from modules.homeostasis import Homeostasis
from bus.neural_bus import NeuralBus
from rich.console import Console

console = Console()


class Kernel:
    """The central MindOS kernel — boots, manages, and coordinates all modules."""

    def __init__(self):
        self.bus = NeuralBus()
        self.config = self.load_config()  # ✅ Load brain settings from JSON
        self.modules = []

    def load_config(self):
        """Load OS-level parameters from config file."""
        cfg_path = Path("config/mindos_config.json")
        if not cfg_path.exists():
            console.log("[yellow]⚠️ No config file found — using defaults.[/yellow]")
            return {"heartbeat_interval": 2.0, "memory_buffer": 10, "log_detail": True}
        try:
            with open(cfg_path, "r") as f:
                config = json.load(f)
            console.log(f"[blue]⚙️  Config loaded from {cfg_path}[/blue]")
            return config
        except Exception as e:
            console.log(f"[red]Failed to load config: {e}[/red]")
            return {"heartbeat_interval": 2.0, "memory_buffer": 10, "log_detail": True}

    def boot(self):
        """Boots all modules and starts their threads."""
        console.rule("[bold green]MindOS Kernel Boot[/bold green]")
        self.modules = [
            Perception(self.bus, name="Perception"),
            Memory(self.bus, name="Memory"),
            Emotion(self.bus, name="Emotion"),
            Reasoning(self.bus, name="Reasoning"),
            Action(self.bus, name="Action"),
            Homeostasis(self.bus, name="Homeostasis"),
        ]

        for m in self.modules:
            m.start()
            console.log(f"[green]{m.name}[/green] starting…")

        console.log("[bold green]Kernel ready — all modules started.[/bold green]")
        console.rule("[bold cyan]MindOS Running[/bold cyan]")

    def shutdown(self):
        """Stops all running modules gracefully."""
        console.rule("[bold red]MindOS Kernel Shutdown[/bold red]")
        for m in self.modules:
            m.stop()
        for m in self.modules:
            m.join()
            console.log(f"[yellow]{m.name}[/yellow] stopped.")
        console.log("[bold red]All services stopped.[/bold red]")