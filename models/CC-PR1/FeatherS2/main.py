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

import board, busio, digitalio, time, neopixel
import adafruit_dotstar
from adafruit_is31fl3741.adafruit_ledglasses import LED_Glasses

gl = LED_Glasses(board.I2C())
for i in range(24):
    gl.left_ring[i] = 0x000800
    gl.right_ring[i] = 0x000800

dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot[0]=(0,33,0)

px = neopixel.NeoPixel(board.IO17, 1)
px.fill((0,0,33))

d0 = digitalio.DigitalInOut(board.IO18)
d0.direction=digitalio.Direction.INPUT
d0.pull=digitalio.Pull.UP

def fill_glasses(color):
    for i in range(24):
        gl.left_ring[i] = color
        gl.right_ring[i] = color

colors = (0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF, 0xFFFFFF)
cx=0 ; kp=0

while True:
    if d0.value:
        px[0] = (0,0,33) ; dot[0]=(0,0,33)
        kp = 0
    else:
        px[0] = (0,33,0) ; dot[0]=(0,33,0)
        kp += 1
        if kp == 3:
            cx += 1
            fill_glasses(colors[cx%len(colors)])
    time.sleep(0.05)
