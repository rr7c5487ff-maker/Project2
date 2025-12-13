"""
inventory.py
Manages the shoe inventory and CSV storage.
"""

import csv
from pathlib import Path
from typing import List

from models import Shoe


class InventoryManager:
    """
    Manages shoe inventory stored in a CSV file.
    """

    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path
        self.shoes: List[Shoe] = []

    def load_inventory(self) -> None:
        """
        Load shoes from CSV file.
        """
        if not self.csv_path.exists():
            with open(self.csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["brand", "model", "size", "color"])

        with open(self.csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            self.shoes = []
            for row in reader:
                shoe = Shoe(
                    row["brand"],
                    row["model"],
                    float(row["size"]),
                    row["color"],
                )
                self.shoes.append(shoe)

    def save_inventory(self) -> None:
        """
        Save inventory to CSV file.
        """
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["brand", "model", "size", "color"])
            for shoe in self.shoes:
                writer.writerow([shoe.brand, shoe.model, shoe.size, shoe.color])

    def add_shoe(self, shoe: Shoe) -> None:
        """
        Add a shoe to inventory.
        """
        self.shoes.append(shoe)
        self.save_inventory()

    def remove_shoe(self, index: int) -> None:
        """
        Remove a shoe by index.
        """
        self.shoes.pop(index)
        self.save_inventory()

    def clear_inventory(self) -> None:
        """
        Remove all shoes.
        """
        self.shoes.clear()
        self.save_inventory()
