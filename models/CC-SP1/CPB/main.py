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

import board, busio, digitalio, neopixel, time

# neopixels
px=neopixel.NeoPixel(board.NEOPIXEL,10)

# uart
ux=busio.UART(board.TX,board.RX)

def initDOut(dPin):
  dOut = digitalio.DigitalInOut(dPin)
  dOut.direction=digitalio.Direction.OUTPUT
  return dOut

# Serpente state control
dS0 = initDOut(board.D3)
dS1 = initDOut(board.D2)

# Serpente value control
dV0 = initDOut(board.D6)
dV1 = initDOut(board.D9)
dV2 = initDOut(board.D10)

while True:
  for col in range(3):
    for br in range(8):
      if col == 0:
        dS0.value = True ; dS1.value = False;
      elif col == 1:
        dS0.value = False ; dS1.value = True;
      elif col == 2:
        dS0.value = True ; dS1.value = True;
      #
      dV0.value = br&1 > 0
      dV1.value = br&2 > 0
      dV2.value = br&4 > 0
      #
      time.sleep(1)
    dV0.value = 0
    dV1.value = 0
    dV2.value = 0
    time.sleep(1)

  