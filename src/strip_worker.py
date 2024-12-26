import time
import numpy as np
from segment import Segment
from strip import Strip
from loop import Loop
from gradient import Gradient
from palette import GRADIENT_PRESETS
from status_led import set_led_down, set_led_up, led_clean_up
from effect_manager import EffectManager
from com_manager import ComManager
from effects_factory import add_meter_fx, add_blink_fx, add_cop_fx, add_random_fx, add_scroll_fx

def run_strip_process(commands_queue, audio_queue):
    set_led_up()
    leftStrip = Strip(num_leds=120, gpio_pin=18, dma_channel=10, pwm_channel=0)
    rightStrip = Strip(num_leds=120, gpio_pin=21, dma_channel=5, pwm_channel=0)
    effectManager = EffectManager(mode="auto_cycle", time_cycle_duration=30000)

    add_scroll_fx(effectManager, leftStrip, rightStrip)
    add_meter_fx(effectManager, leftStrip, rightStrip, "center")
    add_random_fx(effectManager, leftStrip, rightStrip, "toxy_reaf")
    add_blink_fx(effectManager, leftStrip, rightStrip, "strobe")
    add_random_fx(effectManager, leftStrip, rightStrip, "red_shift")
    add_blink_fx(effectManager, leftStrip, rightStrip, "smooth")
    add_meter_fx(effectManager, leftStrip, rightStrip, "from_bottom")
    add_random_fx(effectManager, leftStrip, rightStrip, "BlacK_Magenta_Red")
    add_meter_fx(effectManager, leftStrip, rightStrip, "sides")
    add_cop_fx(effectManager, leftStrip, rightStrip)

    comManager = ComManager(effectManager)

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
        effectManager.update(loop.delta, current_level)
        leftStrip.push()
        rightStrip.push()
        comManager.update(loop.avg_fps)
        time.sleep(0.0001)

    set_led_down()