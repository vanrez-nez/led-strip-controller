try:
    import RPi.GPIO as GPIO
    import config as config
    gpio_available = True
except ImportError:
    gpio_available = False

def not_gpio_available(call_str):
    print(f"RPi.GPIO library is not installed or available. {call_str}")
    return None

def set_up():
    if not gpio_available:
        return not_gpio_available('set_up()')
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(config.LED_STATUS_GPIO_PIN, GPIO.OUT)
    GPIO.output(config.LED_STATUS_GPIO_PIN, GPIO.LOW)

def clean_up():
    if not gpio_available:
        return not_gpio_available('clean_up()')
    GPIO.cleanup()

def set_led_up():
    if not gpio_available:
        return not_gpio_available('set_led_up()')
    GPIO.output(config.LED_STATUS_GPIO_PIN, GPIO.HIGH)

def set_led_down():
    if not gpio_available:
        return not_gpio_available('set_led_down()')
    GPIO.output(config.LED_STATUS_GPIO_PIN, GPIO.LOW)

set_up()

if __name__ == "__main__":
    # Test the LED functions by blinking the LED
    import time
    set_led_up()
    time.sleep(1)
    set_led_down()
    clean_up()