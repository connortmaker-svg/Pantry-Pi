while True:
    try:
        scan = input("Scan the Barcode: ")
        if scan.strip():
            print(f"Barcode scanned: {scan}")
        else:
            print("No barcode scanned.")
    except KeyboardInterrupt:
        print("\nExiting...")
        break