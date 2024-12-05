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
    strip = Strip(num_leds=30, gpio_pin=18, dma_channel=10, pwm_channel=0)
    segment1 = Segment(strip, 0, 30)
    # segment2 = Segment(strip, 40, 50, direction=-1)
    gPreset = GRADIENT_PRESETS["red_flash"]
    # gPreset = GRADIENT_PRESETS["es_vintage_57"]
    g = Gradient(colors=gPreset, resolution=255)
    blink_fx = BlinkFx(segment1, color=(255, 0, 0), interval=500, smooth=True, gradient=g)
    blink_fx.set_mode("strobe")
    # blink_fx.set_mode("smooth_level")
    # meter_fx = MeterFx(segment1, gradient=g)
    # meter_fx.set_mode("meter_sides")
    processor = DSPProcessor()
    effectManager = EffectManager(mode="auto_cycle", time_cycle_duration=30000)
    effectManager.add(blink_fx)
    # effectManager.add(meter_fx)
    processor.start()
    loop = Loop()
    try:
        set_led_up()
        while True:
            loop.update()
            processor.update()
            loop.print_fps()
            effectManager.update(loop.delta, processor.level)
            strip.push()
    except KeyboardInterrupt:
        set_led_down()
        led_clean_up()
        strip.cleanup()
        effectManager.clear()

if __name__ == "__main__":
    main()