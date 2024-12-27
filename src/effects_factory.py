from segment import Segment
from multi_segment import MultiSegment
from effects.meter_fx import MeterFx
from effects.blink_fx import BlinkFx
from effects.cop_fx import CopFx
from effects.random_fx import RandomFx
from effects.scroll_fx import ScrollFx

from gradient import Gradient
from palette import GRADIENT_PRESETS

def create_strip_segment(strip, s1_from, s1_to, s2_from, s2_to):
  segment_1 = Segment(strip, s1_from, s1_to)
  segment_2 = Segment(strip, s2_from, s2_to)
  multiSegment = MultiSegment(mode="add")
  multiSegment.addSegment(segment_1)
  multiSegment.addSegment(segment_2)
  return multiSegment


def add_meter_fx(effectManager, strip, mode):
  seg1 = create_strip_segment(strip, 0, 30, 60, 90)
  seg2 = create_strip_segment(strip, 30, 60, 90, 120)

  g = Gradient(resolution=512)
  g.add_color_group(GRADIENT_PRESETS["red_flash"])
  g.add_color_group(GRADIENT_PRESETS["fierce_ice"])

  fx1 = MeterFx(seg1, gradient=g)
  fx1.set_mode(mode)

  fx2 = MeterFx(seg2, gradient=g)
  fx2.set_mode(mode)

  effectManager.add("meter_" + mode, [
      fx1,
      fx2
  ])

def add_blink_fx(effectManager, strip, mode):
  seg = Segment(strip, 0, 120)

  g = Gradient(resolution=512)
  g.add_color_group(GRADIENT_PRESETS["red_flash"])
  g.add_color_group(GRADIENT_PRESETS["es_landscape_64"])

  fx = BlinkFx(seg, gradient=g)
  fx.set_mode(mode)

  effectManager.add("blink_" + mode, [
      fx
  ])

def add_cop_fx(effectManager, strip):
  seg = Segment(strip, 0, 120)
  fx = CopFx(seg, 500, direction = 1)
  fx.set_mode('flash')
  effectManager.add("cop", [
      fx
  ])

def add_random_fx(effectManager, strip, color_preset):
  seg1 = create_strip_segment(strip, 0, 30, 60, 90)
  seg2 = create_strip_segment(strip, 30, 60, 90, 120)

  g = Gradient(resolution=512)
  g.add_color_group(GRADIENT_PRESETS[color_preset])

  fx1 = RandomFx(seg1, gradient=g)
  fx2 = RandomFx(seg2, gradient=g)

  effectManager.add("random_" + color_preset, [
      fx1,
      fx2
  ])

def add_scroll_fx(effectManager, strip):
  seg1 = create_strip_segment(strip, 0, 30, 60, 90)
  seg2 = create_strip_segment(strip, 30, 60, 90, 120)

  g = Gradient(resolution=512)
  g.add_color_group(GRADIENT_PRESETS["red_flash"])
  g.add_color_group(GRADIENT_PRESETS["fierce_ice"])

  fx1 = ScrollFx(seg1, gradient=g)
  fx2 = ScrollFx(seg2, gradient=g)

  effectManager.add("scroll", [
      fx1,
      fx2
  ])