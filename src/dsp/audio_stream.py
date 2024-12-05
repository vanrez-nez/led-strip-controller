import pyaudio
import time
import numpy as np
import config as config

class AudioStream:
    def __init__(self):
        """Initialize the DSP Processor."""
        self.p = pyaudio.PyAudio()
        self.frames_per_buffer = int(config.DSP_RATE / config.DSP_FPS)
        self.stream = None
        self.audio_data = None  # Store the latest audio data
        self.running = False  # Indicates whether the stream is running

    def list_input_devices(self):
        """Lists all available audio input devices."""
        p = pyaudio.PyAudio()
        print("Available audio input devices:")
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:
                print(f"Device {i}: {device_info['name']}")
        p.terminate()

    def start(self):
        """Start the audio stream."""
        self.list_input_devices()
        if self.running:
            print("DSP Processor is already running.")
            return
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=config.DSP_RATE, input=True, frames_per_buffer=self.frames_per_buffer, input_device_index=config.DSP_DEVICE_INDEX)
        self.running = True

        print("DSP Processor started.")

    def stop(self):
        """Stop the audio stream."""
        if not self.running:
            print("DSP Processor is not running.")
            return

        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        self.running = False
        print("DSP Processor stopped.")

    def update(self):
        """Fetch the latest audio data. Store it in the `audio_data` property."""
        if not self.running:
            print("Warning: DSP Processor is not running. No data to update.")
            return None

        try:
            # Read audio data from the stream
            data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)
            self.audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            return self.audio_data
        except IOError as e:
            print(f"Error reading audio data: {e}")
            self.audio_data = None
            return None

    def __del__(self):
        """Clean up resources when the object is destroyed."""
        if self.running:
            self.stop()
        self.p.terminate()


# Example usage
if __name__ == "__main__":
    dsp = AudioStream()
    AudioStream.list_input_devices()

    try:
        dsp.start()
        while True:
            audio_data = dsp.update()
            if audio_data is not None:
                print(f"Audio data: {audio_data[:5]}")  # Example: Print first 5 samples
            time.sleep(0.1)  # Simulate periodic updates
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        dsp.stop()