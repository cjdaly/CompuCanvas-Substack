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

def initDigIn(pin):
  dIn = DigitalInOut(pin) ; dIn.direction = Direction.INPUT
  return dIn

ledR = initLED(board.LED_R)
ledG = initLED(board.LED_G)
ledB = initLED(board.LED_B)
leds = [ledR, ledG, ledB]

dIn1 = initDigIn(board.D1)
dIn2 = initDigIn(board.D2)
dIn3 = initDigIn(board.D3)
dIns = [dIn1, dIn2, dIn3]

def updateLEDs(leds, dIns):
  leds[0].value = not dIns[0].value
  leds[1].value = dIns[1].value
  leds[2].value = not dIns[2].value

while True:
  updateLEDs(leds, dIns)
  time.sleep(0.2)

