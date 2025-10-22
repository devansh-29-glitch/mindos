from core.kernel import Kernel
from rich.console import Console
import time

console = Console()

if __name__ == "__main__":
    console.rule("[bold cyan]MindOS Kernel Boot[/bold cyan]")
    k = Kernel()
    k.boot()
    console.rule("[bold green]MindOS Running[/bold green]")

    try:
        time.sleep(10)  # run for 10 seconds demo
    except KeyboardInterrupt:
        console.print("\nGraceful shutdown requested.")
    finally:
        console.rule("[bold red]MindOS Kernel Shutdown[/bold red]")
        k.shutdown()
