# Raspberry Pi 5 Barcode Scanner Setup

This guide details how to use the Waveshare Barcode Scanner Module (1D/2D, QR Code Reader) with a Raspberry Pi 5 using UART/GPIO, and how to transmit data wirelessly to a PC via Bluetooth.

## 1. Wiring (Scanner to Pi 5)

Connecting the scanner via UART keeps USB ports free and is ideal for permanent, embedded applications.

The Pi 5 uses 3.3V logic. Most Waveshare modules use 5V for power but 3.3V for data pins. Always check your specific module version.

| Scanner Pin | Raspberry Pi 5 Pin    | Notes                                                    |
| :---------- | :-------------------- | :------------------------------------------------------- |
| **VCC**     | Pin 2 or 4 (5V)       | Check manual; some versions specifically require 3.3V.   |
| **GND**     | Pin 6 (Ground)        |                                                          |
| **TX**      | Pin 10 (GPIO 15 / RX) | Scanner's Talker to Pi's Listener.                       |
| **RX**      | Pin 8 (GPIO 14 / TX)  | Pi's Talker to Scanner's Listener.                       |

## 2. Configuration & Software

### Serial Port Setup

The Pi 5 requires specific configuration to enable the GPIO serial pins.

1. Open the terminal and run:
   ```bash
   sudo raspi-config
   ```
2. Navigate to **Interface Options -> Serial Port**.
3. Select **No** for the login shell.
4. Select **Yes** to enable serial port hardware.
5. **Pi 5 Specific Step:** Open `/boot/firmware/config.txt` and add the following line to the bottom of the file:
   ```ini
   dtoverlay=uart0-pi5
   ```
6. Reboot the Pi.

### Testing the Scanner

To verify your wiring and configuration are correct, you can use the provided `scanner.py` script.

1. Install the required Python library:
   ```bash
   pip install pyserial
   ```
2. Run the test script:
   ```bash
   python scanner.py
   ```
3. Scan a barcode. If successful, you should see the scanned data printed in the terminal.

## 3. Wireless Connection to PC (Bluetooth)

To send scanner data wirelessly to a PC without a Wi-Fi router, you can configure the Pi as a Bluetooth "Server," making it appear as a wireless COM port to the remote PC.

### Pairing

Use `bluetoothctl` on the Pi to make it discoverable and pair it with the PC.
```bash
sudo bluetoothctl
power on
discoverable on
pairable on
```

### Service Setup

Edit the Bluetooth service to enable the Serial Port Profile (SPP).

1. Edit the service file: 
   ```bash
   sudo nano /etc/systemd/system/dbus-org.bluez.service
   ```
2. Add `-C` to the end of the `ExecStart` line to enable Compatibility mode.
3. Add a new line directly below that: 
   ```ini
   ExecStartPost=/usr/bin/sdptool add SP
   ```
4. Restart the service to apply changes:
   ```bash
   sudo systemctl daemon-reload && sudo systemctl restart bluetooth
   ```

### Implementation

Use the Python `socket` library in your scanning script to transmit the parsed UART data to the PC via Bluetooth RFCOMM.

## 4. Screen Setup (GUI)

The Python GUI application (`gui.py`) is built using `customtkinter` and is designed to display the scanned output locally on a 400x300 touchscreen or HDMI display connected to the Pi.

1. Install the CustomTkinter UI library:
   ```bash
   pip install customtkinter
   ```
2. If you are running the script over SSH and getting display errors, you must export the display variable so the GUI appears on the screen physically connected to the Pi:
   ```bash
   export DISPLAY=:0
   ```

## 5. PM2 Service Setup

To keep the application running continuously in the background and ensure it automatically restarts on boot or in case of a crash, you should set it up using the Node.js PM2 process manager.

1. Install Node.js & npm (if not already installed):
   ```bash
   sudo apt update
   sudo apt install nodejs npm -y
   ```
2. Install PM2 globally:
   ```bash
   sudo npm install pm2 -g
   ```
3. Start the GUI script via PM2 (run this inside the `Pi-Programs` directory):
   ```bash
   pm2 start gui.py --name "pantry-scanner" --interpreter python3
   ```
4. Save the PM2 process list so it respawns on reboot:
   ```bash
   pm2 save
   ```
5. Configure PM2 to start automatically on system boot:
   ```bash
   pm2 startup
   ```
   *(Running this command will output another command that you must copy and paste into your terminal to finalize the startup configuration.)*