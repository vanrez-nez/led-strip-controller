import time
import numpy as np
from segment import Segment
from strip import Strip
from loop import Loop
from gradient import Gradient
from palette import GRADIENT_PRESETS
# from status_led import set_led_down, set_led_up, led_clean_up
from effect_manager import EffectManager
from effects_factory import add_meter_fx, add_blink_fx, add_cop_fx

def run_strip_process(commands_queue, audio_queue):
    leftStrip = Strip(num_leds=120, gpio_pin=18, dma_channel=10, pwm_channel=0)
    rightStrip = Strip(num_leds=120, gpio_pin=21, dma_channel=5, pwm_channel=0)
    effectManager = EffectManager(mode="auto_cycle", time_cycle_duration=30000)
    add_cop_fx(effectManager, leftStrip, rightStrip)
    # add_meter_fx(effectManager, leftStrip, rightStrip, "meter_sides")
    # add_meter_fx(effectManager, leftStrip, rightStrip, "meter_center")
    # add_meter_fx(effectManager, leftStrip, rightStrip, "meter")
    # add_blink_fx(effectManager, leftStrip, rightStrip, "strobe_level")
    # add_blink_fx(effectManager, leftStrip, rightStrip, "smooth_level")
    loop = Loop(mode="avg", avg_interval=2.0)
    # Keep track of the last known audio level
    current_level = 0.0
    running = True
    while running:
        # Check for commands from main
        try:
            cmd = commands_queue.get_nowait()
            if cmd == "exit":
                running = False
        except:
            pass

        # Check for new audio level
        # Drain the queue to get the latest level
        while not audio_queue.empty():
            current_level = audio_queue.get_nowait()
        loop.update()
        loop.print_fps()
        effectManager.update(loop.delta, current_level)
        leftStrip.push()
        rightStrip.push()
        # Aim for a certain refresh rate, e.g., 100 FPS (~10 ms per frame)
        time.sleep(0.0001)