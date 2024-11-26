import pyaudio
import numpy as np
import time
import RPi.GPIO as GPIO

# Constants for audio stream configuration
CHUNK = 512              # Buffer size
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 2              # Mono audio
RATE = 44100              # Default sampling rate in Hz

# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
# List of GPIO pins where LEDs are connected
led_pins = [17, 27, 22, 5, 6]
# Set up each LED pin as an output and initialize it to LOW (off)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def list_input_devices(p):
    """Lists all available audio input devices."""
    print("Available audio input devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            print(f"Device {i}: {device_info['name']}")

def get_audio_level(stream, max_rms):
    """Reads audio data from the stream and returns the audio level."""
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
    except IOError as e:
        print(f"\nError reading audio stream: {e}")
        return None, max_rms

    if not data:
        print("\nNo data received from the audio stream.")
        return None, max_rms

    # Convert byte data to numpy array and to float
    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)

    # Check if audio_data is empty or contains invalid values
    if audio_data.size == 0 or not np.all(np.isfinite(audio_data)):
        print("\nInvalid audio data.")
        return None, max_rms

    # Compute RMS of the audio data
    power = np.mean(np.square(audio_data))
    if np.isnan(power) or power < 0:
        print("\nInvalid power calculation.")
        return None, max_rms

    rms = np.sqrt(power)
    if np.isnan(rms):
        print("\nRMS calculation resulted in NaN.")
        return None, max_rms

    # Update max_rms to prevent division by zero
    max_rms = max(max_rms, rms, 1e-6)

    # Scale RMS value to a level between 0 and 5 (for 5 LEDs)
    level = int((rms / max_rms) * len(led_pins))
    level = max(0, min(level, len(led_pins)))  # Ensure level is within bounds

    return level, max_rms

def control_led(pin, state):
    """Controls an individual LED."""
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)

def set_leds(level):
    """Sets LEDs based on the audio level."""
    # Turn on LEDs up to the current level
    for i in range(len(led_pins)):
        if i < level:
            control_led(led_pins[i], True)
        else:
            control_led(led_pins[i], False)

def main():
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # List and select audio input device
    list_input_devices(p)
    device_index = int(input("Select device index: "))

    # Get device info
    device_info = p.get_device_info_by_index(device_index)
    print(f"Using device: {device_info['name']}")
    print(f"Device info: {device_info}")

    # Use device's default sample rate if possible
    RATE = int(device_info.get("defaultSampleRate", 44100))

    # Open audio input stream
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=CHUNK)
    except Exception as e:
        print(f"Could not open audio stream: {e}")
        p.terminate()
        return

    print("Monitoring audio levels and controlling LEDs. Press Ctrl+C to stop.")

    max_rms = 1e-6  # Initialize to prevent division by zero

    try:
        while True:
            level, max_rms = get_audio_level(stream, max_rms)
            if level is not None:
                set_leds(level)
            # Small delay to reduce CPU usage
            # time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopping...")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    finally:
        # Turn off all LEDs and clean up GPIO
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)
        GPIO.cleanup()

        # Properly close the audio stream
        try:
            if stream.is_active():
                stream.stop_stream()
            stream.close()
        except Exception as e:
            print(f"Error closing stream: {e}")
        p.terminate()

if __name__ == "__main__":
    main()