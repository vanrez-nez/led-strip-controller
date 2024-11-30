# Audio Configuration
RATE = 44100                # Sampling rate in Hz
FPS = 30                    # Frames per second
# N_PIXELS = 5
N_ROLLING_HISTORY = 5       # Number of frames to keep in rolling buffer
N_FFT_BINS = 1              # Number of Mel filterbank channels (5 LEDs)
MIN_FREQUENCY = 20         # Minimum frequency for Mel filterbank in Hz
MAX_FREQUENCY = 160       # Maximum frequency for Mel filterbank in Hz

# MIN_FREQUENCY = 3000
# MAX_FREQUENCY = 20000

# MIN_FREQUENCY = 10000
# MAX_FREQUENCY = 20000

DEVICE_INDEX = 3            # Audio input device index
MIN_VOLUME_THRESHOLD = 1e-7
