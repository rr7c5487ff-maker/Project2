"""
Reads and writes to CSV file.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from models import Shoe


CSV_HEADERS: list[str] = ["brand", "model", "size", "color"]


def ensure_csv_exists(csv_path: Path) -> None:
    """
    Ensure CSV file exists.
    """
    if not csv_path.exists():
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)


def load_inventory(csv_path: Path) -> List[Shoe]:
    """
    Load shoes from the CSV file.
    """
    ensure_csv_exists(csv_path)

    shoes: List[Shoe] = []
    with csv_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV file missing headers.")

        for i, row in enumerate(reader, start=2):
            try:
                brand = (row.get("brand") or "").strip()
                model = (row.get("model") or "").strip()
                color = (row.get("color") or "").strip()
                size_str = (row.get("size") or "").strip()

                if not brand or not model or not color or not size_str:
                    raise ValueError("Missing required fields.")

                size = float(size_str)
                shoes.append(Shoe(brand=brand, model=model, size=size, color=color))
            except Exception as exc:
                raise ValueError(f"Invalid data on CSV line {i}: {row}") from exc

    return shoes


def save_inventory(csv_path: Path, shoes: List[Shoe]) -> None:
    """
    Save the inventory to the CSV file.
    """
    ensure_csv_exists(csv_path)

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)
        for shoe in shoes:
            writer.writerow(shoe.to_row())
