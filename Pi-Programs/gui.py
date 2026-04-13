import customtkinter as ctk
import serial

# Setup Serial Scanner

try:
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        timeout=1
    )
    print("Scanner is Ready")
except Exception as e:
    print(f"Error: {e}")

# GUI Setup
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.overrideredirect(True) # Hidding the Title Bar for the OS
app.geometry("400x300") # Resolution

# Title Elements
title_lable = ctk.CTkLabel(app, text="Last Scanned Item: ", font=("Arial", 24, "bold"))
title_lable.pack(pady=(30,10))

# Readout Labels
readout_label = ctk.CTkLabel(app, text="Waiting...", font=("Arial", 40, "bold"), text_color="#00FF00")
readout_label.pack(pady=20)

# Status Bar
status_label = ctk.CTkLabel(app, text=scanner_status, font=("Arial", 14), text_color="gray")
status_label.pack(pady=(10, 20))

# Functions 

def check_scanner():
    if scanner and scanner.in_waiting > 0:
        try:
            barcode_data = scanner.readline().decode('utf-8').strip()
            if barcode_data:
                readout_label.configure(text=barcode_data)
        except Exception as e:
            print(f"Error: {e}")
    app.after(100, check_scanner)
                
def close_app():
    if ser.is_open:
        ser.close()
        print("Scanner Closed")
    app.destroy()

# Exit Button
exit_button = ctk.CTkButton(app, text="Exit", command=close_app)
exit_button.pack(pady=20)

app.after(100, check_scanner)

# Run the app
app.mainloop()