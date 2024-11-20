import tkinter as tk
from strip import Strip
from segment import Segment
from pixel import Pixel
import numpy as np
import tkinter as tk
import numpy as np
import time

class StripVisualizer:
    def __init__(self, strip):
        self.strip = strip
        num_leds = len(strip)
        # Create the Tkinter window
        self.root = tk.Tk()
        self.root.title("LED Strip Visualization")

        # Define LED size and spacing
        self.led_size = 20
        self.spacing = 5
        width = (self.led_size + self.spacing) * num_leds + self.spacing
        height = self.led_size + 2 * self.spacing

        # Create a canvas to draw the LEDs
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack()

        # Create rectangles representing each LED
        self.led_rects = []
        for i in range(num_leds):
            x0 = self.spacing + i * (self.led_size + self.spacing)
            y0 = self.spacing
            x1 = x0 + self.led_size
            y1 = y0 + self.led_size
            rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill='black')
            self.led_rects.append(rect)

    def update(self):
        for i in range(len(self.strip)):
            r, g, b, brightness = self.strip.data[i]
            # Normalize brightness
            brightness = brightness / 255.0
            # Adjust color values based on brightness
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)
            # Convert to hex color code
            color = f'#{r:02x}{g:02x}{b:02x}'
            # Update the rectangle color only if it has changed
            current_color = self.canvas.itemcget(self.led_rects[i], 'fill')
            if current_color != color:
                self.canvas.itemconfig(self.led_rects[i], fill=color)
        # Process any pending Tkinter events
        self.canvas.update_idletasks()
        self.canvas.update()

if __name__ == "__main__":
    strip = Strip(50)
    # Initialize the visualizer with the strip
    visualizer = StripVisualizer(strip)
    try:
        while True:
            # Modify the strip data as needed
            # Example: Cycle colors across the strip
            strip.data[:, 0] = (strip.data[:, 0] + 5) % 255   # Adjust red component
            strip.data[:, 1] = (strip.data[:, 1] + 3) % 255   # Adjust green component
            strip.data[:, 2] = (strip.data[:, 2] + 1) % 255   # Adjust blue component
            strip.data[:, 3] = 255                            # Set brightness to maximum
            # Update the visualization
            visualizer.update()
            # Sleep or perform other tasks
            time.sleep(30/1000)
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanly close the Tkinter window
        visualizer.root.destroy()