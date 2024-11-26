import RPi.GPIO as GPIO
import dsp.config as config

# GPIO pin numbers for your 5 LEDs (adjust as per your hardware setup)
LED_PINS = [17, 27, 22, 5, 6]


# GPIO setup
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
# List of GPIO pins where LEDs are connected
led_pins = [17, 27, 22, 5, 6]
# Set up each LED pin as an output and initialize it to LOW (off)
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def control_led(pin, state):
    """Controls an individual LED."""
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)

def set_leds(level):
    """Sets LEDs based on the audio level."""
    # Turn on LEDs up to the current level
    for i in range(len(led_pins)):
        if i < level:
            control_led(led_pins[i], True)
        else:
            control_led(led_pins[i], False)