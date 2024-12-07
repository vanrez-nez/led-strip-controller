from dotenv import load_dotenv
import os
load_dotenv()

########################
# DSP Audio Configuration
#########################

# Sampling rate in Hz
DSP_RATE = 44100
# Frames per second
DSP_FPS = 45
# Number of frames to keep in rolling buffer
DSP_N_ROLLING_HISTORY = 4
# Number of Mel filterbank channels (5 LEDs)
DSP_N_FFT_BINS = 1
# Minimum frequency for Mel filterbank in Hz
DSP_MIN_FREQUENCY = 20
# Maximum frequency for Mel filterbank in Hz
DSP_MAX_FREQUENCY = 160
# Audio device index to use
DSP_DEVICE_INDEX = int(os.getenv("DSP_DEVICE_INDEX", 0))
# Minimum volume threshold for audio input
DSP_MIN_VOLUME_THRESHOLD = 1e-7


########################
# Global Configuration
########################

# The GPIO pin number for the LED status indicator (BCM numbering)
LED_STATUS_GPIO_PIN = 5


########################
# LED Strip Configuration
########################
STRIP_LED_FREQ_HZ = 800000
STRIP_LED_BRIGHTNESS = 255