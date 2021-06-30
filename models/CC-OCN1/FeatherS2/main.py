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

import board, busio, time
import adafruit_dotstar, adafruit_mcp4728

i2c = busio.I2C(board.SCL, board.SDA)
mcp4728 = adafruit_mcp4728.MCP4728(i2c)
mcp4728.channel_a.value = 50000

dot = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1)
dot[0]=(0,33,0)

i = 0

while True:
    mcp4728.channel_a.value = 48000 + (i*2000)
    dot[0]=(0,33,0)
    time.sleep(1)
    dot[0]=(0,0,33)
    time.sleep(1)
    i += 1
    if i >=4:
        i = 0



