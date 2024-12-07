from strip import Strip
from segment import Segment
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

    segment_l1 = Segment(leftStrip, 0, 120)
    segment_r1 = Segment(rightStrip, 0, 120)
    gPreset = GRADIENT_PRESETS["red_flash"]
    g = Gradient(colors=gPreset, resolution=255)

    meter_fx_l1 = MeterFx(segment_l1, gradient=g)
    meter_fx_l1.set_mode("meter_sides")

    meter_fx_r1 = MeterFx(segment_r1, gradient=g)
    meter_fx_r1.set_mode("meter_sides")

    processor = DSPProcessor()
    effectManager = EffectManager(mode="auto_cycle", time_cycle_duration=30000)
    effectManager.add([
        meter_fx_l1,
        meter_fx_r1
    ])
    processor.start()
    loop = Loop()
    try:
        set_led_up()
        while True:
            loop.update()
            processor.update()
            # loop.print_fps()
            effectManager.update(loop.delta, processor.level)
            leftStrip.push()
            rightStrip.push()
    except KeyboardInterrupt:
        set_led_down()
        led_clean_up()
        effectManager.clear()

if __name__ == "__main__":
    main()