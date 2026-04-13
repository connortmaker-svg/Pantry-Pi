# Pantry-Pi


The Pi 5 uses 3.3V logic. Most Waveshare modules use 5V for power but 3.3V for data pins.

Scanner Pin,Raspberry Pi 5 Pin,Notes
VCC,Pin 2 or 4 (5V) ,Check manual; some versions use 3.3V.
GND,Pin 6 (Ground) ,
TX,Pin 10 (GPIO 15 / RX) ,Scanner Talker to Pi Listener.
RX,Pin 8 (GPIO 14 / TX) ,Pi Talker to Scanner Listener.