# The MIT License (MIT)
#
# Copyright (c) 2022 Chris J Daly (github user cjdaly)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import board, busio
import neopixel as NP
from adafruit_seesaw import seesaw, rotaryio, digitalio, neopixel

from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.sequence import AnimationSequence

# for QtPy-ESP32-S2:
i2c = busio.I2C(board.SCL1, board.SDA1)
# for ESP32-S2-TFT-Feather:
# i2c = board.I2C()

seesaw = seesaw.Seesaw(i2c, addr=0x36)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)

button = digitalio.DigitalIO(seesaw, 24)
button_held = False

rotary_pixel = neopixel.NeoPixel(seesaw, 6, 1)

brightness_step=0.04
rainbow_pixels = NP.NeoPixel(board.A0, 96, brightness=0.5, auto_write=False)

def update_brightness(step):
  br = rainbow_pixels.brightness + step
  if br > 1.0:
    br = 1.0
  elif br < 0.0:
    br = 0.0
  rainbow_pixels.brightness = br

rainbow = Rainbow(rainbow_pixels, speed=0.1, period=5)
rainbow_comet = RainbowComet(
  rainbow_pixels, speed=0.01, tail_length=99, bounce=True)
rainbow_chase = RainbowChase(
  rainbow_pixels, speed=0.02, size=9, spacing=3, step=33)
rainbow_sparkle = RainbowSparkle(
  rainbow_pixels, speed=0.02, num_sparkles=3)

animations = AnimationSequence(
  rainbow,
  rainbow_comet,
  rainbow_chase,
  rainbow_sparkle,
  auto_clear=True,
)

encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = -encoder.position

while True:
  animations.animate()

  # negate the position to make clockwise rotation positive
  position = -encoder.position

  if position > last_position:
    last_position = position
    update_brightness(brightness_step)
  elif position < last_position:
    last_position = position
    update_brightness(-brightness_step)

  if not button.value and not button_held:
    button_held = True

  if button.value and button_held:
    button_held = False
    animations.next()

