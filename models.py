"""
models.py
Creates shoe class for simple attributes.
"""

class Shoe:
    """
    One shoe in inventory.
    """

    def __init__(self, brand: str, model: str, size: float, color: str) -> None:
        self.brand = brand
        self.model = model
        self.size = size
        self.color = color
