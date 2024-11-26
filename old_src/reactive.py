# reactive.py

import numpy as np
import dsp.config as config
import time
import dsp
import audio_dev_utils
import led_utils

# Initialize rolling buffer
y_roll = np.zeros(config.BUFFER_SIZE)  # e.g., 1764 samples

# Initialize FFT window
fft_window = np.hamming(config.N_FFT)  # e.g., 2048 samples

# Initialize Mel filterbank
dsp.create_mel_bank()  # Initializes mel_y with shape (5, 1025)

# Initialize smoothing filter
mel_smoothing = dsp.ExpFilter(np.zeros(config.N_FFT_BINS), alpha_decay=0.5, alpha_rise=0.5)

def audio_update(audio_samples):
    global y_roll
    # Normalize samples between -1.0 and 1.0
    y = audio_samples / np.iinfo(np.int16).max
    # Append new samples to the rolling buffer
    y_roll = np.roll(y_roll, -len(y))
    y_roll[-len(y):] = y
    # Concatenate rolling buffer for FFT
    y_data = y_roll.copy()

    # Check volume threshold
    vol = np.max(np.abs(y_data))
    if vol < config.MIN_VOLUME_THRESHOLD:
        print('No audio input. Volume below threshold.')
        # Optional: Avoid updating LEDs when volume is too low
        led_utils.set_levels([0] * config.N_FFT_BINS)
        return

    print(f"Volume: {vol}")  # Log volume

    # Pad y_data to match N_FFT
    if config.PAD_SIZE > 0:
        y_data_padded = np.pad(y_data, (0, config.PAD_SIZE), 'constant')
    else:
        y_data_padded = y_data

    # Apply window function
    y_data_windowed = y_data_padded * fft_window  # Shape: (N_FFT,)
    # print("y_data_windowed shape:", y_data_windowed.shape)  # Should be (2048,)

    # Compute FFT and get magnitude
    YS = np.abs(np.fft.rfft(y_data_windowed))  # Shape: (1025,)
    # print("YS shape:", YS.shape)  # Should be (1025,)

    # Compute Mel spectrogram
    mel_spec = np.dot(dsp.mel_y, YS)  # Shape: (5,)
    # print("mel_spec:", mel_spec)

    # Normalize the Mel spectrogram
    max_mel = np.max(mel_spec)
    if max_mel == 0:
        mel_spec_normalized = mel_spec
    else:
        mel_spec_normalized = mel_spec / max_mel
    # print("mel_spec_normalized:", mel_spec_normalized)

    # Smooth the output (optional)
    mel_spec_smoothed = mel_smoothing.update(mel_spec_normalized)
    # print("mel_spec_smoothed:", mel_spec_smoothed)

    # Map to LED levels (0 to N_FFT_BINS)
    led_levels = (mel_spec_smoothed * config.N_FFT_BINS).astype(int)
    led_levels = np.clip(led_levels, 0, config.N_FFT_BINS)
    # print("LED Levels:", led_levels)

    # Update LEDs
    led_utils.set_levels(led_levels)

def test_leds():
    """
    Tests the LEDs by cycling through brightness levels from 0 to 5.
    Sets all LEDs to each level sequentially with a short delay.
    """
    print("Starting LED test...")
    for level in range(0, config.N_FFT_BINS + 1):  # Levels 0 to 5
        levels = [level] * config.N_FFT_BINS  # Set all LEDs to the current level
        print(f"Setting LEDs to: {levels}")
        led_utils.set_levels(levels)
        time.sleep(0.5)  # Wait for 0.5 seconds
    print("LED test completed. Turning off LEDs.")
    led_utils.set_levels([0] * config.N_FFT_BINS)  # Turn off all LEDs
    time.sleep(0.5)  # Short pause after turning off

if __name__ == '__main__':
    dsp.create_mel_bank()  # Ensure Mel filterbank is initialized
    test_leds()  # Execute the LED test function
    led_utils.set_levels([0] * config.N_FFT_BINS)  # Initialize LEDs to off
    try:
        audio_dev_utils.start_stream(audio_update)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        led_utils.cleanup()