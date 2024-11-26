import pyaudio
import numpy as np
import time

# Constants for audio stream configuration
CHUNK = 2048              # Buffer size
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1              # Mono audio
RATE = 44100              # Default sampling rate in Hz

def list_input_devices(p):
    """Lists all available audio input devices."""
    print("Available audio input devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            print(f"Device {i}: {device_info['name']}")

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

    print("Monitoring audio levels. Press Ctrl+C to stop.")

    max_rms = 1e-6  # Initialize to prevent division by zero

    try:
        while True:
            try:
                # Read audio data from the stream
                data = stream.read(CHUNK, exception_on_overflow=False)
            except IOError as e:
                print(f"\nError reading audio stream: {e}")
                continue  # Skip this iteration

            if not data:
                print("\nNo data received from the audio stream.")
                continue  # Skip this iteration

            # Convert byte data to numpy array and to float
            audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)

            # Check if audio_data is empty
            if audio_data.size == 0:
                print("\nAudio data array is empty.")
                continue  # Skip this iteration

            # Check for invalid values in audio_data
            if not np.all(np.isfinite(audio_data)):
                print("\nAudio data contains invalid values.")
                continue  # Skip this iteration

            # Compute RMS of the audio data
            power = np.mean(np.square(audio_data))

            # Check for invalid power value
            if np.isnan(power) or power < 0:
                print("\nPower calculation resulted in an invalid value.")
                continue  # Skip this iteration

            rms = np.sqrt(power)

            # Check for NaN in RMS
            if np.isnan(rms):
                print("\nRMS calculation resulted in NaN.")
                continue  # Skip this iteration

            # Update max_rms
            max_rms = max(max_rms, rms, 1e-6)  # Prevent division by zero

            # Scale RMS value to a suitable level for display
            level = int((rms / max_rms) * 50)  # Scale between 0 and 50

            # Ensure level is within display bounds
            level = max(0, min(level, 50))

            # Create a text-based level bar
            bar = "#" * level

            # Display the audio level bar
            print(f"\rLevel: [{bar:<50}] RMS: {rms:.2f}", end="")

            # Small delay to reduce CPU usage
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        # Properly close the stream
        try:
            if stream.is_active():
                stream.stop_stream()
            stream.close()
        except Exception as e:
            print(f"Error closing stream: {e}")
        p.terminate()

if __name__ == "__main__":
    main()