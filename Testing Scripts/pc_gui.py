import customtkinter as ctk
import json
import os

# --- Data Handling ---
FILE_PATH = 'Database/inventory.json'
CATEGORIES_PATH = 'Database/categories.json'

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
app.geometry("500x700")

scanner_status = "Status: USB Scanner Active (Ready to Scan)"

title_label = ctk.CTkLabel(app, text="Last Scanned Item: ", font=("Arial", 24, "bold"))
title_label.pack(pady=(20,5))

readout_label = ctk.CTkLabel(app, text="Waiting...", font=("Arial", 40, "bold"), text_color="#00FF00")
readout_label.pack(pady=5)

info_frame = ctk.CTkFrame(app)
info_frame.pack(pady=10, padx=20, fill="x")

# --- Grid for Displaying Information ---
top_class_label = ctk.CTkLabel(info_frame, text="Top Level: -", font=("Arial", 16))
top_class_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)

sec_class_label = ctk.CTkLabel(info_frame, text="Sec Level: -", font=("Arial", 16))
sec_class_label.grid(row=0, column=1, sticky="w", padx=10, pady=2)

item_name_label = ctk.CTkLabel(info_frame, text="Name: -", font=("Arial", 16))
item_name_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)

temp_class_label = ctk.CTkLabel(info_frame, text="Temp: -", font=("Arial", 16))
temp_class_label.grid(row=1, column=1, sticky="w", padx=10, pady=2)

weight_class_label = ctk.CTkLabel(info_frame, text="Weight: -", font=("Arial", 16))
weight_class_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)

qty_label = ctk.CTkLabel(info_frame, text="Qty: -", font=("Arial", 16))
qty_label.grid(row=2, column=1, sticky="w", padx=10, pady=2)

location_label = ctk.CTkLabel(info_frame, text="Location: -", font=("Arial", 16))
location_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=2)

# Make columns expand evenly
info_frame.grid_columnconfigure((0, 1), weight=1)

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
        loc = item.get("location", {})
        
        top_class_label.configure(text=f"Top Level: {item.get('top_level_class', 'N/A')}")
        sec_class_label.configure(text=f"Sec Level: {item.get('second_level_class', 'N/A')}")
        item_name_label.configure(text=f"Name: {item.get('item_name', 'N/A')}")
        temp_class_label.configure(text=f"Temp: {item.get('temp_class', 'N/A')}")
        weight_class_label.configure(text=f"Weight: {item.get('weight_class', 'N/A')}")
        qty_label.configure(text=f"Qty: {item.get('total_qty', 'N/A')}")
        
        if isinstance(loc, dict):
            loc_str = f"Rack: {loc.get('rack_unit', 'N/A')} | Shelf: {loc.get('shelf_unit', 'N/A')} | Space: {loc.get('space_on_shelf', 'N/A')}"
        else:
            loc_str = str(loc)
            
        location_label.configure(text=f"Location: {loc_str}")
        
        status_label.configure(text=f"Status: Item Found", text_color="#00FF00")
        prompt_item_action(barcode)
    else:
        top_class_label.configure(text="Top Level: -")
        sec_class_label.configure(text="Sec Level: -")
        item_name_label.configure(text="Name: -")
        temp_class_label.configure(text="Temp: -")
        weight_class_label.configure(text="Weight: -")
        qty_label.configure(text="Qty: -")
        location_label.configure(text="Location: -")
        
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

# --- Action Menus ---
def prompt_item_action(barcode):
    popup = ctk.CTkToplevel(app)
    popup.title("Item Action")
    popup.geometry("350x250")
    popup.transient(app)
    popup.grab_set()

    item = inventory[barcode]
    
    header = ctk.CTkLabel(popup, text=f"Action for: {item.get('item_name', 'Unknown')}", font=("Arial", 16, "bold"))
    header.pack(pady=(10, 10))

    def add_qty():
        ask_qty(barcode, True, popup)

    def del_qty():
        ask_qty(barcode, False, popup)
        
    def scan_loc():
        ask_loc(barcode, popup)
        
    btn_add = ctk.CTkButton(popup, text="Add Quantity to Location", command=add_qty)
    btn_add.pack(pady=5)
    
    btn_del = ctk.CTkButton(popup, text="Delete Quantity from Location", command=del_qty)
    btn_del.pack(pady=5)
    
    btn_loc = ctk.CTkButton(popup, text="Scan in a New Location", command=scan_loc)
    btn_loc.pack(pady=5)
    
    btn_cancel = ctk.CTkButton(popup, text="Cancel", fg_color="gray", command=popup.destroy)
    btn_cancel.pack(pady=(10, 5))
    
def ask_qty(barcode, is_add, parent_popup):
    qty_popup = ctk.CTkToplevel(parent_popup)
    qty_popup.title("Add Quantity" if is_add else "Remove Quantity")
    qty_popup.geometry("300x180")
    qty_popup.transient(parent_popup)
    qty_popup.grab_set()
    
    label = ctk.CTkLabel(qty_popup, text="Enter quantity to " + ("add:" if is_add else "remove:"))
    label.pack(pady=10)
    
    entry = ctk.CTkEntry(qty_popup)
    entry.pack(pady=5)
    entry.focus()
    
    def submit(event=None):
        val = entry.get().strip()
        if val.isdigit():
            current_qty = 0
            try:
                current_qty = int(inventory[barcode].get("total_qty", "0"))
            except ValueError:
                pass
            change = int(val)
            if is_add:
                new_qty = current_qty + change
            else:
                new_qty = max(0, current_qty - change)
                
            inventory[barcode]["total_qty"] = str(new_qty)
            save_data(inventory)
            
            qty_label.configure(text=f"Qty: {new_qty}")
            status_label.configure(text=f"Status: Quantity Updated to {new_qty}", text_color="#00FF00")
            
            qty_popup.destroy()
            parent_popup.destroy()
            app.focus_force()
            
    btn = ctk.CTkButton(qty_popup, text="Submit", command=submit)
    btn.pack(pady=10)
    
    btn_cancel = ctk.CTkButton(qty_popup, text="Cancel", fg_color="gray", command=qty_popup.destroy)
    btn_cancel.pack(pady=0)
    
    qty_popup.bind("<Return>", submit)

def ask_loc(barcode, parent_popup):
    loc_popup = ctk.CTkToplevel(parent_popup)
    loc_popup.title("New Location")
    loc_popup.geometry("300x180")
    loc_popup.transient(parent_popup)
    loc_popup.grab_set()
    
    label = ctk.CTkLabel(loc_popup, text="Scan New Location:")
    label.pack(pady=10)
    
    entry = ctk.CTkEntry(loc_popup)
    entry.pack(pady=5)
    entry.focus()
    
    def submit(event=None):
        val = entry.get().strip()
        if val:
            inventory[barcode]["location"] = val
            save_data(inventory)
            
            location_label.configure(text=f"Location: {val}")
            status_label.configure(text=f"Status: Location Updated", text_color="#00FF00")
            
            loc_popup.destroy()
            parent_popup.destroy()
            app.focus_force()
            
    btn = ctk.CTkButton(loc_popup, text="Submit", command=submit)
    btn.pack(pady=10)
    
    btn_cancel = ctk.CTkButton(loc_popup, text="Cancel", fg_color="gray", command=loc_popup.destroy)
    btn_cancel.pack(pady=0)
    
    loc_popup.bind("<Return>", submit)

# --- Sequential Question Wizard ---
def prompt_add_item(barcode):
    popup = ctk.CTkToplevel(app)
    popup.title("Add New Product")
    popup.geometry("450x300")
    popup.transient(app)
    popup.grab_set() # Focus on popup
    
    # Load category tree
    try:
        with open(CATEGORIES_PATH, 'r') as f:
            categories_tree = json.load(f)
    except FileNotFoundError:
        categories_tree = {"Misc": ["Other"]}
        
    steps = [
        {"desc": "Select Top Level Class:", "type": "dropdown", "options": list(categories_tree.keys()), "key": "top_level_class"},
        {"desc": "Select Second Level Class:", "type": "dropdown", "options": [], "key": "second_level_class"},
        {"desc": "Select Temperature Class:", "type": "dropdown", "options": ["shelf goods", "dry perishables", "refrigerated things", "freezer things"], "key": "temp_class"},
        {"desc": "What is the specific item name?", "type": "entry", "key": "item_name"},
        {"desc": "What is the weight class? (e.g., 12oz)", "type": "entry", "key": "weight_class"},
        {"desc": "What is the total quantity?", "type": "entry", "key": "total_qty"},
        {"desc": "**SCAN IN:** Scan Location Barcode:", "type": "entry", "key": "location_barcode"}
    ]
    
    answers = {}
    current_step = 0
    widget = None
    
    # UI Elements for popup
    header = ctk.CTkLabel(popup, text=f"Adding Barcode: {barcode}", font=("Arial", 14), text_color="gray")
    header.pack(pady=(10, 5))
    
    question_label = ctk.CTkLabel(popup, text="", font=("Arial", 18, "bold"), wraplength=400)
    question_label.pack(pady=10)
    
    input_frame = ctk.CTkFrame(popup, fg_color="transparent")
    input_frame.pack(pady=5)
    
    # Function to render the current step
    def render_step():
        nonlocal widget
        if widget is not None:
            widget.destroy()
            
        if current_step >= len(steps):
            finish_wizard()
            return
            
        step = steps[current_step]
        question_label.configure(text=step["desc"])
        
        if step["key"] == "second_level_class":
            top_val = answers.get("top_level_class", "Misc")
            step["options"] = categories_tree.get(top_val, ["Other"])
            
        if step["type"] == "dropdown":
            widget_var = ctk.StringVar(value=step["options"][0])
            widget = ctk.CTkOptionMenu(input_frame, variable=widget_var, values=step["options"], width=300)
            widget.var = widget_var
            widget.pack(pady=10)
            next_btn.configure(text="Next")
        else:
            widget = ctk.CTkEntry(input_frame, width=300)
            widget.pack(pady=10)
            widget.focus()
            
            if current_step == len(steps)-1:
                next_btn.configure(text="Complete Scan In")
            else:
                next_btn.configure(text="Next")

    def next_step(event=None):
        nonlocal current_step
        step = steps[current_step]
        
        if step["type"] == "dropdown":
            ans = widget.var.get()
        else:
            ans = widget.get().strip()
            
        answers[step["key"]] = ans
        current_step += 1
        render_step()

    def finish_wizard():
        inventory[barcode] = {
            "top_level_class": answers.get("top_level_class"),
            "second_level_class": answers.get("second_level_class"),
            "item_name": answers.get("item_name"),
            "temp_class": answers.get("temp_class"),
            "weight_class": answers.get("weight_class"),
            "total_qty": answers.get("total_qty"),
            "location": answers.get("location_barcode", "")
        }
        save_data(inventory)
        
        # Update Main UI
        loc_str = answers.get('location_barcode', '')
        
        top_class_label.configure(text=f"Top Level: {answers.get('top_level_class')}")
        sec_class_label.configure(text=f"Sec Level: {answers.get('second_level_class')}")
        item_name_label.configure(text=f"Name: {answers.get('item_name')}")
        temp_class_label.configure(text=f"Temp: {answers.get('temp_class')}")
        weight_class_label.configure(text=f"Weight: {answers.get('weight_class')}")
        qty_label.configure(text=f"Qty: {answers.get('total_qty')}")
        location_label.configure(text=f"Location: {loc_str}")
        
        status_label.configure(text="Status: Item Saved into Inventory", text_color="#00FF00")
        
        popup.destroy()
        app.focus_force() # Return focus to main app to keep scanning

    next_btn = ctk.CTkButton(popup, text="Next", command=next_step)
    next_btn.pack(pady=15)
    
    # Also submit on enter key
    popup.bind("<Return>", next_step)
    render_step()

# Functions 
def close_app():
    app.destroy()

# Exit Button
exit_button = ctk.CTkButton(app, text="Exit", command=close_app, fg_color="red", hover_color="darkred")
exit_button.pack(pady=10)

app.focus_force() # Ensure window is focused so scanner keystrokes are caught
# Run the app
app.mainloop()
