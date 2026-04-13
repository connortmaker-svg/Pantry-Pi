# Wiring Guides #

# VCC -> 5V (Pin 2)
# GND -> GND (Pin 6)
# Tx -> Rx (Pin 8)
# Rx -> Tx (Pin 10)

# Turning the UART debug on
# sudo raspi-config -> Interfacing Options -> Serial Port -> No -> Yes -> Finish
# Open /boot/firmware/config.txt
# dtoverlay=uart0-pi5

# Pip install pyserial

import serial 
import time

# Check that the Scanner is Connected and Turned on
try:
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        timeout=1
    )
    print("Scanner is Ready")
# Any errors that occur due to the scanner not being connected or turned on will be printed here
except Exception as e:
    print(f"Error: {e}")

# Loop to read the barcode data
try:
    while True:
        if ser.in_waiting > 0:
            barcode_data = ser.readline().decode('utf-8').strip()
            print(f"Scanned Code: {barcode_data}")

# Stop the program when the user presses Ctrl+C
except KeyboardInterrupt:
    print("Program Stopped")
    ser.close()
    print("Scanner Non-Active")