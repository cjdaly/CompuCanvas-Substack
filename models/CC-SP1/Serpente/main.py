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

import time, board, pulseio, analogio

ledR = pulseio.PWMOut(board.LED_R)
ledG = pulseio.PWMOut(board.LED_G)
ledB = pulseio.PWMOut(board.LED_B)
leds = [ledR, ledG, ledB]

aIn0 = analogio.AnalogIn(board.A0)
aIn1 = analogio.AnalogIn(board.A1)
aIn2 = analogio.AnalogIn(board.A2)
aIns = [aIn0, aIn1, aIn2]

def updateLEDs(leds, dIns):
  leds[0].duty_cycle = 65535 - aIns[0].value
  leds[1].duty_cycle = 65535 - aIns[1].value
  leds[2].duty_cycle = 65535 - aIns[2].value

while True:
  updateLEDs(leds, aIns)
  time.sleep(0.2)

