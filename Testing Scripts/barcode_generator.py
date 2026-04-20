import os

try:
    import barcode
    from barcode.writer import ImageWriter
except ImportError:
    print("Missing required libraries. Please install them by running:")
    print("pip install python-barcode pillow")
    exit(1)

def generate_location_barcodes(racks, shelves, spaces):
    output_dir = "Location_Barcodes"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nGenerating barcode images in '{output_dir}' folder...")
    
    # Code128 is the best barcode format for letters and numbers combined
    Code128 = barcode.get_barcode_class('code128')
    
    count = 0
    for rack in racks:
        for shelf in range(1, shelves + 1):
            for space in range(1, spaces + 1):
                location_code = f"{rack}-{shelf:02d}-{space:02d}"
                
                # Generate barcode image
                my_barcode = Code128(location_code, writer=ImageWriter())
                
                # Save as PNG
                filename = os.path.join(output_dir, location_code)
                my_barcode.save(filename)
                count += 1
                
    print(f"Success! Saved {count} barcode images to the '{output_dir}' directory.")
    print("You can now print these out and stick them to your shelves!")

if __name__ == "__main__":
    print("--- Pantry-Pi Location Barcode Generator ---")
    
    rack_input = input("Enter Rack letters separated by comma (e.g. A,B,C) [Default A]: ").strip()
    racks = [r.strip().upper() for r in rack_input.split(',')] if rack_input else ['A']
    
    try:
        shelves = int(input("How many shelves per rack? [Default 5]: ").strip() or 5)
        spaces = int(input("How many spaces per shelf? [Default 5]: ").strip() or 5)
    except ValueError:
        print("Invalid number. Falling back to default: 5.")
        shelves = 5
        spaces = 5
        
    generate_location_barcodes(racks, shelves, spaces)
