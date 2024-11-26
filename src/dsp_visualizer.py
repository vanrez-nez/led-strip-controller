import pyaudio
from dsp.input import list_input_devices

if __name__ == "__main__":
    p = pyaudio.PyAudio()
    list_input_devices(p)
