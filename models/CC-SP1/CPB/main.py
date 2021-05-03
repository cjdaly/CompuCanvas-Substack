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

import board, busio, pulseio, neopixel, time

# neopixels
px=neopixel.NeoPixel(board.NEOPIXEL,10)

# uart
ux=busio.UART(board.TX,board.RX)

# PWM to Serpente for RGB
sp1 = pulseio.PWMOut(board.D6)
sp2 = pulseio.PWMOut(board.D9)
sp3 = pulseio.PWMOut(board.D10)

def strobe(spx):
  for i in range(101):
    pi = i / 100
    spx.duty_cycle = int (65535 * pi)
    time.sleep(0.05)
  spx.duty_cycle = 0


while True:
  px[0] = (3,0,0)
  strobe(sp1)
  px[0] = (0,3,0)
  strobe(sp2)
  px[0] = (0,0,3)
  strobe(sp3)

  