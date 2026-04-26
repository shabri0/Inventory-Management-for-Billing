import tkinter as tk
from tkinter import ttk, messagebox

# Store inventory data
inventory = {}  # {item_name: {"quantity": int, "price": float}}

# ---------------- INVENTORY FUNCTIONS ----------------
def add_item():
    name = entry_name.get().strip()
    qty = entry_qty.get().strip()
    price = entry_price.get().strip()
    
    if not name or not qty or not price:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return
    if name in inventory:
        messagebox.showwarning("Duplicate", "Item already exists. Use Update instead.")
        return
    try:
        qty = int(qty)
        price = float(price)
    except ValueError:
        messagebox.showerror("Input Error", "Quantity must be integer, price must be a number.")
        return
    
    inventory[name] = {"quantity": qty, "price": price}
    refresh_table()
    clear_entries()
    messagebox.showinfo("Success", f"{name} added successfully.")

def update_item():
    name = entry_name.get().strip()
    if name not in inventory:
        messagebox.showerror("Error", "Item not found.")
        return
    try:
        qty = int(entry_qty.get().strip())
        price = float(entry_price.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Invalid quantity or price.")
        return
    
    inventory[name] = {"quantity": qty, "price": price}
    refresh_table()
    clear_entries()
    messagebox.showinfo("Updated", f"{name} updated successfully.")

def delete_item():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Item", "Please select an item to delete.")
        return
    item_name = tree.item(selected[0], "values")[0]
    del inventory[item_name]
    refresh_table()
    messagebox.showinfo("Deleted", f"{item_name} deleted successfully.")

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for item, details in inventory.items():
        tree.insert("", tk.END, values=(item, details["quantity"], details["price"]))

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_qty.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# ---------------- CUSTOMER BILLING ----------------
def open_billing():
    bill_win = tk.Toplevel(root)
    bill_win.title("Customer Billing")
    bill_win.geometry("500x500")

    tk.Label(bill_win, text="Select Item:").pack(pady=5)
    item_var = tk.StringVar()
    item_dropdown = ttk.Combobox(bill_win, textvariable=item_var, values=list(inventory.keys()))
    item_dropdown.pack(pady=5)

    tk.Label(bill_win, text="Quantity:").pack(pady=5)
    qty_entry = tk.Entry(bill_win)
    qty_entry.pack(pady=5)

    bill_area = tk.Text(bill_win, height=20, width=50)
    bill_area.pack(pady=10)

    total_price = [0]  # Mutable list to store total

    bill_area.insert(tk.END, "===== Customer Bill =====\n")

    def add_to_bill():
        item = item_var.get().strip()
        qty = qty_entry.get().strip()
        if not item or not qty:
            messagebox.showwarning("Input Error", "Please select an item and enter quantity.")
            return
        if item not in inventory:
            messagebox.showerror("Error", "Item not found in inventory.")
            return
        try:
            qty = int(qty)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer.")
            return
        if qty > inventory[item]["quantity"]:
            messagebox.showerror("Error", "Not enough stock available.")
            return
        
        price = inventory[item]["price"] * qty
        total_price[0] += price
        inventory[item]["quantity"] -= qty
        refresh_table()
        bill_area.insert(tk.END, f"{item} x {qty} = ₹{price:.2f}\n")
        qty_entry.delete(0, tk.END)

    def finish_bill():
        bill_area.insert(tk.END, f"\nTotal Amount: ₹{total_price[0]:.2f}")
        messagebox.showinfo("Bill Complete", "Bill generated successfully!")

    tk.Button(bill_win, text="Add to Bill", command=add_to_bill).pack(pady=5)
    tk.Button(bill_win, text="Finish Bill", command=finish_bill).pack(pady=5)

# ---------------- MAIN GUI ----------------
root = tk.Tk()
root.title("Inventory Manager with Billing")
root.geometry("600x500")

# Input Frame
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_inputs)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
entry_qty = tk.Entry(frame_inputs)
entry_qty.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Price:").grid(row=2, column=0, padx=5, pady=5)
entry_price = tk.Entry(frame_inputs)
entry_price.grid(row=2, column=1, padx=5, pady=5)

# Buttons Frame
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

tk.Button(frame_buttons, text="Add", command=add_item, width=10).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Update", command=update_item, width=10).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="Delete", command=delete_item, width=10).grid(row=0, column=2, padx=5)
tk.Button(frame_buttons, text="Clear", command=clear_entries, width=10).grid(row=0, column=3, padx=5)
tk.Button(frame_buttons, text="Billing", command=open_billing, width=10, bg="lightblue").grid(row=0, column=4, padx=5)

# Inventory Table
columns = ("Item Name", "Quantity", "Price")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(pady=10)

root.mainloop()
