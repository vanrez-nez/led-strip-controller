import time
from rpi_ws281x import *
import numpy as np
import colorsys

# LED strip configuration:
LED_COUNT = 42         # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 255   # Default max brightness (0-255)
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0        # Set to '1' for GPIOs 13, 19, 41, 45 or 53

# Initialize the strip
strip = Adafruit_NeoPixel(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
)
strip.begin()

# Track the current LED level and peak for decay
current_level = 0
peak_position = 0
peak_decay = 0.995  # Slower decay for the peak
peak_colors = [(0, 0, 0), (255, 0, 0)]

def rgb_to_hsl(r, g, b):
    """Convert RGB to HSL."""
    return colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

def hsl_to_rgb(h, l, s):
    """Convert HSL back to RGB."""
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

def interpolate_hsl(color1, color2, factor):
    """Interpolate between two colors in HSL space."""
    h1, l1, s1 = rgb_to_hsl(*color1)
    h2, l2, s2 = rgb_to_hsl(*color2)

    # Handle hue interpolation by taking the shortest path around the circle
    if abs(h2 - h1) > 0.5:
        if h1 > h2:
            h2 += 1.0
        else:
            h1 += 1.0

    # Interpolate each HSL component
    h = (h1 + (h2 - h1) * factor) % 1.0
    l = l1 + (l2 - l1) * factor
    s = s1 + (s2 - s1) * factor

    return hsl_to_rgb(h, l, s)

def calculate_brightness(rgb):
    """
    Calculate the perceived brightness of an RGB color using the luminance formula.

    :param rgb: Tuple of (R, G, B) with each component in the range 0-255.
    :return: Brightness value as a float in the range 0-255.
    """
    r, g, b = rgb
    brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return brightness

def lookup_gradient_color(position, total_leds, colors):
    """
    Calculate the interpolated color at a specific position along the gradient using HSL interpolation.

    :param position: The position of the LED on the strip (0 to total_leds - 1).
    :param total_leds: Total number of LEDs on the strip.
    :param colors: List of color tuples [(R, G, B), (R, G, B), ...] defining the gradient steps.
    :return: Interpolated color as an (R, G, B) tuple.
    """
    if len(colors) < 2:
        raise ValueError("At least two colors are required for the gradient.")

    step_leds = total_leds / (len(colors) - 1)
    left_index = int(position // step_leds)
    right_index = min(left_index + 1, len(colors) - 1)

    factor = (position % step_leds) / step_leds
    color = interpolate_hsl(colors[left_index], colors[right_index], factor)

    # Debug: Print position and color
    # print(f"lookup_gradient_color - Position: {position}, Color: {color}")
    return color

def apply_main_gradient(current_level, colors, peak_pos=None):
    """
    Apply the main gradient to the LEDs up to current_level, excluding the peak position.

    :param current_level: Number of LEDs to light up.
    :param colors: List of color tuples [(R, G, B), (R, G, B), ...] defining the gradient steps.
    :param peak_pos: Position of the peak LED to exclude from the main gradient.
    """
    strip.setBrightness(int(np.clip(current_level * 0.1 * 255, 0, 255)))
    for i in range(LED_COUNT):
        if i < current_level:
            if peak_pos is not None and i == peak_pos:
                continue  # Skip setting the peak position here
            color = lookup_gradient_color(i, LED_COUNT, colors)
            strip.setPixelColor(i, Color(color[0], color[1], color[2]))
        else:
            # Turn off LEDs beyond `current_level`
            strip.setPixelColor(i, Color(0, 0, 0))

def set_gradient_led(num_leds, colors, decay=0.91):
    """
    Apply a color gradient to the full LED strip, lighting up to `num_leds` LEDs.
    Gradually decays if the level decreases. Adds a peak LED that decays more slowly, within LED limits.

    :param num_leds: Target number of LEDs to light up.
    :param colors: List of color tuples [(R, G, B), (R, G, B), ...] defining the gradient steps.
    :param decay: Decay factor between 0 and 1 to smooth the transition to lower levels.
    """
    global current_level, peak_position

    # Apply decay if the requested level is lower than the current level
    if num_leds < current_level:
        current_level = current_level * decay
    else:
        # Set current level to the new target directly if it's higher or equal
        current_level = num_leds

    # Update the peak position, decaying more slowly, and ensure it's within bounds
    if num_leds > peak_position:
        peak_position = num_leds
    else:
        peak_position = peak_position * peak_decay
        # Ensure peak stays within LED strip limits and above current level
        peak_position = np.clip(peak_position, current_level, LED_COUNT - 1)

    # Apply the main gradient across the LEDs up to current_level, excluding peak_position
    # strip.setBrightness(255)
    apply_main_gradient(int(current_level), colors, peak_pos=int(peak_position) if peak_position >=0 else None)

    # Set the peak LED with its own custom gradient, if within range
    if 0 <= int(peak_position) < LED_COUNT:
        peak_color = lookup_gradient_color(int(peak_position), LED_COUNT, peak_colors)
        # print(f"Setting peak LED at position {peak_position} to color {peak_color}")
        strip.setPixelColor(int(peak_position), Color(peak_color[0], peak_color[1], peak_color[2]))
    strip.show()

def cleanup_leds():
    """
    Turn off all LEDs on the strip and ensure they are cleanly turned off.
    """
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))  # Set each LED to off
    strip.show()  # Update the strip to show the changes

# Example usage
if __name__ == '__main__':
    try:
        # Define a gradient from black to red
        gradient_colors = [(0, 0, 0), (255, 0, 0)]  # Black to red

        while True:
            # Example: Increase level to 100% instantly
            print("Setting gradient to 100%")
            set_gradient_led(LED_COUNT, gradient_colors)
            time.sleep(0.1)

            # Example: Decrease level to 50% with decay
            print("Setting gradient to 50% with decay")
            set_gradient_led(LED_COUNT // 2, gradient_colors, decay=0.9)
            time.sleep(0.1)

            # Example: Decrease level to 0 with decay
            print("Setting gradient to 0 with decay")
            set_gradient_led(0, gradient_colors, decay=0.9)
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Turn off the strip on exit
        print("Strip turned off.")