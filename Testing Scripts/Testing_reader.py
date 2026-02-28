while True:
    try:
        scan = input("Scan the Barcode: ")
        if scan.strip():
            if scan == "0613008756451":
                print("Arizona")
            print(f"Barcode scanned: {scan}")
        else:
            print("No barcode scanned.")
    except KeyboardInterrupt:
        print("\nExiting...")
        break