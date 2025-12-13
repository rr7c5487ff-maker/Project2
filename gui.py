"""
gui.py
Tkinter GUI for the Footwear Inventory Manager.
"""

import tkinter as tk
from tkinter import messagebox

from models import Shoe
from inventory import InventoryManager
# AI HELPED GENERATE TKINTER CODE, ASSISTED IN FIRST FUNCTION MOSTLY

class InventoryApp(tk.Tk):
    """
    GUI application for managing footwear inventory.
    """

    def __init__(self, manager: InventoryManager) -> None:
        super().__init__()

        self.manager = manager

        self.title("Footwear Inventory Manager")
        self.geometry("700x500")
        self.minsize(700, 500)

        # Input fields
        self.brand_var = tk.StringVar()
        self.model_var = tk.StringVar()
        self.size_var = tk.StringVar()
        self.color_var = tk.StringVar()

        self._build_ui()
        self.manager.load_inventory()
        self.refresh_list()

    def _build_ui(self) -> None:
        """
        Build GUI layout.
        """

        # --- Add Shoe Frame ---
        add_frame = tk.LabelFrame(self, text="Add Shoe")
        add_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(add_frame, text="Brand").grid(row=0, column=0, sticky="w")
        tk.Entry(add_frame, textvariable=self.brand_var).grid(row=0, column=1)

        tk.Label(add_frame, text="Model").grid(row=1, column=0, sticky="w")
        tk.Entry(add_frame, textvariable=self.model_var).grid(row=1, column=1)

        tk.Label(add_frame, text="Size").grid(row=2, column=0, sticky="w")
        tk.Entry(add_frame, textvariable=self.size_var).grid(row=2, column=1)

        tk.Label(add_frame, text="Color").grid(row=3, column=0, sticky="w")
        tk.Entry(add_frame, textvariable=self.color_var).grid(row=3, column=1)

        tk.Button(add_frame, text="Add Shoe", command=self.add_shoe).grid(
            row=4, column=0, columnspan=2, pady=5
        )

        # --- Inventory List ---
        list_frame = tk.LabelFrame(self, text="Inventory")
        list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.listbox = tk.Listbox(list_frame, width=40)
        self.listbox.pack(padx=5, pady=5)

        tk.Button(list_frame, text="Remove Selected", command=self.remove_selected).pack(pady=5)
        tk.Button(list_frame, text="Clear Inventory", command=self.clear_inventory).pack(pady=5)

        self.grid_columnconfigure(1, weight=1)

    def add_shoe(self) -> None:
        """
        Add shoe from input fields.
        """
        try:
            brand = self.brand_var.get().strip()
            model = self.model_var.get().strip()
            color = self.color_var.get().strip()
            size = float(self.size_var.get())

            if not brand or not model or not color:
                raise ValueError("All fields are required.")

            shoe = Shoe(brand, model, size, color)
            self.manager.add_shoe(shoe)
            self.refresh_list()

            self.brand_var.set("")
            self.model_var.set("")
            self.size_var.set("")
            self.color_var.set("")

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please check your values.")

    def remove_selected(self) -> None:
        """
        Remove selected shoe.
        """
        if not self.listbox.curselection():
            messagebox.showinfo("Info", "Select a shoe to remove.")
            return

        index = self.listbox.curselection()[0]
        self.manager.remove_shoe(index)
        self.refresh_list()

    def clear_inventory(self) -> None:
        """
        Clear entire inventory.
        """
        if messagebox.askyesno("Confirm", "Clear all inventory?"):
            self.manager.clear_inventory()
            self.refresh_list()

    def refresh_list(self) -> None:
        """
        Refresh inventory listbox.
        """
        self.listbox.delete(0, tk.END)
        for shoe in self.manager.shoes:
            self.listbox.insert(
                tk.END,
                f"{shoe.brand} - {shoe.model} - Size {shoe.size} - {shoe.color}"
            )
