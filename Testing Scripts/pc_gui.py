import customtkinter as ctk
import json
import os

# --- Data Handling ---
FILE_PATH = 'Testing Scripts/data.json'

def load_data():
    try:
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'r') as file:
                return json.load(file)
    except Exception as e:
        print(f"Error loading data: {e}")
    return {}

def save_data(data):
    try:
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        with open(FILE_PATH, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error saving data: {e}")

inventory = load_data()

# --- GUI Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pantry-Pi PC GUI Test")
app.geometry("500x400")

scanner_status = "Status: USB Scanner Active (Ready to Scan)"

title_label = ctk.CTkLabel(app, text="Last Scanned Item: ", font=("Arial", 24, "bold"))
title_label.pack(pady=(20,5))

readout_label = ctk.CTkLabel(app, text="Waiting...", font=("Arial", 40, "bold"), text_color="#00FF00")
readout_label.pack(pady=5)

info_frame = ctk.CTkFrame(app)
info_frame.pack(pady=10, padx=20, fill="x")

name_label = ctk.CTkLabel(info_frame, text="Name: -", font=("Arial", 18))
name_label.pack(anchor="w", padx=10, pady=5)

price_label = ctk.CTkLabel(info_frame, text="Price: -", font=("Arial", 18))
price_label.pack(anchor="w", padx=10, pady=5)

stock_label = ctk.CTkLabel(info_frame, text="Stock: -", font=("Arial", 18))
stock_label.pack(anchor="w", padx=10, pady=5)

status_label = ctk.CTkLabel(app, text=scanner_status, font=("Arial", 14), text_color="gray")
status_label.pack(pady=(5, 5))

# --- USB Scanner Logic ---
# USB scanners act as keyboards. They type characters quickly and hit Enter.
barcode_buffer = ""

def process_barcode(barcode):
    barcode = barcode.strip()
    if not barcode:
        return
        
    readout_label.configure(text=barcode)
    
    if barcode in inventory:
        item = inventory[barcode]
        name_label.configure(text=f"Name: {item.get('name', 'N/A')}")
        price_label.configure(text=f"Price: ${item.get('price', 'N/A')}")
        stock_label.configure(text=f"Stock: {item.get('stock', 'N/A')}")
        status_label.configure(text=f"Status: Item Found", text_color="#00FF00")
    else:
        name_label.configure(text="Name: -")
        price_label.configure(text="Price: -")
        stock_label.configure(text="Stock: -")
        status_label.configure(text=f"Status: Item Not Found. Add it below.", text_color="red")
        prompt_add_item(barcode)

def on_key(event):
    global barcode_buffer
    if event.keysym in ('Return', 'KP_Enter'):
        process_barcode(barcode_buffer)
        barcode_buffer = ""
    elif event.char and event.char.isprintable():
        barcode_buffer += event.char

app.bind("<Key>", on_key)

# --- Add New Item Popup ---
def prompt_add_item(barcode):
    popup = ctk.CTkToplevel(app)
    popup.title("Add New Product")
    popup.geometry("300x300")
    popup.transient(app)
    popup.grab_set() # Focus on popup
    
    ctk.CTkLabel(popup, text=f"Adding Barcode:\n{barcode}", font=("Arial", 16, "bold")).pack(pady=10)
    
    name_entry = ctk.CTkEntry(popup, placeholder_text="Item Name")
    name_entry.pack(pady=5)
    
    price_entry = ctk.CTkEntry(popup, placeholder_text="Price")
    price_entry.pack(pady=5)
    
    qty_entry = ctk.CTkEntry(popup, placeholder_text="Quantity")
    qty_entry.pack(pady=5)
    
    def save_new():
        name = name_entry.get().strip()
        price = price_entry.get().strip()
        qty = qty_entry.get().strip()
        
        inventory[barcode] = {
            "name" : name,
            "price" : price,
            "stock" : qty
        }
        save_data(inventory)
        
        # Update UI
        name_label.configure(text=f"Name: {name}")
        price_label.configure(text=f"Price: ${price}")
        stock_label.configure(text=f"Stock: {qty}")
        status_label.configure(text="Status: Item Saved into Inventory", text_color="#00FF00")
        
        popup.destroy()
        app.focus_force() # Return focus to main app to keep scanning

    save_btn = ctk.CTkButton(popup, text="Save Item", command=save_new)
    save_btn.pack(pady=15)

# Functions 
def close_app():
    app.destroy()

# Exit Button
exit_button = ctk.CTkButton(app, text="Exit", command=close_app, fg_color="red", hover_color="darkred")
exit_button.pack(pady=10)

app.focus_force() # Ensure window is focused so scanner keystrokes are caught
# Run the app
app.mainloop()
