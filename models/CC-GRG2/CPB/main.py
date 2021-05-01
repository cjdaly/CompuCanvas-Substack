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

import board, busio, neopixel, time

# neopixels
px=neopixel.NeoPixel(board.NEOPIXEL,10)

# colors
clr_yay=((0,0,99),(0,99,0))
clr_boo=((99,0,0),(99,99,0))

def blink(colors,offset):
  for i in range(10):
    if (i+offset)%2==0:
      px[i]=colors[0]
    else:
      px[i]=colors[1]

# uart
ur=busio.UART(board.TX,board.RX)

def read_cmd():
  bc=ur.in_waiting
  if bc == 0:
    return ""
  data=ur.read(bc)
  if data is None:
    return ""
  msg=''.join([chr(b) for b in data])
  return msg

has_coin=False

def process_cmd(phase):
  global has_coin
  msg=read_cmd()
  if not (msg=="" or msg==None):
    if msg.startswith("COIN"):
      has_coin=True
    elif msg.startswith("GONE"):
      has_coin=False
    print("message: " + msg)
  #
  if has_coin:
    blink(clr_yay,phase)
  else:
    blink(clr_boo,phase)

while True:
  process_cmd(0)
  time.sleep(0.4)
  process_cmd(1)
  time.sleep(0.4)
