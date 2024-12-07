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


def add_meter_fx(effectManager, leftStrip, rightStrip, mode):
  ml1 = create_strip_segment(leftStrip, 0, 30, 60, 90)
  ml2 = create_strip_segment(leftStrip, 30, 60, 90, 120)
  mr1 = create_strip_segment(rightStrip, 0, 30, 60, 90)
  mr2 = create_strip_segment(rightStrip, 30, 60, 90, 120)


  g = Gradient(resolution=512)
  g.add_color_group(GRADIENT_PRESETS["red_flash"])
  g.add_color_group(GRADIENT_PRESETS["fierce_ice"])

  fx_l1 = MeterFx(ml1, gradient=g)
  fx_l1.set_mode(mode)
  fx_l2 = MeterFx(ml2, gradient=g)
  fx_l2.set_mode(mode)

  fx_r1 = MeterFx(mr1, gradient=g)
  fx_r1.set_mode(mode)
  fx_r2 = MeterFx(mr2, gradient=g)
  fx_r2.set_mode(mode)

  effectManager.add([
      fx_l1,
      fx_l2,
      fx_r1,
      fx_r2
  ])

def add_blink_fx(effectManager, leftStrip, rightStrip, mode):
  segment_1 = Segment(leftStrip, 0, 120)
  segment_2 = Segment(rightStrip, 0, 120)

  g = Gradient(resolution=512)
  g.add_color_group(GRADIENT_PRESETS["red_flash"])
  g.add_color_group(GRADIENT_PRESETS["es_landscape_64"])

  fx_left = BlinkFx(segment_1, gradient=g)
  fx_left.set_mode(mode)
  fx_right = BlinkFx(segment_2, gradient=g)
  fx_right.set_mode(mode)

  effectManager.add([
      fx_left,
      fx_right
  ])

def add_cop_fx(effectManager, leftStrip, rightStrip):
  segment_1 = Segment(leftStrip, 0, 120)
  segment_2 = Segment(rightStrip, 0, 120)
  fx_left = CopFx(segment_1, 500, direction = 1)
  fx_left.set_mode('flash')
  fx_right = CopFx(segment_2, 500, direction = 0, reverse_colors=True)
  fx_right.set_mode('flash')
  effectManager.add([
      fx_left,
      fx_right
  ])

def add_random_fx(effectManager, leftStrip, rightStrip, color_preset):
  ml1 = create_strip_segment(leftStrip, 0, 30, 60, 90)
  ml2 = create_strip_segment(leftStrip, 30, 60, 90, 120)
  mr1 = create_strip_segment(rightStrip, 0, 30, 60, 90)
  mr2 = create_strip_segment(rightStrip, 30, 60, 90, 120)

  g = Gradient(resolution=512)
  g.add_color_group(GRADIENT_PRESETS[color_preset])

  fx_l1 = RandomFx(ml1, gradient=g)
  fx_l2 = RandomFx(ml2, gradient=g)
  fx_r1 = RandomFx(mr1, gradient=g)
  fx_r2 = RandomFx(mr2, gradient=g)

  effectManager.add([
      fx_l1,
      fx_l2,
      fx_r1,
      fx_r2
  ])

def add_scroll_fx(effectManager, leftStrip, rightStrip):
  ml1 = create_strip_segment(leftStrip, 0, 30, 60, 90)
  ml2 = create_strip_segment(leftStrip, 30, 60, 90, 120)
  mr1 = create_strip_segment(rightStrip, 0, 30, 60, 90)
  mr2 = create_strip_segment(rightStrip, 30, 60, 90, 120)

  g = Gradient(resolution=512)
  g.add_color_group(GRADIENT_PRESETS["red_flash"])
  g.add_color_group(GRADIENT_PRESETS["fierce_ice"])

  fx_l1 = ScrollFx(ml1, gradient=g)
  fx_l2 = ScrollFx(ml2, gradient=g)

  fx_r1 = ScrollFx(mr1, gradient=g)
  fx_r2 = ScrollFx(mr2, gradient=g)

  effectManager.add([
      fx_l1,
      fx_l2,
      fx_r1,
      fx_r2
  ])