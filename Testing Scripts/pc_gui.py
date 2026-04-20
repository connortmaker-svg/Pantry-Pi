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

sec_barcode_label = ctk.CTkLabel(info_frame, text="Sec. Barcode: -", font=("Arial", 16))
sec_barcode_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=2)

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
        
        loc_str = f"Rack: {loc.get('rack_unit', 'N/A')} | Shelf: {loc.get('shelf_unit', 'N/A')} | Space: {loc.get('space_on_shelf', 'N/A')}"
        location_label.configure(text=f"Location: {loc_str}")
        
        sec_barcode_label.configure(text=f"Sec. Barcode: {item.get('secondary_barcode', 'None')}")
        status_label.configure(text=f"Status: Item Found", text_color="#00FF00")
    else:
        top_class_label.configure(text="Top Level: -")
        sec_class_label.configure(text="Sec Level: -")
        item_name_label.configure(text="Name: -")
        temp_class_label.configure(text="Temp: -")
        weight_class_label.configure(text="Weight: -")
        qty_label.configure(text="Qty: -")
        location_label.configure(text="Location: -")
        sec_barcode_label.configure(text="Sec. Barcode: -")
        
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
        {"desc": "Location - What Rack Unit?", "type": "entry", "key": "rack_unit"},
        {"desc": "Location - What Shelf Unit?", "type": "entry", "key": "shelf_unit"},
        {"desc": "Location - What Space on the Shelf?", "type": "entry", "key": "space_on_shelf"},
        {"desc": "**SCAN IN:** Scan the secondary barcode now:", "type": "entry", "key": "secondary_barcode"}
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
            "location": {
                "rack_unit": answers.get("rack_unit"),
                "shelf_unit": answers.get("shelf_unit"),
                "space_on_shelf": answers.get("space_on_shelf")
            },
            "secondary_barcode": answers.get("secondary_barcode")
        }
        save_data(inventory)
        
        # Update Main UI
        loc_str = f"Rack: {answers.get('rack_unit')} | Shelf: {answers.get('shelf_unit')} | Space: {answers.get('space_on_shelf')}"
        
        top_class_label.configure(text=f"Top Level: {answers.get('top_level_class')}")
        sec_class_label.configure(text=f"Sec Level: {answers.get('second_level_class')}")
        item_name_label.configure(text=f"Name: {answers.get('item_name')}")
        temp_class_label.configure(text=f"Temp: {answers.get('temp_class')}")
        weight_class_label.configure(text=f"Weight: {answers.get('weight_class')}")
        qty_label.configure(text=f"Qty: {answers.get('total_qty')}")
        location_label.configure(text=f"Location: {loc_str}")
        sec_barcode_label.configure(text=f"Sec. Barcode: {answers.get('secondary_barcode')}")
        
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
