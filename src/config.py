# DSP Audio Configuration
DSP_RATE = 44100                # Sampling rate in Hz
DSP_FPS = 42                    # Frames per second
DSP_N_ROLLING_HISTORY = 4       # Number of frames to keep in rolling buffer
DSP_N_FFT_BINS = 1              # Number of Mel filterbank channels (5 LEDs)
DSP_MIN_FREQUENCY = 20         # Minimum frequency for Mel filterbank in Hz
DSP_MAX_FREQUENCY = 160       # Maximum frequency for Mel filterbank in Hz
# MIN_FREQUENCY = 3000
# MAX_FREQUENCY = 20000
# MIN_FREQUENCY = 10000
# MAX_FREQUENCY = 20000
DSP_DEVICE_INDEX = 3            # Audio input device index
DSP_MIN_VOLUME_THRESHOLD = 1e-7


LED_STATUS_GPIO_PIN = 5
