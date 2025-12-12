"""
gui.py

Tkinter GUI for the shoe Manager.
"""
# A LOT OF GUI TKINTER CODE GENERATED USING AI, DOCSTRINGS ADDED BY ME
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Optional

from models import Shoe
from inventory import InventoryManager


class InventoryApp(tk.Tk):
    """
    Tkinter window.
    """

    def __init__(self, manager: InventoryManager) -> None:
        """
        Make GUI and load inventory.

        Args:
            manager (InventoryManager): Inventory manager instance.
        """
        super().__init__()
        self.title("Shoe Inventory Manager")
        self.geometry("800x500")
        self.resizable(False, False)

        self._manager = manager

        self.brand_var = tk.StringVar()
        self.model_var = tk.StringVar()
        self.size_var = tk.StringVar()
        self.color_var = tk.StringVar()
      
        self.search_brand_var = tk.StringVar()
        self.search_model_var = tk.StringVar()
        self.search_size_var = tk.StringVar()
        self.search_color_var = tk.StringVar()

        self._build_ui()
      
        try:
            self._manager.load()
            self._refresh_list(self._manager.list_all())
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to load inventory.\n\n{exc}")

    def _build_ui(self) -> None:
        """
        Build all GUI widgets.
        """
        add_frame = tk.LabelFrame(self, text="Add Shoe", padx=10, pady=10)
        add_frame.place(x=10, y=10, width=380, height=200)

        tk.Label(add_frame, text="Brand:").grid(row=0, column=0, sticky="w")
        tk.Entry(add_frame, textvariable=self.brand_var, width=30).grid(row=0, column=1, pady=5)

        tk.Label(add_frame, text="Model:").grid(row=1, column=0, sticky="w")
        tk.Entry(add_frame, textvariable=self.model_var, width=30).grid(row=1, column=1, pady=5)

        tk.Label(add_frame, text="Size:").grid(row=2, column=0, sticky="w")
        tk.Entry(add_frame, textvariable=self.size_var, width=30).grid(row=2, column=1, pady=5)

        tk.Label(add_frame, text="Color:").grid(row=3, column=0, sticky="w")
        tk.Entry(add_frame, textvariable=self.color_var, width=30).grid(row=3, column=1, pady=5)

        tk.Button(add_frame, text="Add Shoe", command=self._on_add).grid(row=4, column=0, columnspan=2, pady=10)

        search_frame = tk.LabelFrame(self, text="Search (leave blank to ignore a field)", padx=10, pady=10)
        search_frame.place(x=10, y=220, width=380, height=220)

        tk.Label(search_frame, text="Brand contains:").grid(row=0, column=0, sticky="w")
        tk.Entry(search_frame, textvariable=self.search_brand_var, width=30).grid(row=0, column=1, pady=5)

        tk.Label(search_frame, text="Model contains:").grid(row=1, column=0, sticky="w")
        tk.Entry(search_frame, textvariable=self.search_model_var, width=30).grid(row=1, column=1, pady=5)

        tk.Label(search_frame, text="Size equals:").grid(row=2, column=0, sticky="w")
        tk.Entry(search_frame, textvariable=self.search_size_var, width=30).grid(row=2, column=1, pady=5)

        tk.Label(search_frame, text="Color contains:").grid(row=3, column=0, sticky="w")
        tk.Entry(search_frame, textvariable=self.search_color_var, width=30).grid(row=3, column=1, pady=5)

        tk.Button(search_frame, text="Search", command=self._on_search).grid(row=4, column=0, pady=10, sticky="ew")
        tk.Button(search_frame, text="Show All", command=self._on_show_all).grid(row=4, column=1, pady=10, sticky="ew")

        list_frame = tk.LabelFrame(self, text="Inventory", padx=10, pady=10)
        list_frame.place(x=410, y=10, width=380, height=430)

        self.listbox = tk.Listbox(list_frame, width=55, height=18)
        self.listbox.grid(row=0, column=0, columnspan=2, pady=5)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        tk.Button(list_frame, text="Remove Selected", command=self._on_remove_selected).grid(row=1, column=0, pady=10, sticky="ew")
        tk.Button(list_frame, text="Clear Inventory", command=self._on_clear).grid(row=1, column=1, pady=10, sticky="ew")
      
        hint = tk.Label(self, text="Tip: Select an item in the list to remove it.", fg="gray")
        hint.place(x=410, y=450)

    def _parse_size(self, size_text: str) -> float:
        """
        Parse and validate shoe size.

        Args:
            size_text (str): Size string from user input.

        Returns:
            float: Parsed size.

        Raises:
            ValueError: If invalid.
        """
        size_text = size_text.strip()
        if not size_text:
            raise ValueError("Size is required.")
        size = float(size_text)
        if size <= 0:
            raise ValueError("Size must be greater than 0.")
        return size

    def _validate_text(self, value: str, field_name: str) -> str:
        """
        Validate non-empty text fields.

        Args:
            value (str): Input value.
            field_name (str): Field label for error messages.

        Returns:
            str: Cleaned value.

        Raises:
            ValueError: If empty.
        """
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(f"{field_name} is required.")
        return cleaned

    def _on_add(self) -> None:
        """
        Handle Add Shoe button.
        """
        try:
            brand = self._validate_text(self.brand_var.get(), "Brand")
            model = self._validate_text(self.model_var.get(), "Model")
            color = self._validate_text(self.color_var.get(), "Color")
            size = self._parse_size(self.size_var.get())

            shoe = Shoe(brand=brand, model=model, size=size, color=color)
            self._manager.add_shoe(shoe)
            self._refresh_list(self._manager.list_all())
            self._clear_add_fields()
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"Could not add shoe.\n\n{exc}")

    def _on_remove_selected(self) -> None:
        """
        Handle Remove Selected button.
        """
        try:
            selection = self.listbox.curselection()
            if not selection:
                messagebox.showinfo("Info", "Please select a shoe to remove.")
                return

            item_text = self.listbox.get(selection[0])
            shoe = self._shoe_from_list_text(item_text)
            removed = self._manager.remove_shoe(shoe)

            if not removed:
                messagebox.showwarning("Not Found", "That shoe could not be found (it may have changed).")

            self._refresh_list(self._manager.list_all())
        except Exception as exc:
            messagebox.showerror("Error", f"Could not remove shoe.\n\n{exc}")

    def _on_clear(self) -> None:
        """
        Handle Clear Inventory button.
        """
        try:
            confirm = messagebox.askyesno("Confirm", "Clear ALL inventory? This cannot be undone.")
            if not confirm:
                return
            self._manager.clear_inventory()
            self._refresh_list(self._manager.list_all())
        except Exception as exc:
            messagebox.showerror("Error", f"Could not clear inventory.\n\n{exc}")

    def _on_search(self) -> None:
        """
        Handle Search button.
        """
        try:
            brand = self.search_brand_var.get().strip() or None
            model = self.search_model_var.get().strip() or None
            color = self.search_color_var.get().strip() or None

            size_text = self.search_size_var.get().strip()
            size: Optional[float] = None
            if size_text:
                size = self._parse_size(size_text)

            results = self._manager.search(brand=brand, model=model, color=color, size=size)
            self._refresh_list(results)
        except ValueError as exc:
            messagebox.showerror("Invalid Input", str(exc))
        except Exception as exc:
            messagebox.showerror("Error", f"Search failed.\n\n{exc}")

    def _on_show_all(self) -> None:
        """
        Handle Show All button.
        """
        try:
            self._refresh_list(self._manager.list_all())
        except Exception as exc:
            messagebox.showerror("Error", f"Could not refresh inventory.\n\n{exc}")

    def _refresh_list(self, shoes: list[Shoe]) -> None:
        """
        Refresh the listbox display.

        Args:
            shoes (list[Shoe]): Shoes to display.
        """
        self.listbox.delete(0, tk.END)
        for shoe in shoes:
            self.listbox.insert(tk.END, self._shoe_to_list_text(shoe))

    def _shoe_to_list_text(self, shoe: Shoe) -> str:
        """
        Convert a Shoe into a nice listbox display string.

        Args:
            shoe (Shoe): Shoe item.

        Returns:
            str: Display string.
        """

        size_str = str(int(shoe.size)) if float(shoe.size).is_integer() else str(shoe.size)
        return f"Brand: {shoe.brand} | Model: {shoe.model} | Size: {size_str} | Color: {shoe.color}"

    def _shoe_from_list_text(self, text: str) -> Shoe:
        """
        Parse a Shoe back from the listbox display string.

        Args:
            text (str): Display string.

        Returns:
            Shoe: Parsed shoe.

        Raises:
            ValueError: If parsing fails.
        """
        try:
            parts = [p.strip() for p in text.split("|")]
            brand = parts[0].split(":", 1)[1].strip()
            model = parts[1].split(":", 1)[1].strip()
            size_str = parts[2].split(":", 1)[1].strip()
            color = parts[3].split(":", 1)[1].strip()
            size = float(size_str)
            return Shoe(brand=brand, model=model, size=size, color=color)
        except Exception as exc:
            raise ValueError(f"Could not parse shoe from list item: {text}") from exc

    def _clear_add_fields(self) -> None:
        """
        Clear the add-shoe form inputs.
        """
        self.brand_var.set("")
        self.model_var.set("")
        self.size_var.set("")
        self.color_var.set("")

