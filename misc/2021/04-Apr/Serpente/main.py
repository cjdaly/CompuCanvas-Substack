# The MIT License (MIT)
#
# Copyright (c) 2021 Chris J Daly (github user cjdaly)
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

import time, board
from digitalio import DigitalInOut, Direction

def initLED(pin):
  led = DigitalInOut(pin) ; led.direction = Direction.OUTPUT
  led.value = True # off
  return led

ledR = initLED(board.LED_R)
ledG = initLED(board.LED_G)
ledB = initLED(board.LED_B)
leds = [ledR, ledG, ledB]

def updateLEDs(leds, pattern):
  if (len(pattern)==5) and pattern.startswith("[") :
    leds[0].value = pattern[1] != 'R'
    leds[1].value = pattern[2] != 'G'
    leds[2].value = pattern[3] != 'B'

while True:
  updateLEDs(leds, input())

