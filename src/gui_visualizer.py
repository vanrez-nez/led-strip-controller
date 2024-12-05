import tkinter as tk
from strip import Strip
from segment import Segment
import tkinter as tk
from effects.blink_fx import BlinkFx
from effects.meter_fx import MeterFx
from loop import Loop
from gradient import Gradient
from palette import GRADIENT_PRESETS
from dsp_processor import DSPProcessor
from effect_manager import EffectManager

class GuiStripVisualizer:
    def __init__(self, strip):
        self.strip = strip
        num_leds = len(strip)
        # Create the Tkinter window
        self.root = tk.Tk()
        self.root.title("LED Strip Visualization")

        # Define LED size and spacing
        self.led_size = 10
        self.spacing = 2
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
            rect = self.canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='black')
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
    strip = Strip(num_leds=30, gpio_pin=18, dma_channel=10, pwm_channel=0)
    visualizer = GuiStripVisualizer(strip)
    segment1 = Segment(strip, 0, 30)
    # segment2 = Segment(strip, 40, 50, direction=-1)
    gPreset = GRADIENT_PRESETS["red_flash"]
    # gPreset = GRADIENT_PRESETS["es_vintage_57"]
    g = Gradient(colors=gPreset, resolution=255)
    blink_fx = BlinkFx(segment1, color=(255, 0, 0), interval=500, smooth=True, gradient=g)
    blink_fx.set_mode("strobe")
    # meter_fx = MeterFx(segment1, gradient=g)
    # meter_fx.set_mode("meter_sides")
    processor = DSPProcessor()
    effectManager = EffectManager(mode="auto_cycle", time_cycle_duration=30000)
    effectManager.add(blink_fx)
    # effectManager.add(meter_fx)
    processor.start()
    loop = Loop()

    def on_frame():
        loop.update()
        processor.update()
        # loop.print_fps()
        effectManager.update(loop.delta, processor.level)
        visualizer.update()
        visualizer.root.after(1, on_frame)
    visualizer.root.after(1, on_frame)
    try:
        visualizer.root.mainloop()

    except KeyboardInterrupt:
        pass
    finally:
        visualizer.close()

if __name__ == "__main__":
    main()