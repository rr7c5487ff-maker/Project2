"""
main.py
Application entry point.
"""

from pathlib import Path

from inventory import InventoryManager
from gui import InventoryApp


def main() -> None:
    csv_path = Path("inventory.csv")
    manager = InventoryManager(csv_path)
    app = InventoryApp(manager)
    app.mainloop()


if __name__ == "__main__":
    main()
