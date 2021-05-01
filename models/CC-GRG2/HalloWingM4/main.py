# The MIT License (MIT)
#
# Copyright (c) 2020 Chris J Daly (github user cjdaly)
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

# setup coin checker
cx=digitalio.DigitalInOut(board.A1)
cx.direction=digitalio.Direction.INPUT
cx.pull=digitalio.Pull.UP

# set neopixels
px=neopixel.NeoPixel(board.NEOPIXEL,4)

# colors
clr_yay=((0,0,10),(0,10,0))
clr_boo=((10,0,0),(10,10,0))

def blink(colors,offset):
  for i in range(4):
    if (i+offset)%2==0:
      px[i]=colors[0]
    else:
      px[i]=colors[1]

# uart
ur=busio.UART(board.TX,board.RX)

def write_cmd(has_coin):
  if has_coin:
    ur.write(b'COIN')
  else:
    ur.write(b'GONE')

while True:
  has_coin=not cx.value
  if has_coin: 
    blink(clr_yay, 0)
  else:
    blink(clr_boo, 0)
  write_cmd(has_coin)
  time.sleep(1)
  #
  has_coin=not cx.value
  if has_coin:
    blink(clr_yay, 1)
  else:
    blink(clr_boo, 1)
  write_cmd(has_coin)
  time.sleep(1)
  
