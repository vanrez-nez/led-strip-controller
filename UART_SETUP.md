## UART Configuration in Raspberry Pi 3B

To configure your Raspberry Pi 3B to work properly with UART (for communication with your ESP32), follow these step-by-step instructions See more in [Official Docs](https://github.com/raspberrypi/documentation/blob/develop/documentation/asciidoc/computers/configuration/uart.adoc):

1. Understand the UARTs on Raspberry Pi 3B

On the Raspberry Pi 3B:
	•	Primary UART is UART1 (mini UART) → /dev/ttyS0 (default).
	•	Secondary UART is UART0 (PL011) → /dev/ttyAMA0.

However, the mini UART is less capable (prone to baud rate issues because it’s linked to the CPU clock). For reliability, it’s better to switch the PL011 UART (UART0) to the GPIO pins.

2. Reconfigure UARTs

We will disable Bluetooth to free up UART0 (PL011) and map it to /dev/serial0 (GPIO 14 and 15).

Steps:
	1.	Edit /boot/config.txt:
Open the configuration file:

sudo nano /boot/config.txt


	2.	Add the following lines to disable Bluetooth and enable UART0:

enable_uart=1
dtoverlay=disable-bt

	•	enable_uart=1: Enables the UART hardware.
	•	dtoverlay=disable-bt: Disables Bluetooth to free up /dev/ttyAMA0 for GPIO 14/15.

	3.	Disable the Bluetooth modem service:

sudo systemctl disable hciuart


	4.	Reboot the Raspberry Pi:

sudo reboot

3. Verify the UART Configuration

After reboot, check that UART0 (PL011) is now mapped to /dev/serial0:

Check UART Mapping:

ls -l /dev/serial*

You should see something like this:

/dev/serial0 -> ttyAMA0

	•	/dev/serial0 → PL011 UART (ttyAMA0).
	•	If it still points to /dev/ttyS0, double-check the config.txt changes.

Check UART Availability:

dmesg | grep tty

You should see a line like:

serial0: ttyAMA0 at MMIO 0x3f201000 (irq = 99, base_baud = 0) is a PL011 rev2

4. Connect ESP32 to Raspberry Pi

Ensure your UART wiring is correct:

Raspberry Pi Pin	ESP32 Pin	Direction
GPIO 15 (RX)	ESP32 TX (17)	RPi ← ESP32
GPIO 14 (TX)	ESP32 RX (18)	RPi → ESP32
GND	GND	Common Ground

5. Test UART Communication

Raspberry Pi Python Script:

Use /dev/serial0 in your Python code:

import serial
import time

# Initialize UART on /dev/serial0
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)

print("Raspberry Pi UART Communication with ESP32")

try:
    while True:
        # Send data to ESP32
        message = "Hello ESP32!"
        ser.write((message + "\n").encode('utf-8'))
        print(f"Sent: {message}")

        # Check for incoming data
        if ser.in_waiting > 0:
            incoming_data = ser.readline().decode('utf-8').strip()
            print(f"Received: {incoming_data}")

        time.sleep(1)
except KeyboardInterrupt:
    print("Program exited.")
    ser.close()

ESP32 Code:

Ensure your ESP32 is reading from UART2 and sending back responses:

#define RXD2 18  // ESP32 RX
#define TXD2 17  // ESP32 TX

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2); // Initialize UART2
  Serial.println("UART2 initialized...");
}

void loop() {
  // Send data to Raspberry Pi
  Serial2.println("Hello Raspberry Pi!");
  Serial.println("Sent: Hello Raspberry Pi!");

  // Check for incoming data
  if (Serial2.available()) {
    String data = Serial2.readStringUntil('\n');
    Serial.print("Received from Raspberry Pi: ");
    Serial.println(data);
  }
  delay(1000);
}

6. Test Communication
	1.	Run the Python script on the Raspberry Pi.
	2.	Monitor the ESP32 using the Serial Monitor (115200 baud).
	3.	You should see:
	•	Raspberry Pi sending: Hello ESP32!
	•	ESP32 replying: Hello Raspberry Pi!

Summary of Steps
	1.	Disable Bluetooth on the Raspberry Pi to free UART0 (PL011).
	2.	Edit /boot/config.txt:

enable_uart=1
dtoverlay=disable-bt


	3.	Reboot and verify /dev/serial0 points to /dev/ttyAMA0.
	4.	Wire UART GPIO 14 (TX) and 15 (RX) to the ESP32’s RX/TX pins.
	5.	Test communication using Python (on RPi) and Arduino code (on ESP32).

This setup ensures reliable UART communication using the PL011 UART on the Raspberry Pi 3B. 🚀 Let me know if you face any issues!