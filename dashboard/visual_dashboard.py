import os
import time
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from core.persistence import load_memory

console = Console()

def generate_activity_state():
    """Simulated live brain module activity levels."""
    return {
        "Perception": random.choice(["active", "idle", "scanning"]),
        "Memory": random.choice(["updating", "retrieving", "stable"]),
        "Emotion": random.choice(["focused", "neutral", "excited", "calm"]),
        "Reasoning": random.choice(["thinking...", "integrating", "predicting"]),
        "Action": random.choice(["executing move()", "planning", "waiting"]),
        "Homeostasis": random.choice(["stable", "adjusting"]),
    }

def draw_dashboard():
    table = Table(title="🧠 MindOS Neural Activity Dashboard", expand=True)
    table.add_column("Module", justify="left", style="bold cyan")
    table.add_column("State", justify="left")

    memory_data = load_memory()
    trace_size = len(memory_data.get("memory_trace", []))
    states = generate_activity_state()

    # Dynamic color indicators
    for module, state in states.items():
        color = "green"
        if "idle" in state or "stable" in state:
            color = "yellow"
        elif "thinking" in state or "updating" in state:
            color = "cyan"
        elif "executing" in state or "move" in state:
            color = "red"
        table.add_row(module, f"[{color}]{state}[/{color}]")

    cognitive_load = random.randint(35, 90)
    load_bar = "█" * (cognitive_load // 10) + "░" * (10 - cognitive_load // 10)

    panel = Panel.fit(
        f"Cognitive Load: [bold magenta]{load_bar} {cognitive_load}%[/bold magenta]\n"
        f"Memory Trace Size: [bold yellow]{trace_size}[/bold yellow] entries",
        border_style="blue",
    )

    return table, panel


def run_dashboard(duration: int = 20):
    """Run live dashboard for given seconds."""
    console.clear()
    with Live(console=console, refresh_per_second=2):
        start = time.time()
        while time.time() - start < duration:
            table, panel = draw_dashboard()
            console.clear()
            console.print(table)
            console.print(panel)
            time.sleep(0.8)

    console.print("\n[bold green]✅ MindOS Dashboard session ended.[/bold green]")


if __name__ == "__main__":
    run_dashboard()
