import serial
import time
from base.event_manager import EventManager
from collections import defaultdict

class UARTCommunication:
    def __init__(self, port='/dev/serial0', baudrate=9600, timeout=1):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        self.ser.reset_input_buffer()  # Flush input buffer
        self.ser.reset_output_buffer() # Flush output buffer
        self.event_manager = EventManager()
        print("Raspberry Pi UART Communication with ESP32 Initialized")

    def update(self):
        """
        Reads incoming data from the serial port and dispatches events if commands are received.
        """
        if self.ser.in_waiting > 0:
            incoming_data = self.ser.readline().decode('utf-8').strip()
            print(f"Received: {incoming_data}")
            self._parse_and_dispatch(incoming_data)

    def _parse_and_dispatch(self, message):
        """
        Parses the incoming message in the format cmd::name::key:value and dispatches events.
        """
        try:
            parts = message.split('::')
            if len(parts) < 2 or parts[0] != "cmd":
                print("Invalid command format")
                return

            command_name = parts[1]
            params = {}
            if len(parts) > 2:
                params = dict(param.split(':', 1) for param in parts[2].split(','))

            # Dispatch event to subscribed listeners
            self.event_manager.publish(command_name, params)

        except Exception as e:
            print(f"Error parsing command: {e}")

    def on(self, command_name, callback):
        """
        Subscribes a callback function to a specific command using the EventManager.
        """
        self.event_manager.subscribe(command_name, callback)

    def off(self, command_name, callback):
        """
        Removes a callback function from a specific command using the EventManager.
        """
        self.event_manager.unsubscribe(command_name, callback)

    def send(self, command_name, params=None):
        """
        Sends a command through the serial port.
        """
        params = params or {}
        param_string = ','.join(f"{key}:{value}" for key, value in params.items())
        message = f"cmd::{command_name}"
        if param_string:
            message += f"::{param_string}"
        self.ser.write((message + "\n").encode('utf-8'))
        print(f"Sent: {message}")

    def close(self):
        """
        Closes the serial port.
        """
        self.ser.close()
        print("Serial port closed")


# Example usage
if __name__ == "__main__":
    uart = UARTCommunication()

    # Example event handlers
    def status_handler(params):
        print(f"Status command received with params: {params}")

    def restart_handler(params):
        print(f"Restart command received with params: {params}")

    def ping_handler(params):
        print("Ping command received. Sending pong response...")
        uart.send("pong", {"timestamp": str(time.time())})

    # Subscribe to commands
    uart.on("status", status_handler)
    uart.on("restart", restart_handler)
    uart.on("ping", ping_handler)

    try:
        while True:
            # Check for updates
            uart.update()
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Program exited.")
        uart.close()