import customtkinter as ctk
import json
import os

# --- Data Handling ---
FILE_PATH = 'Database/inventory.json'

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
app.geometry("500x550")

scanner_status = "Status: USB Scanner Active (Ready to Scan)"

title_label = ctk.CTkLabel(app, text="Last Scanned Item: ", font=("Arial", 24, "bold"))
title_label.pack(pady=(20,5))

readout_label = ctk.CTkLabel(app, text="Waiting...", font=("Arial", 40, "bold"), text_color="#00FF00")
readout_label.pack(pady=5)

info_frame = ctk.CTkFrame(app)
info_frame.pack(pady=10, padx=20, fill="x")

top_class_label = ctk.CTkLabel(info_frame, text="Top Level Class: -", font=("Arial", 16))
top_class_label.pack(anchor="w", padx=10, pady=2)

sec_class_label = ctk.CTkLabel(info_frame, text="Second Level Class: -", font=("Arial", 16))
sec_class_label.pack(anchor="w", padx=10, pady=2)

item_name_label = ctk.CTkLabel(info_frame, text="Item Name: -", font=("Arial", 16))
item_name_label.pack(anchor="w", padx=10, pady=2)

temp_class_label = ctk.CTkLabel(info_frame, text="Temp Class: -", font=("Arial", 16))
temp_class_label.pack(anchor="w", padx=10, pady=2)

weight_class_label = ctk.CTkLabel(info_frame, text="Weight Class: -", font=("Arial", 16))
weight_class_label.pack(anchor="w", padx=10, pady=2)

qty_label = ctk.CTkLabel(info_frame, text="Total Qty: -", font=("Arial", 16))
qty_label.pack(anchor="w", padx=10, pady=2)

status_label = ctk.CTkLabel(app, text=scanner_status, font=("Arial", 14), text_color="gray")
status_label.pack(pady=(5, 5))

# --- USB Scanner Logic ---
barcode_buffer = ""

def process_barcode(barcode):
    barcode = barcode.strip()
    if not barcode:
        return
        
    readout_label.configure(text=barcode)
    
    if barcode in inventory:
        item = inventory[barcode]
        top_class_label.configure(text=f"Top Level Class: {item.get('top_level_class', 'N/A')}")
        sec_class_label.configure(text=f"Second Level Class: {item.get('second_level_class', 'N/A')}")
        item_name_label.configure(text=f"Item Name: {item.get('item_name', 'N/A')}")
        temp_class_label.configure(text=f"Temp Class: {item.get('temp_class', 'N/A')}")
        weight_class_label.configure(text=f"Weight Class: {item.get('weight_class', 'N/A')}")
        qty_label.configure(text=f"Total Qty: {item.get('total_qty', 'N/A')}")
        status_label.configure(text=f"Status: Item Found", text_color="#00FF00")
    else:
        top_class_label.configure(text="Top Level Class: -")
        sec_class_label.configure(text="Second Level Class: -")
        item_name_label.configure(text="Item Name: -")
        temp_class_label.configure(text="Temp Class: -")
        weight_class_label.configure(text="Weight Class: -")
        qty_label.configure(text="Total Qty: -")
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
    popup.geometry("350x450")
    popup.transient(app)
    popup.grab_set() # Focus on popup
    
    ctk.CTkLabel(popup, text=f"Adding Barcode:\n{barcode}", font=("Arial", 16, "bold")).pack(pady=10)
    
    top_class_entry = ctk.CTkEntry(popup, placeholder_text="Top Level Class", width=250)
    top_class_entry.pack(pady=5)
    
    sec_class_entry = ctk.CTkEntry(popup, placeholder_text="Second Level Class", width=250)
    sec_class_entry.pack(pady=5)

    item_name_entry = ctk.CTkEntry(popup, placeholder_text="Item Specific Name", width=250)
    item_name_entry.pack(pady=5)

    temp_class_entry = ctk.CTkEntry(popup, placeholder_text="Temp Class", width=250)
    temp_class_entry.pack(pady=5)

    weight_class_entry = ctk.CTkEntry(popup, placeholder_text="Weight Class", width=250)
    weight_class_entry.pack(pady=5)
    
    qty_entry = ctk.CTkEntry(popup, placeholder_text="Total Quantity", width=250)
    qty_entry.pack(pady=5)
    
    def save_new():
        top_c = top_class_entry.get().strip()
        sec_c = sec_class_entry.get().strip()
        name = item_name_entry.get().strip()
        temp_c = temp_class_entry.get().strip()
        weight_c = weight_class_entry.get().strip()
        qty = qty_entry.get().strip()
        
        inventory[barcode] = {
            "top_level_class": top_c,
            "second_level_class": sec_c,
            "item_name": name,
            "temp_class": temp_c,
            "weight_class": weight_c,
            "total_qty": qty
        }
        save_data(inventory)
        
        # Update UI
        top_class_label.configure(text=f"Top Level Class: {top_c}")
        sec_class_label.configure(text=f"Second Level Class: {sec_c}")
        item_name_label.configure(text=f"Item Name: {name}")
        temp_class_label.configure(text=f"Temp Class: {temp_c}")
        weight_class_label.configure(text=f"Weight Class: {weight_c}")
        qty_label.configure(text=f"Total Qty: {qty}")
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
