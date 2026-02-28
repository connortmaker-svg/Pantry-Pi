import json

FILE_PATH = 'Testing Scripts/data.json'


def load_data():
    try:
        with open(FILE_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def add_new_item(barcode):
    print(f"/n Adding New Product: {barcode}")
    name = input("Item Name:").strip()
    price = input("Price: ").strip()
    qty = input("Quantity:").strip()
    
    inventory[barcode] = {
        "name" : name,
        "price" : price,
        "stock" : qty
    }

    save_data(inventory)
    print("Item Saved into Inventory")
    
inventory = load_data()

while True:
    try:
        scan = input("Start Scanning a Barcode:  ").strip()
        if not scan:
            continue
        if scan.lower() == 'q':
            break

        if scan in inventory:
            item = inventory[scan]
            print(f"Product: {item['name']}")
            print(f"Price:   ${item['price']}")
            print(f"Stock:   {item['stock']} units\n")
        else:
            print(f"Barcode {scan} not found in inventory")
            choice = input("Would you Life to add it now? (y/n): ").lower()
            if choice == 'y':
                add_new_item(scan)
    except KeyboardInterrupt:
        break