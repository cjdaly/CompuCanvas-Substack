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

import board, digitalio, time, neopixel

px_moon = neopixel.NeoPixel(board.A1, 61)
px_keys = neopixel.NeoPixel(board.A2, 3)

d0 = digitalio.DigitalInOut(board.A3)
d0.direction=digitalio.Direction.INPUT
d0.pull=digitalio.Pull.UP

d1 = digitalio.DigitalInOut(board.A4)
d1.direction=digitalio.Direction.INPUT
d1.pull=digitalio.Pull.UP

d2 = digitalio.DigitalInOut(board.A5)
d2.direction=digitalio.Direction.INPUT
d2.pull=digitalio.Pull.UP

while True:
    moon_color = (0,0,0)
    #
    if d0.value:
        px_keys[0] = (33,0,0)
    else:
        px_keys[0] = (200,0,0)
        moon_color = (20,0,0)
    #
    if d1.value:
        px_keys[1] = (0,33,0)
    else:
        px_keys[1] = (0,200,0)
        moon_color = (0,33,0)
    #
    if d2.value:
        px_keys[2] = (0,0,33)
    else:
        px_keys[2] = (0,0,200)
        moon_color = (0,0,69)
    #
    px_moon.fill(moon_color)
    time.sleep(0.05)
