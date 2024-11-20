import tkinter as tk
from strip import Strip
from segment import Segment
from pixel import Pixel
import numpy as np
import tkinter as tk
import numpy as np
import time
from effects.blink_fx import BlinkFx
from loop import Loop

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

    def close(self):
        """Cleanly close the Tkinter window."""
        self.root.quit()
        self.root.destroy()

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

def main():
    strip = Strip(50)
    visualizer = StripVisualizer(strip)
    segment1 = Segment(strip, 10, 20)
    segment2 = Segment(strip, 40, 50, direction=-1)
    blink_fx = BlinkFx(segment1, color=(255, 0, 0), interval=500)  # Red blink every 500 ms

    def on_frame(delta_ms, elapsed_ms):
        blink_fx.update(delta_ms)
        visualizer.update()
        print(f"Elapsed time: {elapsed_ms:.2f} ms")
        visualizer.root.after(1, loop.update)

    loop = Loop(callback=on_frame, fps=60)
    visualizer.root.after(1, loop.update)
    try:
        loop.start()
        visualizer.root.mainloop()

    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        visualizer.close()

if __name__ == "__main__":
    main()