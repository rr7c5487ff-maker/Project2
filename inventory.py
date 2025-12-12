"""
inventory.py

Business logic for managing the shoe inventory.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from models import Shoe
from data_storage import load_inventory, save_inventory


class InventoryManager:
    """
    Manages an in-memory list of shoes and persists changes to a CSV file.
    """

    def __init__(self, csv_path: Path) -> None:
        """
        Initialize manager and load data from CSV.

        Args:
            csv_path (Path): Path to inventory CSV.
        """
        self._csv_path = csv_path
        self._shoes: List[Shoe] = []

    def load(self) -> None:
        """
        Load inventory from CSV into memory.

        Raises:
            Exception: Propagates errors from storage layer.
        """
        self._shoes = load_inventory(self._csv_path)

    def list_all(self) -> List[Shoe]:
        """
        Return all shoes currently in inventory.

        Returns:
            List[Shoe]: All shoes.
        """
        return list(self._shoes)

    def add_shoe(self, shoe: Shoe) -> None:
        """
        Add a shoe to inventory and persist.

        Args:
            shoe (Shoe): Shoe to add.
        """
        self._shoes.append(shoe)
        save_inventory(self._csv_path, self._shoes)

    def remove_shoe(self, shoe: Shoe) -> bool:
        """
        Remove the first matching shoe from inventory and persist.

        Args:
            shoe (Shoe): Shoe to remove.

        Returns:
            bool: True if removed, False if not found.
        """
        for idx, existing in enumerate(self._shoes):
            if existing == shoe:
                self._shoes.pop(idx)
                save_inventory(self._csv_path, self._shoes)
                return True
        return False

    def clear_inventory(self) -> None:
        """
        Clear inventory and persist.
        """
        self._shoes.clear()
        save_inventory(self._csv_path, self._shoes)

    def search(
        self,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        color: Optional[str] = None,
        size: Optional[float] = None,
    ) -> List[Shoe]:
        """
        Search inventory by any combination of fields.

        - brand/model/color: case-insensitive substring match
        - size: exact match (float)

        Args:
            brand (Optional[str]): Brand query.
            model (Optional[str]): Model query.
            color (Optional[str]): Color query.
            size (Optional[float]): Size query.

        Returns:
            List[Shoe]: Matching shoes.
        """
        brand_q = (brand or "").strip().lower()
        model_q = (model or "").strip().lower()
        color_q = (color or "").strip().lower()

        results: List[Shoe] = []
        for shoe in self._shoes:
            if brand_q and brand_q not in shoe.brand.lower():
                continue
            if model_q and model_q not in shoe.model.lower():
                continue
            if color_q and color_q not in shoe.color.lower():
                continue
            if size is not None and shoe.size != size:
                continue
            results.append(shoe)

        return results
