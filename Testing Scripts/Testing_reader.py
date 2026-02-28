# inventory = {
#     "0613008756451": {
#         "name": "Arizona Iced Tea",
#         "price": 0.99,
#         "size": "23oz",
#         "stock": 50
#     },
#     "0077890204023": {
#         "name": "Cranberry Sauce",
#         "price": 3.49,
#         "size": "9.25oz",
#         "stock": 12
#     }
# }

import json

try:
    with open('Testing Scripts/data.json', 'r') as file:
        inventory = json.load(file)
except FileNotFoundError:
    print("Error: 'database_t.json' not found! Make sure it's in the same folder.")
    inventory = {}

while True:
    try:
        scan = input("Scan the Barcode: ").strip()
        if scan:
            if scan in inventory:
                item = inventory[scan]
                print(f"--- Item Found ---")
                print(f"Product: {item['name']}")
                print(f"Price:   ${item['price']}")
                print(f"Stock:   {item['stock']} units")
            else:
                print(f"Unknown Barcode: {scan}")
        else:
            print("No input detected.")
    except KeyboardInterrupt:
        print("\nExiting...")
        break