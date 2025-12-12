"""
models.py

Contains the data model(s) used by the application.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Shoe:
    """
    Represents a single shoe inventory item.
    """
    brand: str
    model: str
    size: float
    color: str

    def to_row(self) -> list[str]:
        """
        Convert the Shoe to a CSV row (all values as strings).

        Returns:
            list[str]: CSV row values in correct column order.
        """
        return [self.brand, self.model, self._format_size(self.size), self.color]

    @staticmethod
    def _format_size(size: float) -> str:
        """
        Format sizes so 10.0 becomes '10' but 9.5 stays '9.5'.

        Args:
            size (float): Shoe size.

        Returns:
            str: A nicely formatted size string.
        """
        if float(size).is_integer():
            return str(int(size))
        return str(size)
