import time
import numpy as np
from segment import Segment
from strip import Strip
from loop import Loop
from multi_segment import MultiSegment
from effects.blink_fx import BlinkFx
from effects.meter_fx import MeterFx
from gradient import Gradient
from palette import GRADIENT_PRESETS
# from status_led import set_led_down, set_led_up, led_clean_up
from effect_manager import EffectManager

def run_strip_process(commands_queue, audio_queue):
    leftStrip = Strip(num_leds=120, gpio_pin=18, dma_channel=10, pwm_channel=0)
    rightStrip = Strip(num_leds=120, gpio_pin=21, dma_channel=5, pwm_channel=0)

    segment_l1 = Segment(leftStrip, 0, 30)
    segment_l2 = Segment(leftStrip, 60, 90)
    leftMultisegment_1 = MultiSegment(mode="add")
    leftMultisegment_1.addSegment(segment_l1)
    leftMultisegment_1.addSegment(segment_l2)

    segment_l3 = Segment(leftStrip, 30, 60)
    segment_l4 = Segment(leftStrip, 90, 120)
    leftMultisegment_2 = MultiSegment(mode="add")
    leftMultisegment_2.addSegment(segment_l3)
    leftMultisegment_2.addSegment(segment_l4)

    segment_r1 = Segment(rightStrip, 0, 30)
    segment_r2 = Segment(rightStrip, 60, 90)
    rightMultisegment_1 = MultiSegment(mode="add")
    rightMultisegment_1.addSegment(segment_r1)
    rightMultisegment_1.addSegment(segment_r2)

    segment_r3 = Segment(rightStrip, 30, 60)
    segment_r4 = Segment(rightStrip, 90, 120)
    rightMultisegment_2 = MultiSegment(mode="add")
    rightMultisegment_2.addSegment(segment_r3)
    rightMultisegment_2.addSegment(segment_r4)

    gPreset = GRADIENT_PRESETS["red_flash"]
    g = Gradient(colors=gPreset, resolution=255)

    meter_fx_l1 = MeterFx(leftMultisegment_1, gradient=g)
    meter_fx_l1.set_mode("meter_sides")

    meter_fx_l2 = MeterFx(leftMultisegment_2, gradient=g)
    meter_fx_l2.set_mode("meter_sides")

    meter_fx_r1 = MeterFx(rightMultisegment_1, gradient=g)
    meter_fx_r1.set_mode("meter_sides")

    meter_fx_r2 = MeterFx(rightMultisegment_2, gradient=g)
    meter_fx_r2.set_mode("meter_sides")

    effectManager = EffectManager(mode="auto_cycle", time_cycle_duration=30000)
    effectManager.add([
        meter_fx_l1,
        meter_fx_l2,
        meter_fx_r1,
        meter_fx_r2
    ])

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