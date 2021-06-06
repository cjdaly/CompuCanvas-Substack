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

import board, digitalio, time
import adafruit_dotstar, neopixel

dt = adafruit_dotstar.DotStar(board.DOTSTAR_CLOCK, board.DOTSTAR_DATA, 5)
dt.fill((0,0,10))

px = neopixel.NeoPixel(board.A2, 2)
px.fill((0,0,33))

d0 = digitalio.DigitalInOut(board.A0)
d0.direction=digitalio.Direction.INPUT
d0.pull=digitalio.Pull.UP

d1 = digitalio.DigitalInOut(board.A1)
d1.direction=digitalio.Direction.INPUT
d1.pull=digitalio.Pull.UP

while True:
    if d0.value:
        px[1] = (0,0,33)
    else:
        px[1] = (0,33,0)
    #
    if d1.value:
        px[0] = (0,0,33)
    else:
        px[0] = (0,33,0)
    #
    time.sleep(0.05)
