from strip import Strip
from segment import Segment
from multi_segment import MultiSegment
from effects.blink_fx import BlinkFx
from effects.meter_fx import MeterFx
from loop import Loop
from gradient import Gradient
from palette import GRADIENT_PRESETS
from status_led import set_led_down, set_led_up, led_clean_up
from dsp_processor import DSPProcessor
from effect_manager import EffectManager

def main():
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

    segment_r1 = Segment(leftStrip, 0, 30)
    segment_r2 = Segment(leftStrip, 60, 90)
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

    processor = DSPProcessor()
    effectManager = EffectManager(mode="auto_cycle", time_cycle_duration=30000)
    effectManager.add([
        meter_fx_l1,
        meter_fx_l2,
        meter_fx_r1,
        meter_fx_r2
    ])
    processor.start()
    loop = Loop(mode="avg", avg_interval=2.0)
    try:
        set_led_up()
        while True:
            loop.update()
            processor.update()
            loop.print_fps()
            effectManager.update(loop.delta, processor.level)
            leftStrip.push()
            rightStrip.push()
    except KeyboardInterrupt:
        set_led_down()
        led_clean_up()
        effectManager.clear()

if __name__ == "__main__":
    main()