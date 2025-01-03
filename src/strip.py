import numpy as np
import config as cfg

try:
    from rpi_ws281x import *
    rpi_ws281x_available = True
except ImportError:
    rpi_ws281x_available = False

class Strip:
    def __init__(self, num_leds, gpio_pin, dma_channel, pwm_channel, invert=False):
        # Initialize strip data with zeros
        # Each LED has 4 components: R, G, B, Brightness
        self.data = np.zeros((num_leds, 4), dtype=np.uint8)
        self.gpio = gpio_pin
        self.invert = invert
        self.dma_channel = dma_channel
        self.pwm_channel = pwm_channel
        self.strip = None
        self.initted = False

    def print_error(self, caller):
        print(f"Error in {caller}: rpi_ws281x library is not available. Please install it with 'pip install rpi_ws281x'.")

    def init_strip(self):
        if not rpi_ws281x_available:
            self.print_error("init_strip")
            return None
        if self.initted:
            return self.strip
        led_count = len(self.data)
        strip = Adafruit_NeoPixel(
            num=led_count,
            pin=self.gpio,
            channel=self.pwm_channel,
            dma=self.dma_channel,
            invert=self.invert,
            brightness=cfg.STRIP_LED_BRIGHTNESS,
            freq_hz=cfg.STRIP_LED_FREQ_HZ)
        strip.begin()
        self.strip = strip

    def __len__(self):
        return len(self.data)

    def push(self):
        """Push the LED data to the strip."""
        if not rpi_ws281x_available:
            self.print_error("push")
            return
        if not self.strip:
            self.init_strip()
        for i in range(len(self.data)):
            r, g, b, brightness = self.data[i]
            nb = brightness / 255
            rb = int(r * nb)
            gb = int(g * nb)
            bb = int(b * nb)
            self.strip.setPixelColorRGB(i, rb, gb, bb)
        self.strip.show()

    def clear(self):
        print("Clearing strip data.")
        self.strip.setBrightness(0)
        self.strip.show()
        self.strip._cleanup()
        self.strip = None
        self.initted = False