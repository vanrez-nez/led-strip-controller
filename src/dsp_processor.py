import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from dsp.dsp import ExpFilter, mel_y
import config as config
from dsp.audio_stream import AudioStream

class DSPProcessor:
    def __init__(self):
        """Initialize the DSP Processor with necessary configurations and filters."""
        self.audio_stream = AudioStream()  # Initialize the audio stream
        self.mel_gain = ExpFilter(np.tile(1e-1, config.DSP_N_FFT_BINS), alpha_decay=0.01, alpha_rise=0.99)
        self.mel_smoothing = ExpFilter(np.tile(1e-1, config.DSP_N_FFT_BINS), alpha_decay=0.5, alpha_rise=0.99)
        self.gain = ExpFilter(np.tile(0.01, config.DSP_N_FFT_BINS), alpha_decay=0.001, alpha_rise=0.99)
        self.fft_window = np.hamming(int(config.DSP_RATE / config.DSP_FPS) * config.DSP_N_ROLLING_HISTORY)
        self.y_roll = np.random.rand(config.DSP_N_ROLLING_HISTORY, int(config.DSP_RATE / config.DSP_FPS)) / 1e16
        self.level = None  # Store the computed level

    def update(self):
        """Fetch new audio samples, update the rolling buffer, and compute the level."""
        # Update the AudioStream and get audio data from its property
        self.audio_stream.update()
        audio_samples = self.audio_stream.audio_data

        if audio_samples is None:
            print("Warning: No audio samples received.")
            return

        # Update the rolling buffer
        np.set_printoptions(suppress=True, precision=4)
        y = audio_samples / 2.0**15  # Normalize the input samples
        self.y_roll[:-1] = self.y_roll[1:]
        self.y_roll[-1, :] = np.copy(y)
        y_data = np.concatenate(self.y_roll, axis=0).astype(np.float32)

        # Compute the level from the updated buffer
        self.level = self.get_level(y_data)

    def get_level(self, y_data):
        """Process the rolling buffer to compute the visualization level."""
        # Check volume threshold
        vol = np.max(np.abs(y_data))
        if vol < config.DSP_MIN_VOLUME_THRESHOLD:
            print('No audio input. Volume below threshold. Volume:', vol)
            return np.zeros(config.DSP_N_FFT_BINS)  # Return zeros if volume is too low

        # Apply FFT and Mel filterbank
        N = len(y_data)
        N_zeros = 2**int(np.ceil(np.log2(N))) - N
        y_data *= self.fft_window
        y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
        YS = np.abs(np.fft.rfft(y_padded)[:N // 2])

        # Mel filterbank processing
        mel = np.atleast_2d(YS).T * mel_y.T
        mel = np.sum(mel, axis=0)
        mel = mel**2.0  # Emphasize energy

        # Gain normalization and smoothing
        self.mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
        mel /= self.mel_gain.value
        mel = self.mel_smoothing.update(mel)

        # Energy normalization
        self.gain.update(mel)
        level = mel / self.gain.value
        return level[0]

    def start(self):
        """Start the audio stream."""
        self.audio_stream.start()

    def stop(self):
        """Stop the audio stream."""
        self.audio_stream.stop()