# audio_dev_utils.py

import pyaudio
import time
import numpy as np
import dsp.config as config

def list_input_devices(p):
    """Lists all available audio input devices."""
    print("Available audio input devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info["maxInputChannels"] > 0:
            print(f"Device {i}: {device_info['name']}")

def start_stream(callback):
    """Starts the audio stream and continuously feeds data to the callback."""
    p = pyaudio.PyAudio()
    # list_input_devices(p)
    frames_per_buffer = int(config.RATE / config.FPS)
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=config.RATE,
                    input=True,
                    frames_per_buffer=frames_per_buffer,
                    input_device_index=config.DEVICE_INDEX)
    overflows = 0
    prev_ovf_time = time.time()
    try:
        while True:
            try:
                # Read audio data
                data = stream.read(frames_per_buffer, exception_on_overflow=False)
                y = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                callback(y)
            except IOError as e:
                overflows += 1
                current_time = time.time()
                if current_time > prev_ovf_time + 1:
                    prev_ovf_time = current_time
                    print(f'Audio buffer has overflowed {overflows} times. Error: {e}')
    except KeyboardInterrupt:
        print("Audio stream interrupted by user.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()