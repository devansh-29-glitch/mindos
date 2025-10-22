import json
from pathlib import Path
from typing import Any, Dict
from rich.console import Console

console = Console()

MEMORY_FILE = Path("memory_store/persistent_memory.json")
MEMORY_FILE.parent.mkdir(exist_ok=True)

def save_memory(data: Dict[str, Any]):
    """Save memory to disk."""
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)
        console.log(f"[green]💾 Memory saved ({len(data)} entries).[/green]")
    except Exception as e:
        console.log(f"[red]Failed to save memory: {e}[/red]")

def load_memory() -> Dict[str, Any]:
    """Load previous memory from disk."""
    if not MEMORY_FILE.exists():
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
        console.log(f"[cyan]🧠 Previous memory restored ({len(data)} entries).[/cyan]")
        return data
    except Exception as e:
        console.log(f"[red]Failed to load memory: {e}[/red]")
        return {}


