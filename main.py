"""
main.py
Starts inventory manager
"""

from __future__ import annotations

from pathlib import Path

from inventory import InventoryManager
from gui import InventoryApp


def main() -> None:
    csv_path = Path(__file__).parent / "inventory.csv"
    manager = InventoryManager(csv_path=csv_path)
    app = InventoryApp(manager=manager)
    app.mainloop()


if __name__ == "__main__":
    main()
