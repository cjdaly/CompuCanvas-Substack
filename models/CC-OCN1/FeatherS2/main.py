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
import adafruit_dotstar, adafruit_mcp4728

i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 = adafruit_mcp4728.MCP4728(i2c)
mcp4728.channel_a.value = 50000

dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot[0]=(0,33,0)

px = neopixel.NeoPixel(board.IO17, 2)
px.fill((0,0,33))

d0 = digitalio.DigitalInOut(board.IO18)
d0.direction=digitalio.Direction.INPUT
d0.pull=digitalio.Pull.UP

d1 = digitalio.DigitalInOut(board.IO12)
d1.direction=digitalio.Direction.INPUT
d1.pull=digitalio.Pull.UP

while True:
    v_base=0 ; v0=0 ; v1=0
    if d0.value:
        px[0] = (0,0,33)
        dot[0]=(0,0,33)
    else:
        px[0] = (0,33,0)
        dot[0]=(0,33,0)
        v_base = 50000 ; v0 = 1000
    #
    if d1.value:
        px[1] = (0,0,33)
        dot[0]=(0,0,33)
    else:
        px[1] = (0,33,0)
        dot[0]=(10,0,20)
        v_base = 50000 ; v1 = 2000
    #
    mcp4728.channel_a.value = v_base + v0 + v1
    time.sleep(0.05)
